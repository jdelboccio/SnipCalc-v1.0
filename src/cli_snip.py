import sys
import mss
import numpy as np
from PIL import Image
import pytesseract
from calculator import calculate_stats
import json
from datetime import datetime
import os

def process_image(image_path):
    """Process an image file and extract numbers"""
    try:
        # Open and process the image
        img = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(img)
        
        # Extract numbers
        import re
        numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
        
        if numbers:
            # Calculate statistics
            stats = calculate_stats(numbers)
            
            # Print results
            print("\nResults:")
            print(f"SUM: {stats['SUM']:.2f}")
            print(f"AVG: {stats['AVG']:.2f}")
            print(f"COUNT: {stats['COUNT']}")
            print(f"Numbers found: {', '.join(map(str, numbers))}")
            
            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results = {
                'timestamp': timestamp,
                'stats': stats,
                'numbers': numbers
            }
            
            results_file = f'results_{timestamp}.json'
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {results_file}")
            
        else:
            print("No numbers found in the image")
            
    except Exception as e:
        print(f"Error processing image: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli_snip.py <image_path>")
        print("\nExample:")
        print("  python cli_snip.py test_image.png")
        return
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found")
        return
    
    process_image(image_path)

if __name__ == "__main__":
    main()
