from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_test_image():
    # Create a new image with white background
    width, height = 600, 500  # Larger image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some numbers with clear formatting
    numbers = [
        "123.45",
        "678.90",
        "1234.56",
        "90.12",
        "456.78"
    ]
    
    # Create larger text for better OCR recognition
    try:
        # Try to use a clear font if available
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Draw numbers with more spacing and larger size
    y_position = 60
    for number in numbers:
        # Draw black text on white background with extra padding
        text_width = draw.textlength(number, font=font) if hasattr(draw, 'textlength') else 200
        x_position = (width - text_width) // 2  # Center the text
        
        # Add a white rectangle behind the text for better contrast
        text_height = 60
        draw.rectangle([x_position-10, y_position-10, x_position+text_width+10, y_position+text_height],
                      fill='white')
        
        # Draw the number
        draw.text((x_position, y_position), number, fill='black', font=font)
        y_position += 80  # More spacing between numbers
    
    # Save the image
    img.save('test_numbers.png')
    print("Created test image: test_numbers.png")
    print("Expected numbers:", numbers)
    print("Expected SUM:", sum(float(n) for n in numbers))
    print("Expected AVG:", sum(float(n) for n in numbers) / len(numbers))
    print("Expected COUNT:", len(numbers))

if __name__ == "__main__":
    create_test_image()
