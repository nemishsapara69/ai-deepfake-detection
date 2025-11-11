# Quick Start Guide - Deepfake Detection Application

## 🚀 Fast Setup (5 Minutes)

### Step 1: Install Backend Dependencies
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies
```powershell
# Open new terminal
cd frontend
npm install
```

### Step 3: Start Backend Server
```powershell
# In backend directory with venv activated
python app.py
```
✅ Backend running at: http://localhost:5000

### Step 4: Start Frontend Server
```powershell
# In frontend directory
npm run dev
```
✅ Frontend running at: http://localhost:5173

### Step 5: Test the Application
1. Open browser: http://localhost:5173
2. Upload a test image
3. View results!

---

## 📝 Important Notes

### Without Trained Model
- The app will work but use **dummy predictions** for demonstration
- To get real predictions, you need to train the model first

### Training the Model
```powershell
cd model
jupyter notebook
# Open deepfake_model_training.ipynb
# Add images to dataset/ folders
# Run all cells to train
```

**Dataset Requirements:**
- Minimum 500 images per class (real/fake)
- Recommended 2000+ images per class
- Place in: `dataset/train/real/` and `dataset/train/fake/`

### Where to Get Dataset
1. **Quick Test**: Generate a few fake faces using:
   - https://thispersondoesnotexist.com/
   - https://www.midjourney.com/
   
2. **Real Faces**: Download from:
   - Kaggle Face Datasets
   - CelebA Dataset
   
3. **Full Dataset**: Download DFDC or FaceForensics++

---

## 🎯 Simplified Training (If You're in a Hurry)

1. Create minimal dataset:
   - 100 real face images → `dataset/train/real/`
   - 100 fake face images → `dataset/train/fake/`
   - 20 real face images → `dataset/validation/real/`
   - 20 fake face images → `dataset/validation/fake/`

2. Modify training notebook:
   - Change `EPOCHS = 10` (instead of 50)
   - Change `BATCH_SIZE = 16` (instead of 32)

3. Train for quick results (less accurate but faster)

---

## 🔍 Testing Without Training

The application works without a trained model for UI testing:
- Face detection will work
- Predictions will be random (dummy mode)
- All UI features functional
- Perfect for frontend development

---

## ⚡ Common Commands

### Backend
```powershell
cd backend
.\venv\Scripts\activate    # Activate venv
python app.py              # Run server
deactivate                 # Exit venv
```

### Frontend
```powershell
cd frontend
npm run dev         # Development server
npm run build       # Production build
npm run preview     # Preview production build
```

### Model Training
```powershell
cd model
jupyter notebook    # Start Jupyter
```

---

## 🐛 Quick Fixes

**Problem**: Backend port already in use
```powershell
# Change port in backend/app.py
app.run(port=5001)  # Use different port
```

**Problem**: Frontend can't connect to backend
```powershell
# Check backend is running
# Check CORS settings
# Restart both servers
```

**Problem**: Face detection not working
```powershell
pip install --upgrade opencv-python mtcnn
```

---

## 📁 File Checklist

✅ Backend files:
- `backend/app.py`
- `backend/requirements.txt`
- `backend/.env.example`

✅ Frontend files:
- `frontend/package.json`
- `frontend/src/App.jsx`
- `frontend/src/main.jsx`

✅ Model files:
- `model/deepfake_model_training.ipynb`

✅ Documentation:
- `README.md`
- `QUICKSTART.md` (this file)

---

## 🎉 You're Ready!

Visit http://localhost:5173 and start detecting deepfakes!

For detailed documentation, see `README.md`
