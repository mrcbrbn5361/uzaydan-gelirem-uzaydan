from flask import Flask, render_template, request, send_from_directory, url_for, send_file
import os
from functools import lru_cache
from datetime import datetime
import logging
import mimetypes

app = Flask(__name__)

# Mimetype tanımlamaları ekle
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('video/webm', '.webm')
mimetypes.add_type('video/mkv', '.mkv')

# Logging ayarları
logging.basicConfig(level=logging.DEBUG)
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

# Video bilgilerini tutacak sözlük
videos = {}
last_scan_time = None

def get_video_url(filename):
    """Video URL'sini oluştur"""
    if os.environ.get('VERCEL_URL'):
        return f"https://{os.environ.get('VERCEL_URL')}/video/{filename}"
    return url_for('serve_video', filename=filename)

def get_absolute_video_path():
    """Video dizininin mutlak yolunu al"""
    if os.environ.get('VERCEL'):
        return os.path.join(os.getcwd(), 'static', 'videos')
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, 'static', 'videos')

@app.route('/video/<path:filename>')
def serve_video(filename):
    """Video dosyalarını servis et"""
    try:
        video_dir = os.path.join('static', 'videos')
        response = send_from_directory(video_dir, filename)
        response.headers['Content-Type'] = 'video/mp4'
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        logger.error(f"Video servis hatası: {str(e)}")
        return f"Video bulunamadı: {filename}", 404

@lru_cache(maxsize=32)
def get_video_duration(video_path):
    """Video süresini al (önbellekli)"""
    try:
        import cv2
        video = cv2.VideoCapture(video_path)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
        duration = frames / fps if fps > 0 else 0
        video.release()
        return duration
    except Exception as e:
        logger.error(f"Video süresi alınamadı: {str(e)}")
        return 0

def should_rescan_videos():
    """Video klasörünün yeniden taranması gerekip gerekmediğini kontrol et"""
    global last_scan_time
    if last_scan_time is None:
        return True
    
    video_dir = get_absolute_video_path()
    if not os.path.exists(video_dir):
        logger.warning(f"Video dizini bulunamadı: {video_dir}")
        return False
    
    try:
        files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
        if not files:
            logger.warning("Video dizini boş")
            return False
        
        latest_modification = max(
            os.path.getmtime(os.path.join(video_dir, f))
            for f in files
        )
        return datetime.fromtimestamp(latest_modification) > last_scan_time
    except Exception as e:
        logger.error(f"Video tarama hatası: {str(e)}")
        return False

def scan_videos():
    """Videolar klasöründeki videoları tarar ve dil bilgilerini çıkarır"""
    global last_scan_time, videos
    
    video_dir = get_absolute_video_path()
    logger.info(f"Video dizini taranıyor: {video_dir}")
    
    # Eğer video dizini yoksa oluştur
    if not os.path.exists(video_dir):
        try:
            os.makedirs(video_dir)
            logger.info(f"Video dizini oluşturuldu: {video_dir}")
        except Exception as e:
            logger.error(f"Video dizini oluşturulamadı: {str(e)}")
            return {}
    
    # Eğer yeniden tarama gerekmiyorsa, mevcut videoları döndür
    if not should_rescan_videos() and videos:
        return videos
    
    try:
        videos.clear()
        files = os.listdir(video_dir)
        logger.info(f"Bulunan dosyalar: {files}")
        
        for filename in files:
            if filename.endswith(('.mp4', '.webm', '.mkv')):
                name_parts = filename.rsplit('_', 1)
                if len(name_parts) == 2:
                    video_name = name_parts[0]
                    lang = name_parts[1].split('.')[0]
                    
                    if video_name not in videos:
                        videos[video_name] = {}
                    
                    video_path = os.path.join(video_dir, filename)
                    if os.path.exists(video_path):
                        file_size = os.path.getsize(video_path)
                        duration = get_video_duration(video_path)
                        
                        videos[video_name][lang] = {
                            'filename': filename,
                            'url': get_video_url(filename),
                            'size': file_size,
                            'duration': duration
                        }
                        logger.info(f"Video eklendi: {filename} ({file_size} bytes, {duration} saniye)")
    except Exception as e:
        logger.error(f"Video tarama hatası: {str(e)}")
        return {}
    
    last_scan_time = datetime.now()
    return videos

@app.route('/')
def index():
    try:
        # Mevcut videoları ve dilleri tara
        current_videos = scan_videos()
        logger.info(f"Bulunan videolar: {current_videos}")
        
        # Tüm mevcut dilleri topla
        available_languages = set()
        for video_data in current_videos.values():
            available_languages.update(video_data.keys())
        
        # Seçili dil (varsayılan olarak tr veya ilk dil)
        selected_lang = request.args.get('lang', 'tr')
        if selected_lang not in available_languages and available_languages:
            selected_lang = list(available_languages)[0]
        
        return render_template('index.html', 
                             videos=current_videos,
                             languages=sorted(available_languages),
                             selected_lang=selected_lang,
                             language_names=LANGUAGE_NAMES)
    except Exception as e:
        logger.error(f"Sayfa yüklenirken hata: {str(e)}")
        return f"Bir hata oluştu: {str(e)}", 500

@app.route('/static/<path:path>')
def serve_static(path):
    try:
        if path.startswith('videos/'):
            filename = os.path.basename(path)
            return serve_video(filename)
        response = send_from_directory('static', path)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response
    except Exception as e:
        logger.error(f"Statik dosya sunulurken hata: {str(e)}")
        return f"Dosya bulunamadı: {path}", 404

@app.after_request
def add_header(response):
    """Önbellekleme başlıkları ekle"""
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    if request.path.endswith('.mp4'):
        response.headers['Content-Type'] = 'video/mp4'
        response.headers['Accept-Ranges'] = 'bytes'
    return response

# Vercel için WSGI uygulaması
application = app

if __name__ == '__main__':
    # Yerel geliştirme için
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 