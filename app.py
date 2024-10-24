from flask import Flask, request, jsonify, send_file, render_template
from PIL import Image
import pytesseract
import io
import os
from docx import Document
import tempfile

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C://Program Files//Tesseract-OCR//tesseract.exe'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_image_to_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))

    try:
        text = pytesseract.image_to_string(image)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/txt', methods=['POST'])
def download_txt():
    text = request.json.get('text', '')
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        temp_file.write(text)
    return send_file(temp_file.name, as_attachment=True, download_name='converted_text.txt')


@app.route('/download/docx', methods=['POST'])
def download_docx():
    text = request.json.get('text', '')
    doc = Document()
    doc.add_paragraph(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
        doc.save(temp_file.name)
    return send_file(temp_file.name, as_attachment=True, download_name='converted_text.docx')


if __name__ == '__main__':
    app.run(debug=True)
