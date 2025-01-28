from flask import Flask, render_template, request, send_from_directory
import os
from functools import lru_cache
from datetime import datetime

app = Flask(__name__)

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
    except:
        return 0

def should_rescan_videos():
    """Video klasörünün yeniden taranması gerekip gerekmediğini kontrol et"""
    global last_scan_time
    if last_scan_time is None:
        return True
    
    video_dir = os.path.join('static', 'videos')
    if not os.path.exists(video_dir) or not os.listdir(video_dir):
        return False
    
    try:
        latest_modification = max(
            os.path.getmtime(os.path.join(video_dir, f))
            for f in os.listdir(video_dir)
            if os.path.isfile(os.path.join(video_dir, f))
        )
        return datetime.fromtimestamp(latest_modification) > last_scan_time
    except:
        return False

def scan_videos():
    """Videolar klasöründeki videoları tarar ve dil bilgilerini çıkarır"""
    global last_scan_time, videos
    
    video_dir = os.path.join('static', 'videos')
    
    # Eğer video dizini yoksa veya boşsa, boş sözlük döndür
    if not os.path.exists(video_dir):
        try:
            os.makedirs(video_dir)
        except:
            pass
        return {}
    
    # Eğer yeniden tarama gerekmiyorsa, mevcut videoları döndür
    if not should_rescan_videos() and videos:
        return videos
    
    try:
        videos.clear()
        for filename in os.listdir(video_dir):
            if filename.endswith(('.mp4', '.webm', '.mkv')):
                name_parts = filename.rsplit('_', 1)
                if len(name_parts) == 2:
                    video_name = name_parts[0]
                    lang = name_parts[1].split('.')[0]
                    
                    if video_name not in videos:
                        videos[video_name] = {}
                    
                    video_path = os.path.join(video_dir, filename)
                    if os.path.exists(video_path):
                        videos[video_name][lang] = {
                            'filename': filename,
                            'size': os.path.getsize(video_path),
                            'duration': get_video_duration(video_path)
                        }
    except Exception as e:
        print(f"Video tarama hatası: {str(e)}")
        return {}
    
    last_scan_time = datetime.now()
    return videos

@app.route('/')
def index():
    try:
        # Mevcut videoları ve dilleri tara
        current_videos = scan_videos()
        
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
        return f"Bir hata oluştu: {str(e)}", 500

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.after_request
def add_header(response):
    """Önbellekleme başlıkları ekle"""
    response.headers['Cache-Control'] = 'public, max-age=300'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Vercel için WSGI uygulaması
application = app

if __name__ == '__main__':
    # Yerel geliştirme için
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 