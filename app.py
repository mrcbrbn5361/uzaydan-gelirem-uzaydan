from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

VIDEOS_FOLDER = 'videos'

def get_video_info():
    videos = {}
    for filename in os.listdir(VIDEOS_FOLDER):
        if filename.endswith('.mp4'):
            language = os.path.splitext(filename)[0]
            videos[language] = {
                'versions': [filename]
            }
    return videos

@app.route('/')
def index():
    videos = get_video_info()
    return render_template('index.html', videos=videos)

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEOS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True) 