from flask import Flask, request, send_file, render_template_string
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
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="google-site-verification" content="google77a5f11be42b0911.html" />
        <title>YouTube Downloader</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 100%;
                position: relative;
            }

            h1 {
                color: #ff0000;
                margin-bottom: 20px;
                text-align: center;
            }

            .header {
                position: absolute;
                top: 10px;
                left: 10px;
                font-weight: bold;
                color: red;
                font-size: 8px;
            }

            label {
                display: block;
                margin-bottom: 10px;
                color: #333;
            }

            input[type="text"] {
                width: calc(100% - 22px);
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }

            button {
                width: 100%;
                padding: 10px 20px;
                background-color: #ff0000;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background-color: #cc0000;
            }

            .note {
                margin-top: 20px;
                font-size: 12px;
                color: #888;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">1080 Quality</div>
            <h1>Download Video</h1>
            <form id="download-form" method="POST">
                <label for="youtube-url">Enter YouTube Video URL:</label>
                <input type="text" id="youtube-url" name="youtube-url" placeholder="https://www.youtube.com/watch?v=example" required>
                <button type="submit">Download</button>
            </form>
        </div>
    </body>
    </html>
    '''

# Serve the Google verification file
@app.route('/google77a5f11be42b0911.html')
def google_verification():
    return send_file('google77a5f11be42b0911.html')

if __name__ == '__main__':
    app.run(debug=True)
