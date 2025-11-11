# Project Structure Visualization

```
deepfake_detection_final/
│
├── 📁 backend/                          # Flask API Server
│   ├── app.py                          # Main Flask application (API endpoints)
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment configuration template
│   ├── test_api.py                     # API testing script
│   └── uploads/                        # Uploaded images (auto-created)
│
├── 📁 frontend/                         # React + Vite Application
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── Header.jsx             # Top navigation bar
│   │   │   ├── Footer.jsx             # Footer component
│   │   │   ├── ImageUploader.jsx      # Drag-and-drop upload
│   │   │   └── ResultDisplay.jsx      # Prediction results display
│   │   ├── App.jsx                    # Main application component
│   │   ├── main.jsx                   # React entry point
│   │   └── index.css                  # Global styles (TailwindCSS)
│   ├── index.html                     # HTML template
│   ├── package.json                   # Node.js dependencies
│   ├── vite.config.js                 # Vite configuration
│   ├── tailwind.config.js             # TailwindCSS configuration
│   ├── postcss.config.js              # PostCSS configuration
│   └── node_modules/                  # Node packages (auto-created)
│
├── 📁 model/                            # Machine Learning Model
│   ├── deepfake_model_training.ipynb  # Training notebook (Jupyter)
│   ├── inference.py                   # Standalone inference script
│   ├── saved_models/                  # Trained models (generated)
│   │   ├── deepfake_detector_efficientnet.h5
│   │   ├── deepfake_detector_weights.h5
│   │   ├── deepfake_detector_savedmodel/
│   │   └── model_architecture.json
│   └── logs/                          # Training logs & visualizations
│       ├── training_history.png
│       ├── confusion_matrix.png
│       └── roc_curve.png
│
├── 📁 dataset/                          # Training Dataset Structure
│   ├── 📁 train/
│   │   ├── 📁 real/                   # Real face images for training
│   │   │   └── (Place real images here)
│   │   └── 📁 fake/                   # Fake face images for training
│   │       └── (Place fake images here)
│   └── 📁 validation/
│       ├── 📁 real/                   # Real face images for validation
│       │   └── (Place real images here)
│       └── 📁 fake/                   # Fake face images for validation
│           └── (Place fake images here)
│
├── 📁 test_images/                      # Sample Test Images
│   ├── README.md                      # Testing guide
│   └── (Place test images here)
│
├── 📄 README.md                         # Main documentation (START HERE!)
├── 📄 QUICKSTART.md                     # Fast setup guide
├── 📄 DELIVERABLES.md                   # Project deliverables summary
├── 📄 API_EXAMPLES.md                   # API usage examples
├── 📄 LICENSE                           # MIT License
├── 📄 .gitignore                        # Git ignore rules
└── 📄 setup.ps1                         # Automated setup script (PowerShell)
```

## 📋 File Descriptions

### Backend Files
| File | Purpose | Key Features |
|------|---------|--------------|
| `app.py` | Flask API server | REST endpoints, face detection, model inference |
| `requirements.txt` | Python packages | TensorFlow, Flask, OpenCV, MTCNN |
| `test_api.py` | API testing | Automated endpoint testing |

### Frontend Files
| File | Purpose | Key Features |
|------|---------|--------------|
| `App.jsx` | Main app | State management, routing |
| `ImageUploader.jsx` | Upload UI | Drag-drop, preview, API call |
| `ResultDisplay.jsx` | Results UI | Confidence bars, visualizations |
| `Header.jsx` | Navigation | Branding, links |
| `Footer.jsx` | Footer | Credits, links |

### Model Files
| File | Purpose | Key Features |
|------|---------|--------------|
| `deepfake_model_training.ipynb` | Model training | EfficientNetB4, data augmentation, evaluation |
| `inference.py` | Standalone testing | CLI tool for model testing |

### Documentation Files
| File | Purpose | Target Audience |
|------|---------|-----------------|
| `README.md` | Complete guide | All users (comprehensive) |
| `QUICKSTART.md` | Fast setup | Developers (quick start) |
| `API_EXAMPLES.md` | API usage | API consumers |
| `DELIVERABLES.md` | Project summary | Reviewers, stakeholders |

## 🔄 Data Flow

```
User Browser (React)
        ↓
    Upload Image
        ↓
Frontend (localhost:5173)
        ↓
    HTTP POST /api/predict
        ↓
Backend (localhost:5000)
        ↓
    1. Receive Image
    2. Detect Face (MTCNN)
    3. Crop Face Region
    4. Preprocess (resize, normalize)
        ↓
TensorFlow Model
        ↓
    Inference (EfficientNetB4)
        ↓
    Prediction Score [0-1]
        ↓
Backend Processing
        ↓
    Interpret Result
    Format Response (JSON)
        ↓
Frontend Display
        ↓
    Show Results
    - Real/Fake indicator
    - Confidence score
    - Face crop
    - Probabilities
```

## 🎨 Technology Stack Overview

### Frontend Stack
```
React 18.2
    ├── Vite (Build Tool)
    ├── TailwindCSS (Styling)
    ├── Framer Motion (Animations)
    ├── React Dropzone (File Upload)
    ├── Axios (HTTP Client)
    └── Lucide React (Icons)
```

### Backend Stack
```
Flask 2.3
    ├── TensorFlow 2.13 (ML Framework)
    ├── Keras 2.13 (High-level API)
    ├── OpenCV 4.8 (Image Processing)
    ├── MTCNN (Face Detection)
    ├── Pillow (Image Manipulation)
    └── NumPy (Numerical Computing)
```

### ML Stack
```
EfficientNetB4 (Base Model)
    ├── ImageNet Pre-training
    ├── Transfer Learning
    ├── Custom Dense Layers
    ├── Dropout Regularization
    └── Binary Classification Output
```

## 📊 Size Estimates

| Component | Estimated Size |
|-----------|----------------|
| Frontend Dependencies | ~200 MB |
| Backend Dependencies | ~1.5 GB (TensorFlow) |
| Trained Model | ~75 MB |
| Source Code | ~1 MB |
| Documentation | ~500 KB |

## 🚦 Startup Sequence

1. **Backend Start**
   ```
   Load Model → Initialize Face Detector → Start Flask Server
   ```

2. **Frontend Start**
   ```
   Build React App → Start Dev Server → Proxy API Calls
   ```

3. **Request Flow**
   ```
   Upload → Validate → Detect → Predict → Display
   ```

## 🔐 Security Considerations

- File size limits (16MB)
- File type validation (.jpg, .jpeg, .png)
- CORS configuration
- Input sanitization
- Error handling
- No permanent storage of uploads

## 🎯 Entry Points

| Task | Entry Point | Command |
|------|-------------|---------|
| Setup | `setup.ps1` | `.\setup.ps1` |
| Run Backend | `backend/app.py` | `python app.py` |
| Run Frontend | `frontend/` | `npm run dev` |
| Train Model | `model/deepfake_model_training.ipynb` | Open in Jupyter |
| Test API | `backend/test_api.py` | `python test_api.py` |
| Test Model | `model/inference.py` | `python inference.py <image>` |
| Read Docs | `README.md` | Open in editor/browser |

---

**Note**: This structure is designed for easy navigation, development, and deployment!
