#man muss bevor man flask run macht,
#in den ordner über cd gehen, also in den webapp ordner unten in der konsole
from flask import Flask, redirect, url_for

app = Flask(__name__)
@app.route('/')



def index():
    return redirect(url_for('foo_function'))
@app.route('/fowo') #link erweiterung

def foo_function():
    return 'Hellolljdjndqkw'
@app.route('/bar')

def bar_function():
    return redirect('/foo') # Not recommended to give redirect() a hard-coded UR

