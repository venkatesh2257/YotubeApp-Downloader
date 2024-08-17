from flask import Flask, request, send_file, abort
import yt_dlp
import os
import pathlib
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Define DOWNLOAD_FOLDER as a temporary directory
DOWNLOAD_FOLDER = str(pathlib.Path.home() / 'Downloads')

# Ensure the folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_youtube_video(url, file_path):
    # Updated ydl_opts with the specific formats you want
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': file_path,
        'noplaylist': True,
    }
    try:
        logging.debug(f"Attempting to download video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.debug(f"Download completed successfully. File saved to: {file_path}")
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('youtube-url')
        if not video_url:
            logging.error("No URL provided")
            return "Error: No URL provided.", 400
        
        file_path = os.path.join(DOWNLOAD_FOLDER, 'video.mp4')
        
        # Download the video
        if download_youtube_video(video_url, file_path):
            # Send file to user
            return send_file(file_path, as_attachment=True, download_name='video.mp4')
        else:
            return "Error downloading video. Please check the URL and try again.", 400
    
    # Serve the index.html file from the root directory
    return send_file('index.html')

# Serve the Google verification file
@app.route('/google77a5f11be42b0911.html')
def google_verification():
    try:
        return send_file('google77a5f11be42b0911.html')
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
