from flask import Flask, Response, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from time import time
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import jwt
import os
# from authorizer.main import authorize

app = Flask(__name__)

#secret for password encryption
app.secret_key = 'this is a secret!'


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'my_music'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
# Output message if something goes wrong...
    msg = ''
     # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        print(f'username = {username}')
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'  
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (username, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))    
    # If account exists show error and validation checks
    elif request.method == 'POST' or not 'username' in request.form or 'password' in request.form:
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
   
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
    
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:       
            #Generate JWT Token
            jwt_token = generate_jwt_token(account["username"])
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['authorization'] = 'Bearer ' + jwt_token
            response = redirect(url_for('my_account'))
            # response.headers['authorization'] = 
            print(jwt_token)
            flash('Login successful', 'success')
            return response
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!', 'error')

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Render the logout HTML template
    return redirect(url_for('main_page'))

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/my_account')
def my_account():
    token_header = session['authorization']
    token = isTokenValid(token_header)
    if 'error' in token:
        return token, 401
    else:        
        songs=get_all_songs()
        # Redirect to the playlist page or any other desired page
        return render_template('index.html', songs=songs)

@app.route('/my_account/playlists')
def playlists():
    # Retrieve the list of playlists with songs from the database 
    token_header = session['authorization']
    token = isTokenValid(token_header)
    if 'error' in token:
        return token, 401
    else:        
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT p.playlist_name, s.song_name FROM playlists p JOIN playlist_songs ps ON p.id = ps.playlist_id JOIN songs s ON ps.song_id = s.id WHERE p.user_id = %s', (user_id,))
        playlists_and_songs = cursor.fetchall()
        playlists = sort_playlist(playlists_and_songs)
   
    return render_template('my_playlist.html', playlists=playlists)

@app.route('/create_playlist', methods=['GET','POST'])
def create_playlist():
    token_header = session['authorization']
    token = isTokenValid(token_header)
    if 'error' in token:
        return token, 401
    else:        
        if request.method == 'POST' and 'playlist_name' in request.form:
            playlist_name = request.form['playlist_name']
            song_ids = request.form.getlist('song_ids')
            user_id = session['id']
            # Insert the playlist into the playlists table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO playlists (playlist_name, user_id) VALUES (%s, %s)', (playlist_name, user_id))
            playlist_id = cursor.lastrowid

            # Insert the songs into the playlist_songs table
            for song_id in song_ids:
                cursor.execute('INSERT INTO playlist_songs (user_id, playlist_id, song_id) VALUES (%s, %s, %s)', (user_id, playlist_id, song_id))

            mysql.connection.commit()
            return redirect(url_for('playlists'))   
        elif request.method == 'POST':
            return f'not happening {playlist_name}'
        songs = get_all_songs()
    return render_template('create_playlist.html', songs=songs)

@app.route('/add_song_to_playlist', methods=['GET', 'POST'])
def add_song_to_playlist():
    token_header = session['authorization']
    token = isTokenValid(token_header)
    if 'error' in token:
        return token, 401
    else:        
        if request.method == 'POST' and 'song' in request.form and 'playlist' in request.form:
            # Get the selected song and playlist from the form submission
            song_id = request.form['song']
            playlist_id = request.form['playlist']
            user_id = session['id']
            # Perform necessary validation and authorization checks
            # ...

            # Assuming the validation and authorization checks pass, insert the song into the playlist
            if song_id is not None and playlist_id is not None:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT IGNORE INTO playlist_songs (user_id, playlist_id, song_id) VALUES (%s, %s, %s)', (user_id, playlist_id, song_id))
                mysql.connection.commit()
                return redirect(url_for('my_account'))   
            else:
                return "<h2>Song Already in the playlist</h2>"         

    # Fetch the list of songs and playlists to populate the select fields
    songs = get_all_songs()
    playlists = get_playlist()
    
    return render_template('add_song.html', songs=songs, playlists=playlists)

def get_all_songs():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Fetch all the songs from the 'songs' table
    cursor.execute("SELECT * FROM songs")

    songs = cursor.fetchall()
    # Close the database connection
    mysql.connection.commit()
    return songs

def sort_playlist(playlist_songs):
    playlists = {}
    for playlist_song in playlist_songs:
        playlist_name = playlist_song['playlist_name']
        song_name = playlist_song['song_name']
        
        if playlist_name in playlists:
            playlists[playlist_name].append(song_name)
        else:
            playlists[playlist_name] = [song_name]
    return playlists

def get_playlist():
    user_id = session['id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM playlists WHERE user_id = %s", (user_id,))
    playlists = cursor.fetchall()    
    mysql.connection.commit()
    return playlists

def generate_jwt_token(username):
    seconds_now = time()
    user = str(username)
    return jwt.encode(
        {   "username": user, 
            "iat": seconds_now,
            "exp": seconds_now + 30000
        },
        "test", #os.environ.get('JWT_SECRET')
        algorithm="HS256"
    )

def isTokenValid(tokenHeader):
    if not tokenHeader:
        raise ValueError('Token header is not present')
    print('==============================')
    token = tokenHeader.split(' ')[1]  # Bearer <token>
    print(token)
    print('==============================')
    if not token:
        raise ValueError('Token not present')

    jwt_secret = "test" #os.environ.get('JWT_SECRET')
    if not jwt_secret:
        raise ValueError('JWT_SECRET environment variable is not set')

    try:
        decoded_token = jwt.decode(token, jwt_secret, algorithms=["HS256"], leeway=10)
        print(decoded_token)
        return decoded_token
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

@app.route("/songs/<song_name>")
def play_song(song_name):
    full_song_name = song_name + '.mp3'
    with open(f'./songs/{full_song_name}', 'rb') as f:
        return Response(f.read(), mimetype="audio/mpeg")


if __name__ == '__main__':
    app.run()