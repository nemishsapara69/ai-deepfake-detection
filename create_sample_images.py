"""
Sample Image Generator for Deepfake Detection Testing
Creates simple synthetic images for testing the detection system
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random

def create_sample_images():
    """Generate sample images for testing"""

    # Create test_images directory if it doesn't exist
    os.makedirs('test_images', exist_ok=True)

    # Generate some simple colored images (simulating faces)
    colors = [
        ('real_blue', (100, 150, 200)),    # Blue tint - "real"
        ('real_green', (120, 180, 140)),   # Green tint - "real"
        ('fake_red', (200, 100, 100)),     # Red tint - "fake"
        ('fake_purple', (180, 100, 200)),  # Purple tint - "fake"
    ]

    for name, color in colors:
        # Create a 512x512 image
        img = Image.new('RGB', (512, 512), color=color)

        # Add some simple patterns to simulate face features
        draw = ImageDraw.Draw(img)

        # Add circles for eyes
        eye_color = (255, 255, 255) if 'real' in name else (0, 0, 0)
        draw.ellipse([150, 200, 200, 250], fill=eye_color)
        draw.ellipse([312, 200, 362, 250], fill=eye_color)

        # Add rectangle for mouth
        mouth_color = (0, 0, 0) if 'real' in name else (255, 255, 255)
        draw.rectangle([200, 350, 312, 380], fill=mouth_color)

        # Save the image
        filename = f'test_images/{name}_sample.jpg'
        img.save(filename)
        print(f"Created: {filename}")

    # Create a more complex "face-like" image
    img = Image.new('RGB', (512, 512), color=(180, 160, 140))

    draw = ImageDraw.Draw(img)

    # Draw a simple face shape
    draw.ellipse([100, 100, 412, 412], fill=(220, 190, 160))

    # Eyes
    draw.ellipse([180, 220, 220, 260], fill=(255, 255, 255))
    draw.ellipse([292, 220, 332, 260], fill=(255, 255, 255))
    draw.ellipse([190, 230, 210, 250], fill=(0, 0, 0))
    draw.ellipse([302, 230, 322, 250], fill=(0, 0, 0))

    # Nose
    draw.polygon([(256, 280), (246, 320), (266, 320)], fill=(200, 170, 140))

    # Mouth
    draw.arc([220, 330, 292, 370], start=0, end=180, fill=(150, 50, 50), width=3)

    img.save('test_images/complex_face_sample.jpg')
    print("Created: test_images/complex_face_sample.jpg")

    print("\n✅ Sample images created successfully!")
    print("📁 Check the test_images/ folder for generated images")
    print("🧪 Use these images to test your deepfake detection model")

if __name__ == "__main__":
    create_sample_images()