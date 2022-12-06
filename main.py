import os
from flask import (
    Flask, 
    jsonify, 
    request,
    render_template,
    redirect
)

from services import Connection

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app: Flask = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/img')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
conn: Connection = Connection()

@app.route("/")
def index():
    games = conn.get_games_list()
    genres = conn.get_genre_list()
    platforms = conn.get_platform_list()
    languages = conn.get_language_list()
    publishers = conn.get_publisher_list()
    
    search = {
        'title': '',
        'platform': '',
        'publisher': '',
        'language': '',
        'genre': '',
    }

    return render_template('index.html', games=games, genres=genres, platforms=platforms, languages=languages, publishers=publishers, search=search)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    g = {}
    
    if request.method == 'POST':
        try:
            g['id'] = request.form.get('id')
            g['title'] = request.form.get('title')
            g['description'] = request.form.get('description')
            g['cost'] = request.form.get('cost')
            g['release_date'] = request.form.get('release_date')
            g['publisher_id'] = request.form.get('publisher_id')
            g['language_id'] = request.form.get('language_id')
            g['genres'] = request.form.getlist('genres')
            g['platforms'] = request.form.getlist('platforms')
            
            g['image_path'] = ''
            if 'image_path' in request.files:
                file = request.files['image_path']
                if file and file.filename != '':
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    g['image_path'] = file.filename

            print(g)

            conn.save_game(g)

        except Exception as e:
            print(f"Error saving game: {e}")

    games = conn.get_games_list()
    genres = conn.get_genre_list()
    platforms = conn.get_platform_list()
    languages = conn.get_language_list()
    publishers = conn.get_publisher_list()

    g = {}

    return render_template('admin.html', games=games, genres=genres, platforms=platforms, languages=languages, publishers=publishers, game=g)

if __name__ == "__main__":
    app.run(port=8080, debug=True)