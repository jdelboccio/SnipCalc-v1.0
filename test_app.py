import pytesseract
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from calculator import calculate_stats

def create_test_image():
    """Create a test image with numbers"""
    # Create a new image with white background
    img = Image.new('RGB', (200, 300), color='white')
    d = ImageDraw.Draw(img)
    
    # Add some numbers to the image
    numbers = ['123', '456', '789', '1011', '1213']
    y_position = 30
    for number in numbers:
        d.text((50, y_position), number, fill='black')
        y_position += 40
    
    # Save the image
    img.save('test_image.png')
    return 'test_image.png'

def test_ocr_and_calc():
    """Test OCR and calculation functionality"""
    try:
        # Create test image
        image_path = create_test_image()
        
        # Open the image
        image = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        print("OCR Result:")
        print(text)
        
        # Extract numbers
        numbers = [float(x) for x in text.split() if x.isdigit()]
        print("\nExtracted numbers:", numbers)
        
        # Calculate statistics
        stats = calculate_stats(numbers)
        print("\nCalculated Statistics:")
        print(f"SUM: {stats['SUM']}")
        print(f"AVG: {stats['AVG']}")
        print(f"COUNT: {stats['COUNT']}")
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting OCR and Calculator Test...")
    success = test_ocr_and_calc()
    print("\nTest completed successfully!" if success else "\nTest failed!")
