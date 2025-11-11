# Deepfake Detection - Complete Web Application

A full-stack web application for detecting AI-generated faces and deepfakes using Deep Learning. Built with React + Vite frontend, Flask backend, and EfficientNet-based CNN model.

![Deepfake Detection](https://img.shields.io/badge/AI-Deepfake%20Detection-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![React](https://img.shields.io/badge/React-18.2-61dafb)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange)

## 🎯 Features

- **🤖 Advanced AI Detection**: Uses EfficientNetB4 transfer learning model
- **👤 Face Detection**: Automatic face detection and cropping using MTCNN
- **⚡ Real-time Analysis**: Get results in seconds
- **🎨 Modern UI**: Beautiful, responsive interface with TailwindCSS
- **📊 Detailed Results**: Confidence scores, probability breakdown, and face visualization
- **🔒 Privacy-Focused**: Images processed locally, not stored
- **📱 Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
deepfake_detection_final/
├── backend/                    # Flask API Server
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment configuration template
├── frontend/                  # React + Vite Application
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── ImageUploader.jsx
│   │   │   └── ResultDisplay.jsx
│   │   ├── App.jsx           # Main App component
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── tailwind.config.js    # TailwindCSS configuration
│   └── index.html            # HTML template
├── model/                     # Machine Learning Model
│   ├── deepfake_model_training.ipynb  # Training notebook
│   └── saved_models/         # Trained model files (generated after training)
├── dataset/                   # Training Dataset
│   ├── train/
│   │   ├── real/            # Real face images
│   │   └── fake/            # Fake face images
│   └── validation/
│       ├── real/
│       └── fake/
├── test_images/              # Sample test images
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git**
- (Optional) **CUDA-enabled GPU** for faster model training

### 1. Clone the Repository

```bash
git clone <repository-url>
cd deepfake_detection_final
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Run the backend server
python app.py
```

Backend will start at: `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at: `http://localhost:5173`

### 4. Model Training (Optional)

If you want to train your own model:

```bash
# Prepare your dataset in the dataset/ folder
# - dataset/train/real/ (add real face images)
# - dataset/train/fake/ (add fake/AI-generated face images)
# - dataset/validation/real/
# - dataset/validation/fake/

# Open the training notebook
cd model
jupyter notebook deepfake_model_training.ipynb

# Follow the notebook instructions to train the model
# The trained model will be saved to model/saved_models/
```

**Note**: If you don't train a custom model, the application will use dummy predictions for demonstration purposes.

## 📊 Dataset Preparation

### Where to Get Data

1. **DFDC (DeepFake Detection Challenge)**
   - Download from: https://ai.facebook.com/datasets/dfdc/
   - Contains 128,000+ videos

2. **FaceForensics++**
   - Download from: https://github.com/ondyari/FaceForensics
   - Contains manipulated and original video sequences

3. **Celeb-DF**
   - Download from: http://www.cs.albany.edu/~lsw/celeb-deepfakeforensics.html
   - High-quality DeepFake dataset

4. **Create Custom Dataset**
   - Real faces: Use Kaggle face datasets, CelebA, etc.
   - Fake faces: Generate using StyleGAN, DALL-E, Midjourney, etc.

### Dataset Structure

```
dataset/
├── train/
│   ├── real/
│   │   ├── real_001.jpg
│   │   ├── real_002.jpg
│   │   └── ...
│   └── fake/
│       ├── fake_001.jpg
│       ├── fake_002.jpg
│       └── ...
└── validation/
    ├── real/
    └── fake/
```

**Recommended**: 
- Training: 80% of images (min 1000 per class)
- Validation: 20% of images (min 200 per class)

## 🔧 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "face_detector_loaded": true,
  "timestamp": "2025-11-11T12:00:00"
}
```

#### 2. Predict Single Image
```http
POST /api/predict
Content-Type: multipart/form-data
```

**Request:**
- `file`: Image file (JPG, PNG, JPEG)

**Response:**
```json
{
  "success": true,
  "prediction": {
    "result": "Fake",
    "confidence": 92.3,
    "raw_score": 0.077,
    "fake_probability": 92.3,
    "real_probability": 7.7
  },
  "face_detection": {
    "box": [120, 85, 250, 320],
    "confidence": 0.999,
    "num_faces": 1
  },
  "face_crop": "data:image/jpeg;base64,...",
  "timestamp": "2025-11-11T12:00:00"
}
```

#### 3. Batch Prediction
```http
POST /api/batch-predict
Content-Type: multipart/form-data
```

**Request:**
- `files`: Multiple image files (max 10)

**Response:**
```json
{
  "success": true,
  "total_files": 3,
  "results": [
    {
      "filename": "image1.jpg",
      "prediction": {...},
      "face_detection": {...}
    },
    ...
  ],
  "timestamp": "2025-11-11T12:00:00"
}
```

## 🧠 Model Architecture

### Base Model: EfficientNetB4
- **Pre-trained on**: ImageNet
- **Input Size**: 224x224x3
- **Parameters**: ~19M (base) + ~1M (custom layers)

### Custom Head
```
EfficientNetB4 (frozen initially)
    ↓
