from flask import Flask, Response, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/songs/<song_name>")
def play_song(song_name):
    full_song_name = song_name + '.mp3'
    print(full_song_name)
    with open(f'./songs/{full_song_name}', 'rb') as f:
        return Response(f.read(), mimetype="audio/mpeg")

@app.route('/index')
def serve_ui():
    with open('./index.html') as f:
        return Response(f.read(), mimetype="text/html")

# POST
@app.route('<playlist_name>', methods = ["POST"])
def create_playlist(playlist_name):
    # Make sure the user has a valid token (in all the endpoints)
    pass # insert a row in the playlists table.

# PUT
@app.route('<playlist_name>', methods=["PUT"])
def add_song_to_playlist(playlist_name):
    # Make sure the user has a valid token (in all the endpoints)
    song = request.args.get('song')
    print(f"adding song {song} into the playlist {playlist_name}")
    pass

@app.route('<playlist_name>', methods = ["GET"])
def get_playlist(playlist_name):
    # go into the database and SELECT all the songs for a given playlist. 
    # SELECT * FROM songs s, playlists p, songs_in_playlist sip WHERE s.song_id = sip.song_id AND p.playlist_id = sip.playlist_id AND p.name = ?
    # song (song_id, song_name, song_location)
    return playlist_name
if __name__ == '__main__':
    app.run()