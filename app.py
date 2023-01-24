# name: questions
# info: bau einer website mit flask
# version: 0.1
# author: furkan adigüzel, muhammad el bahir, kâan turan
#
# overview:
#   templates = ordner für html files
#   staticFiles = ordner für css files
#
# info:
#   shift, strg, p -> sqlite
#
#



#import
from flask import Flask, session, render_template, request, url_for, flash, redirect, abort
import sqlite3
import os


#dicrectory where the sqlite data gets saved
currentdirectory = os.path.dirname(os.path.abspath(__file__))

#add folders
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
app.config['SECRET_KEY'] = 'your secret key'


#path to index page (mainpage)
def get_db_connection(): #verbindung zur datenbank herstellen
    conn = sqlite3.connect('database.db') #datenbank datei
    conn.row_factory = sqlite3.Row #gibt daten aus der datenbank wieder
    return conn

#Abrufen von Informationen aus der datenbank
def get_post(post_id):
    conn = get_db_connection() #Verbindung zur Datenbank herstellen
    
    #method returns a single record or None if no more rows are available.
    #gibt aus der tabelle "posts" nur eine reihe mit der id = x
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close() #verbindung trennen

    if post is None: #wenn es keinen eintrag unter "id -> x" gibt dann bricht er es ab
        abort(404)

    return post #falls ja dann gib folgenden post wieder


@app.route('/') #/ -> main page
def index():
    conn = get_db_connection() #datenbankverbindung herstellen

    #fetches all the rows of a query result. It returns all the rows as a list of tuples. An empty list is returned if there is no record to fetch.
    #gibt alle werte aus der tabelle posts wieder
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close() #db verbindung trennen

    #index.html rendern, posts=posts heißt alle spalten und reihen aus der tabelle "posts" in der datenbank zur verfügung stellen
    return render_template('index.html', posts=posts)


@app.route('/create/', methods=('GET', 'POST')) #werte zur datenbank hinzufügen
def create():
    if request.method == 'POST': #wenn gewählte methode hinzufügen

        title = request.form['title'] #werte die hinzugefügt werden
        content = request.form['content']

        if not title: #wenn nichts bei title eingegeben wurde
            flash('Title is required!')
        elif not content: #wenn nichts bei content eingesetzt wurde
            flash('Content is required!')
        else: #wenn alles ausgefüllt wurde (in alle felder wurde etwas reingeschrieben)
            conn = get_db_connection()

            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content)) #werte der datenbank hinzufügen
            
            conn.commit()
            conn.close()

            return redirect(url_for('index')) #weiterleitung an url

    return render_template('create.html')

#mehr oder weniger das gleiche wie oben
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',)) #löschung von daten aus der datenbank
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


#if this (__name__) file is a main-file, run it
if __name__ == '__main__':
   app.run()
