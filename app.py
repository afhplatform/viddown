import os
from flask import Flask, request, jsonify, send_file, render_template
from pytube import YouTube, Playlist

app = Flask(__name__, static_folder='static', template_folder='templates')

def get_default_download_folder():
    return os.path.join(os.path.expanduser('~'), 'Downloads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_thumbnail', methods=['GET'])
def get_thumbnail():
    url = request.args.get('url')
    try:
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        return jsonify({'thumbnail': thumbnail_url})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_playlist_info', methods=['GET'])
def get_playlist_info():
    playlist_id = request.args.get('playlistId')
    try:
        playlist = Playlist(f'https://www.youtube.com/playlist?list={playlist_id}')
        videos = []
        for video in playlist.videos:
            videos.append({
                'id': video.video_id,
                'url': video.watch_url,
                'thumbnail': video.thumbnail_url
            })
        return jsonify({'videos': videos})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download_video', methods=['GET'])
def download_video():
    url = request.args.get('url')
    resolution = request.args.get('resolution')
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        if stream:
            default_folder = get_default_download_folder()
            file_path = stream.download(output_path=default_folder)
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Resolution not available'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
