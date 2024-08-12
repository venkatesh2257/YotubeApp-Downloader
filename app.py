from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import pathlib

app = Flask(__name__)

# Define DOWNLOAD_FOLDER as the user's Downloads directory
DOWNLOAD_FOLDER = str(pathlib.Path.home() / 'Downloads')

# Ensure the folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_youtube_video(url, file_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': file_path,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('youtube-url')
        file_path = os.path.join(DOWNLOAD_FOLDER, 'video.mp4')
        
        # Download the video
        download_youtube_video(video_url, file_path)
        
        # Send file to user
        return send_file(file_path, as_attachment=True)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
