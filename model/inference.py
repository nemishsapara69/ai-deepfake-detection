"""
Simple Inference Script for Deepfake Detection Model
Use this script to test the trained model on individual images
"""

import os
import sys
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import cv2

# Configuration
MODEL_PATH = './saved_models/deepfake_detector_efficientnet.h5'
IMG_SIZE = 224

def load_model_for_inference():
    """Load the trained model"""
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at: {MODEL_PATH}")
        print("Please train the model first using deepfake_model_training.ipynb")
        return None
    
    try:
        model = keras.models.load_model(MODEL_PATH)
        print(f"✅ Model loaded successfully from {MODEL_PATH}")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None

def preprocess_image(image_path):
    """Load and preprocess image for model input"""
    try:
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize
        img = img.resize((IMG_SIZE, IMG_SIZE))
        
        # Convert to array and normalize
        img_array = np.array(img)
        img_array = img_array.astype('float32') / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    except Exception as e:
        print(f"❌ Error preprocessing image: {str(e)}")
        return None

def predict_image(model, image_path, verbose=True):
    """Predict if image is real or fake"""
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return None
    
    # Preprocess
    img_array = preprocess_image(image_path)
    if img_array is None:
        return None
    
    # Predict
    prediction = model.predict(img_array, verbose=0)[0][0]
    
    # Interpret result
    if prediction < 0.5:
        result = "FAKE"
        confidence = (1 - prediction) * 100
    else:
        result = "REAL"
        confidence = prediction * 100
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Image: {os.path.basename(image_path)}")
        print(f"{'='*60}")
        print(f"Result: {result}")
        print(f"Confidence: {confidence:.2f}%")
        print(f"Raw Score: {prediction:.6f}")
        print(f"Fake Probability: {((1 - prediction) * 100):.2f}%")
        print(f"Real Probability: {(prediction * 100):.2f}%")
        print(f"{'='*60}\n")
    
    return {
        'result': result,
        'confidence': confidence,
        'raw_score': prediction,
        'fake_probability': (1 - prediction) * 100,
        'real_probability': prediction * 100
    }

def batch_predict(model, image_folder):
    """Predict on all images in a folder"""
    
    if not os.path.exists(image_folder):
        print(f"❌ Folder not found: {image_folder}")
        return
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = [
        f for f in os.listdir(image_folder)
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    if not image_files:
        print(f"No images found in {image_folder}")
        return
    
    print(f"\n{'='*60}")
    print(f"Batch Prediction on {len(image_files)} images")
    print(f"{'='*60}\n")
    
    results = []
    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)
        result = predict_image(model, img_path, verbose=False)
        
        if result:
            results.append({
                'filename': img_file,
                **result
            })
            print(f"✅ {img_file:<30} → {result['result']:<5} ({result['confidence']:.1f}%)")
        else:
            print(f"❌ {img_file:<30} → Error")
    
    # Summary
    if results:
        fake_count = sum(1 for r in results if r['result'] == 'FAKE')
        real_count = sum(1 for r in results if r['result'] == 'REAL')
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Total: {len(results)}")
        print(f"  Real: {real_count} ({real_count/len(results)*100:.1f}%)")
        print(f"  Fake: {fake_count} ({fake_count/len(results)*100:.1f}%)")
        print(f"  Avg Confidence: {avg_confidence:.2f}%")
        print(f"{'='*60}\n")
    
    return results

def main():
    """Main function"""
    
    print("\n" + "="*60)
    print("Deepfake Detection - Inference Script")
    print("="*60 + "\n")
    
    # Load model
    model = load_model_for_inference()
    if model is None:
        return
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single image:  python inference.py path/to/image.jpg")
        print("  Batch predict: python inference.py path/to/folder/")
        print("\nExample:")
        print("  python inference.py ../test_images/sample.jpg")
        print("  python inference.py ../test_images/")
        return
    
    path = sys.argv[1]
    
    # Check if it's a file or directory
    if os.path.isfile(path):
        # Single image prediction
        predict_image(model, path)
    elif os.path.isdir(path):
        # Batch prediction
        batch_predict(model, path)
    else:
        print(f"❌ Path not found: {path}")

if __name__ == "__main__":
    main()
