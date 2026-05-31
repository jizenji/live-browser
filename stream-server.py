from flask import Flask, render_template_string, send_file
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hermes Realtime Monitor</title>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <style>
            * { margin: 0; padding: 0; }
            body { 
                background: #000; 
                color: #00ff00;
                font-family: 'Courier New', monospace;
                padding: 20px;
            }
            .container {
                max-width: 1920px;
                margin: 0 auto;
            }
            h1 {
                margin-bottom: 15px;
                text-shadow: 0 0 10px #00ff00;
            }
            video {
                width: 100%;
                border: 3px solid #00ff00;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            }
            .status {
                margin-top: 10px;
                font-size: 14px;
                color: #00aa00;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 HERMES REALTIME MONITOR</h1>
            <video id="video" controls autoplay muted></video>
            <div class="status">
                Status: <span id="status">Connecting...</span>
            </div>
        </div>
        <script>
            var video = document.getElementById('video');
            var statusEl = document.getElementById('status');
            var hls = new Hls();
            
            hls.loadSource('/stream/stream.m3u8');
            hls.attachMedia(video);
            
            hls.on(Hls.Events.MANIFEST_PARSED, function() {
                statusEl.textContent = '✓ LIVE (30fps)';
                video.play();
            });
            
            hls.on(Hls.Events.ERROR, function(event, data) {
                if (data.fatal) {
                    statusEl.textContent = '✗ Connection lost';
                }
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/stream/<path:filename>')
def stream(filename):
    stream_dir = Path('/tmp/stream')
    stream_dir.mkdir(exist_ok=True)
    file_path = stream_dir / filename
    if file_path.exists():
        return send_file(str(file_path), mimetype='application/vnd.apple.mpegurl')
    return "File not found", 404

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
