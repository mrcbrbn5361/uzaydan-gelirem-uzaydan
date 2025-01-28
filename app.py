from flask import Flask, render_template, send_from_directory, Response
from flask_cors import CORS
import os
import logging
import mimetypes

app = Flask(__name__)
CORS(app)

# Mimetype tanımlamaları
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('video/webm', '.webm')
mimetypes.add_type('video/mkv', '.mkv')

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dil kodlarının Türkçe karşılıkları
LANGUAGE_NAMES = {
    'tr': 'Türkçe',
    'en': 'İngilizce',
    'ru': 'Rusça',
    'zh': 'Çince',
    'hi': 'Hintçe',
    'ar': 'Arapça',
    'es': 'İspanyolca',
    'pt': 'Portekizce'
}

# Video klasörü
VIDEO_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'videos')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/static/videos/<path:filename>')
def serve_video(filename):
    try:
        response = send_from_directory(VIDEO_FOLDER, filename, conditional=True)
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Accept-Ranges'] = 'bytes'
        return response
    except Exception as e:
        logger.error(f"Video servis hatası: {str(e)}")
        return str(e), 500

@app.route('/static/<path:path>')
def serve_static(path):
    try:
        response = send_from_directory('static', path)
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response
    except Exception as e:
        logger.error(f"Statik dosya hatası: {str(e)}")
        return str(e), 404

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, threaded=True) 