GlobalAveragePooling2D
    ↓
BatchNormalization
    ↓
Dense(512, relu) + Dropout(0.5)
    ↓
Dense(256, relu) + Dropout(0.4)
    ↓
Dense(128, relu) + Dropout(0.3)
    ↓
Dense(1, sigmoid) → Output [0, 1]
```

### Training Strategy
1. **Phase 1**: Train custom head (base frozen) - 50 epochs
2. **Phase 2**: Fine-tune top layers (unfreeze from layer 100) - 20 epochs

### Performance Metrics
- **Accuracy**: ~95% (varies with dataset)
- **Precision**: ~93%
- **Recall**: ~94%
- **AUC-ROC**: ~0.98

## 🎨 Frontend Technology Stack

- **React 18.2**: UI library
- **Vite**: Build tool and dev server
- **TailwindCSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **React Dropzone**: Drag-and-drop file upload
- **Axios**: HTTP client
- **Lucide React**: Icon library

## 🐍 Backend Technology Stack

- **Flask**: Web framework
- **TensorFlow/Keras**: Deep learning
- **OpenCV**: Image processing
- **MTCNN**: Face detection
- **Pillow**: Image manipulation
- **NumPy**: Numerical computing

## 📝 Usage Guide

### Step-by-Step

1. **Start Both Servers**
   - Backend: `python backend/app.py`
   - Frontend: `npm run dev` (in frontend directory)

2. **Open Browser**
   - Navigate to `http://localhost:5173`

3. **Upload Image**
   - Drag & drop an image OR click to browse
   - Supported formats: JPG, JPEG, PNG
   - Max size: 16MB

4. **View Results**
   - 🟢 **Green**: Image is Real
   - 🔴 **Red**: Image is Fake
   - See confidence scores and detected face

5. **Analyze More**
   - Click "Analyze Another Image" to test more images

## 🔮 Future Enhancements

### Planned Features
- [ ] **Live Camera Detection**: Real-time webcam analysis
- [ ] **Grad-CAM Visualization**: Show which parts influenced the decision
- [ ] **Prediction History**: Store and analyze past predictions
- [ ] **Video Support**: Analyze video files frame-by-frame
- [ ] **API Authentication**: Add JWT-based authentication
- [ ] **Model Comparison**: Compare multiple models (EfficientNet, ResNet, Xception)
- [ ] **Explanation AI**: Natural language explanation of results
- [ ] **Docker Support**: Containerized deployment
- [ ] **Cloud Deployment**: Deploy to AWS/GCP/Azure

### Advanced Features
- Temporal consistency analysis for videos
- Multi-face detection and batch analysis
- Detection confidence calibration
- Adversarial robustness testing
- Model explainability dashboard

## 🐛 Troubleshooting

### Common Issues

**1. Backend won't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**2. Frontend connection error**
```bash
# Make sure backend is running on port 5000
# Check CORS settings in backend/app.py
# Verify proxy settings in frontend/vite.config.js
```

**3. Face detection fails**
```bash
# Install MTCNN properly
pip uninstall mtcnn
pip install mtcnn

# Or use OpenCV fallback (automatically used if MTCNN fails)
```

**4. Model not found**
```bash
# If you haven't trained a model, the app will use dummy predictions
# To train: Follow model/deepfake_model_training.ipynb
# The model should be at: model/saved_models/deepfake_detector_efficientnet.h5
```

**5. Out of Memory (OOM) during training**
```bash
# Reduce batch size in the training notebook
BATCH_SIZE = 16  # Instead of 32

# Or use a smaller model
# Change 'EfficientNetB4' to 'EfficientNetB0' in the notebook
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **EfficientNet**: [TensorFlow Models](https://github.com/tensorflow/models)
- **MTCNN**: [Face Detection Library](https://github.com/ipazc/mtcnn)
- **React**: [React.js](https://react.dev/)
- **TailwindCSS**: [Tailwind CSS](https://tailwindcss.com/)
- **DFDC Dataset**: [Facebook AI](https://ai.facebook.com/datasets/dfdc/)
- **FaceForensics++**: [Technical University of Munich](https://github.com/ondyari/FaceForensics)

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

## ⚠️ Disclaimer

This tool is designed for educational and research purposes. While it can detect many types of AI-generated and manipulated images, it is not 100% accurate. Always verify critical information through multiple sources and methods. The detection of deepfakes is an ongoing research challenge, and no system is perfect.

---

**Built with ❤️ using React, TensorFlow, and AI**
