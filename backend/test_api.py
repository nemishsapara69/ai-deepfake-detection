"""
Test Script for Deepfake Detection API
Run this script to test the backend API endpoints
"""

import requests
import json
import os

# Configuration
API_BASE_URL = "http://localhost:5000"
TEST_IMAGE_PATH = "../test_images/sample.jpg"  # Change this to your test image path

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_predict(image_path):
    """Test the prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Prediction Endpoint")
    print("="*60)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        print("Please update TEST_IMAGE_PATH in this script")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/api/predict", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Prediction Result:")
            print(f"  - Classification: {data['prediction']['result']}")
            print(f"  - Confidence: {data['prediction']['confidence']:.2f}%")
            print(f"  - Fake Probability: {data['prediction']['fake_probability']:.2f}%")
            print(f"  - Real Probability: {data['prediction']['real_probability']:.2f}%")
            print(f"  - Faces Detected: {data['face_detection']['num_faces']}")
            print(f"  - Face Detection Confidence: {data['face_detection']['confidence']:.2f}")
            return True
        else:
            print(f"❌ Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_batch_predict(image_paths):
    """Test the batch prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Batch Prediction Endpoint")
    print("="*60)
    
    valid_paths = [path for path in image_paths if os.path.exists(path)]
    
    if not valid_paths:
        print(f"❌ No valid images found")
        return False
    
    try:
        files = [('files', open(path, 'rb')) for path in valid_paths]
        response = requests.post(f"{API_BASE_URL}/api/batch-predict", files=files)
        
        # Close file handles
        for _, f in files:
            f.close()
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Batch Prediction Results:")
            print(f"  - Total Files: {data['total_files']}")
            print(f"  - Results:")
            for i, result in enumerate(data['results'], 1):
                if 'error' in result:
                    print(f"    {i}. {result['filename']}: Error - {result['error']}")
                else:
                    print(f"    {i}. {result['filename']}: {result['prediction']['result']} ({result['prediction']['confidence']:.1f}%)")
            return True
        else:
            print(f"❌ Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 DEEPFAKE DETECTION API TEST SUITE")
    print("="*60)
    
    print("\n📋 Prerequisites:")
    print("  1. Backend server running on http://localhost:5000")
    print("  2. Test image available (update TEST_IMAGE_PATH)")
    print("\nStarting tests...\n")
    
    # Test 1: Health Check
    health_ok = test_health_check()
    
    # Test 2: Single Prediction
    if health_ok:
        predict_ok = test_predict(TEST_IMAGE_PATH)
    else:
        print("\n⚠️ Skipping prediction tests - health check failed")
        predict_ok = False
    
    # Test 3: Batch Prediction (if we have multiple test images)
    # Uncomment and modify the paths below to test batch prediction
    # batch_images = [
    #     "../test_images/sample1.jpg",
    #     "../test_images/sample2.jpg",
    #     "../test_images/sample3.jpg"
    # ]
    # batch_ok = test_batch_predict(batch_images)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"  ✅ Health Check: {'PASS' if health_ok else 'FAIL'}")
    print(f"  {'✅' if predict_ok else '❌'} Single Prediction: {'PASS' if predict_ok else 'FAIL'}")
    # print(f"  {'✅' if batch_ok else '❌'} Batch Prediction: {'PASS' if batch_ok else 'FAIL'}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
