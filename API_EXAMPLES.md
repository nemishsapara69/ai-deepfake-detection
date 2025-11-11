# API Testing and Usage Examples

## Using cURL

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Single Image Prediction
```bash
curl -X POST -F "file=@path/to/image.jpg" http://localhost:5000/api/predict
```

### Batch Prediction
```bash
curl -X POST \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  http://localhost:5000/api/batch-predict
```

## Using Python (requests)

```python
import requests

# Health Check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Single Prediction
with open('test_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/predict', files=files)
    print(response.json())

# Batch Prediction
files = [
    ('files', open('image1.jpg', 'rb')),
    ('files', open('image2.jpg', 'rb'))
]
response = requests.post('http://localhost:5000/api/batch-predict', files=files)
print(response.json())
```

## Using JavaScript (fetch)

```javascript
// Single Prediction
async function predictImage(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:5000/api/predict', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  console.log(data);
}

// Usage
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', (e) => {
  predictImage(e.target.files[0]);
});
```

## Using Postman

1. **Health Check**
   - Method: GET
   - URL: http://localhost:5000/api/health

2. **Single Prediction**
   - Method: POST
   - URL: http://localhost:5000/api/predict
   - Body: form-data
   - Key: file
   - Value: [Select file]

3. **Batch Prediction**
   - Method: POST
   - URL: http://localhost:5000/api/batch-predict
   - Body: form-data
   - Key: files (multiple)
   - Value: [Select multiple files]

## Response Examples

### Success Response
```json
{
  "success": true,
  "prediction": {
    "result": "Fake",
    "confidence": 92.34,
    "raw_score": 0.0766,
    "fake_probability": 92.34,
    "real_probability": 7.66
  },
  "face_detection": {
    "box": [120, 85, 250, 320],
    "confidence": 0.9987,
    "num_faces": 1
  },
  "face_crop": "data:image/jpeg;base64,/9j/4AAQ...",
  "timestamp": "2025-11-11T12:00:00.000000"
}
```

### Error Response
```json
{
  "error": "No face detected",
  "detected_faces": 0
}
```

## Rate Limiting

Currently no rate limiting is implemented. For production:
- Consider using Flask-Limiter
- Implement API key authentication
- Add request throttling

## CORS Configuration

The backend allows requests from:
- http://localhost:5173 (Vite dev server)
- http://localhost:3000 (React dev server)

To allow other origins, modify `CORS(app)` in `backend/app.py`.
