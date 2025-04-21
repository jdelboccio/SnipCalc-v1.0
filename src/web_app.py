from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import io
import base64
from calculator import calculate_stats

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # Get the image data from the request
        image_data = request.form['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        
        # Extract numbers
        numbers = [float(x) for x in text.split() if x.replace('.', '').isdigit()]
        
        # Calculate statistics
        if numbers:
            stats = calculate_stats(numbers)
            return jsonify({
                'success': True,
                'stats': stats,
                'numbers': numbers
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No numbers found in the image'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
