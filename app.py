from flask import Flask, send_from_directory, Response
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
    'pt': 'Portekizce',
    'de': 'Almanca',
    'fr': 'Fransızca',
    'jp': 'Japonca',
    'kor': 'Korece'
}

# Video klasörü
VIDEO_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'videos')

@app.route('/')
def index():
    """Ana sayfayı göster"""
    return app.send_static_file('index.html')

@app.route('/static/videos/<path:filename>')
def serve_video(filename):
    """Video dosyalarını servis et"""
    try:
        if not os.path.exists(os.path.join(VIDEO_FOLDER, filename)):
            logger.error(f"Video dosyası bulunamadı: {filename}")
            return "Video bulunamadı", 404

        response = send_from_directory(VIDEO_FOLDER, filename, conditional=True)
        response.headers.update({
            'Cache-Control': 'public, max-age=31536000',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Accept-Ranges': 'bytes',
            'Content-Type': 'video/mp4'
        })
        return response
    except Exception as e:
        logger.error(f"Video servis hatası: {str(e)}")
        return str(e), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Statik dosyaları servis et"""
    try:
        response = send_from_directory('static', path)
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response
    except Exception as e:
        logger.error(f"Statik dosya hatası: {str(e)}")
        return str(e), 404

@app.after_request
def add_header(response):
    """Güvenlik başlıkları ekle"""
    response.headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    })
    return response

# Vercel için WSGI uygulaması
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, threaded=True) 