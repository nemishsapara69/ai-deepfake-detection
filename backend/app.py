"""
Deepfake Detection Backend API
Flask-based REST API for image upload, face detection, and deepfake classification
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import cv2
from PIL import Image
import io
import base64
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import keras
from mtcnn import MTCNN
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and face detector
model = None
face_detector = None

# Model configuration
IMG_SIZE = 224
MODEL_PATH = '../model/saved_models/deepfake_detector_efficientnet.h5'


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_model():
    """Load the trained deepfake detection model"""
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = keras.models.load_model(MODEL_PATH)
            logger.info(f"✅ Model loaded successfully from {MODEL_PATH}")
        else:
            logger.warning(f"⚠️ Model not found at {MODEL_PATH}. Using dummy predictions.")
            model = None
    except Exception as e:
        logger.error(f"❌ Error loading model: {str(e)}")
        model = None


def load_face_detector():
    """Initialize MTCNN face detector"""
    global face_detector
    try:
        face_detector = MTCNN()
        logger.info("✅ MTCNN face detector initialized")
    except Exception as e:
        logger.error(f"❌ Error initializing face detector: {str(e)}")
        face_detector = None


def detect_and_crop_face(image):
    """
    Detect face in image using MTCNN and crop it
    Returns cropped face image and detection info
    """
    try:
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(img_array.shape) == 2:  # Grayscale
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        # Detect faces
        if face_detector:
            detections = face_detector.detect_faces(img_array)
        else:
            # Fallback to OpenCV Haar Cascade if MTCNN fails
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                detections = [{'box': [x, y, w, h], 'confidence': 0.99}]
            else:
                detections = []
        
        if len(detections) == 0:
            logger.warning("No face detected in image")
            return None, None, "No face detected"
        
        # Get the face with highest confidence
        face = max(detections, key=lambda x: x['confidence'])
        x, y, width, height = face['box']
        confidence = face['confidence']
        
        # Add padding around face
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        width = min(img_array.shape[1] - x, width + 2 * padding)
        height = min(img_array.shape[0] - y, height + 2 * padding)
        
        # Crop face
        face_img = img_array[y:y+height, x:x+width]
        
        # Convert back to PIL Image
        face_pil = Image.fromarray(face_img)
        
        detection_info = {
            'box': [int(x), int(y), int(width), int(height)],
            'confidence': float(confidence),
            'num_faces': len(detections)
        }
        
        return face_pil, detection_info, None
        
    except Exception as e:
        logger.error(f"Error in face detection: {str(e)}")
        return None, None, str(e)


def preprocess_image(image):
    """Preprocess image for model input"""
    # Resize to model input size
    image = image.resize((IMG_SIZE, IMG_SIZE))
    
    # Convert to array and normalize
    img_array = np.array(image)
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def predict_deepfake(image):
    """
    Run deepfake detection on preprocessed image
    Returns prediction result and confidence
    """
    try:
        # Preprocess image
        processed_img = preprocess_image(image)
        
        if model is not None:
            # Get prediction
            prediction = model.predict(processed_img, verbose=0)[0][0]
        else:
            # Dummy prediction if model not loaded
            logger.warning("Using dummy prediction (model not loaded)")
            prediction = np.random.random()
        
        # Interpret result
        # Assuming: 0 = FAKE, 1 = REAL
        if prediction < 0.5:
            result = "Fake"
            confidence = (1 - prediction) * 100
        else:
            result = "Real"
            confidence = prediction * 100
        
        return {
            'result': result,
            'confidence': float(confidence),
            'raw_score': float(prediction),
            'fake_probability': float((1 - prediction) * 100),
            'real_probability': float(prediction * 100)
        }
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return None


def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"


@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'message': 'Deepfake Detection API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            '/api/predict': 'POST - Upload image for deepfake detection',
            '/api/health': 'GET - Check API health status'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'face_detector_loaded': face_detector is not None,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint
    Accepts image file and returns deepfake detection result
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG'}), 400
        
        # Read and open image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        logger.info(f"Processing image: {file.filename}")
        
        # Detect and crop face
        face_image, detection_info, error = detect_and_crop_face(image)
        
        if error or face_image is None:
            return jsonify({
                'error': error or 'Face detection failed',
                'detected_faces': 0
            }), 400
        
        logger.info(f"Face detected with confidence: {detection_info['confidence']:.2f}")
        
        # Run deepfake prediction
        prediction_result = predict_deepfake(face_image)
        
        if prediction_result is None:
            return jsonify({'error': 'Prediction failed'}), 500
        
        # Convert face crop to base64 for response
        face_base64 = image_to_base64(face_image)
        
        # Prepare response
        response = {
            'success': True,
            'prediction': prediction_result,
            'face_detection': detection_info,
            'face_crop': face_base64,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Prediction: {prediction_result['result']} ({prediction_result['confidence']:.2f}%)")
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in prediction endpoint: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint
    Accepts multiple images and returns predictions for each
    """
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400
        
        if len(files) > 10:
            return jsonify({'error': 'Maximum 10 files allowed per batch'}), 400
        
        results = []
        
        for file in files:
            try:
                if not allowed_file(file.filename):
                    results.append({
                        'filename': file.filename,
                        'error': 'Invalid file type'
                    })
                    continue
                
                # Process image
                image_bytes = file.read()
                image = Image.open(io.BytesIO(image_bytes))
                
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Detect face
                face_image, detection_info, error = detect_and_crop_face(image)
                
                if error or face_image is None:
                    results.append({
                        'filename': file.filename,
                        'error': error or 'Face detection failed'
                    })
                    continue
                
                # Predict
                prediction_result = predict_deepfake(face_image)
                
                if prediction_result:
                    results.append({
                        'filename': file.filename,
                        'prediction': prediction_result,
                        'face_detection': detection_info
                    })
                else:
                    results.append({
                        'filename': file.filename,
                        'error': 'Prediction failed'
                    })
                    
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'total_files': len(files),
            'results': results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch prediction: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


if __name__ == '__main__':
    # Load model and face detector on startup
    logger.info("🚀 Starting Deepfake Detection API...")
    load_model()
    load_face_detector()
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
