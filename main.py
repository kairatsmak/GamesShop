import os
from flask import Flask, request, render_template, redirect
from services import Connection

app: Flask = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
conn: Connection = Connection()

dicts: dict = conn.get_dicts()

@app.route("/", methods=['GET'])
def index():
    """ Main page """
    global dicts
    
    games = conn.get_games_list()

    search = {}
    search['title'] = request.args.get('title') if request.args.get('title') else ''
    search['platforms'] = request.args.getlist('platforms') if request.args.getlist('platforms') else []
    search['publishers'] = request.args.getlist('publishers') if request.args.getlist('publishers') else []
    search['languages'] = request.args.getlist('languages') if request.args.getlist else []
    search['genres'] = request.args.getlist('genres') if request.args.getlist('genres') else []

    find_games = []
    
    for game in games:
        fl = True
         
        if search['title'] and game['title'].lower().find(search['title'].lower()) == -1:
            fl = False

        if search['platforms']:
            for item in game['platforms']:
                if item in search['platforms']:
                    break
            else:    
                fl = False
        
        if search['genres']:
            for item in game['genres']:
                if item in search['genres']:
                    break
            else:    
                fl = False

        if search['publishers'] and game['publisher'] not in search['publishers']:
            fl = False

        if search['languages'] and game['language'] not in search['languages']:
            fl = False

        if fl:
            find_games.append(game)


    return render_template('index.html', 
        games=find_games, 
        genres=dicts['genres'], 
        platforms=dicts['platforms'], 
        languages=dicts['languages'], 
        publishers=dicts['publishers'], 
        search=search
    )

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    """ Admin page """
    global dicts

    if request.method == 'POST':
        try:
            g = {}
            
            g['id'] = request.form.get('id')
            g['title'] = request.form.get('title')
            g['description'] = request.form.get('description')
            g['cost'] = request.form.get('cost')
            g['release_date'] = request.form.get('release_date')
            g['publisher_id'] = request.form.get('publisher_id')
            g['language_id'] = request.form.get('language_id')
            g['genres'] = request.form.getlist('genres')
            g['platforms'] = request.form.getlist('platforms')
            
            g['image_path'] = request.form.get('image_path_default')
            if 'image_path' in request.files:
                file = request.files['image_path']
                if file and file.filename != '':
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    g['image_path'] = file.filename

            conn.save_game(g)

        except Exception as e:
            print(f"Error saving game: {e}")

    games = conn.get_games_list()
    
    g = {}

    return render_template('admin.html', 
        games=games, 
        genres=dicts['genres'], 
        platforms=dicts['platforms'], 
        languages=dicts['languages'], 
        publishers=dicts['publishers'], 
        game=g
    )

@app.route("/admin/delete/<int:id>")
def delete_game(id: int):
    conn.delete_game(id)

    return redirect("/admin")

@app.route("/admin/get/<int:id>")
def get_game(id: int):
    global dicts

    g = conn.get_game(id)

    games = conn.get_games_list()

    return render_template('admin.html', 
        games=games, 
        genres=dicts['genres'], 
        platforms=dicts['platforms'], 
        languages=dicts['languages'], 
        publishers=dicts['publishers'], 
        game=g
    )

if __name__ == "__main__":
    app.run(port=8080, debug=True)