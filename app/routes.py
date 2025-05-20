from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from .similarity import calculate_similarity
from .file_utils import extract_text
from .config import Config

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return "Hello, VR Text Similarity App!", 200

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.getcwd(), 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/compare', methods=['POST'])
def compare_texts():
    try:
        audio_text = request.form.get('audio_text', '').strip()
        language = request.form.get('language', 'en')
        file = request.files.get('file')

        if not file or file.filename == '' or '.' not in file.filename:
            return jsonify({'error': 'Invalid or missing file'}), 400

        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in Config.ALLOWED_EXTENSIONS:
            return jsonify({'error': 'Unsupported file type'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(file_path)

        file_text = extract_text(file_path, ext)
        if not audio_text or not file_text:
            return jsonify({'error': 'Missing audio or file text'}), 400

        similarity_score = calculate_similarity(audio_text, file_text, language)
        if similarity_score is None:
            return jsonify({'error': 'Model not available for this language'}), 500

        return jsonify({'similarity_score': similarity_score, 'language': language}), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {e}'}), 500