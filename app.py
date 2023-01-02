#------------------------------------------------

#name: questions
#info: bau einer website mit flask
#version: 0.1
#devs: furkan adigüzel, muhammad el bahir, kâan turan

#notes:
#       flask run - startet website

#------------------------------------------------


#import des flask objektes
from flask import Flask, render_template

#templates = ordner für html files
#static_folder = ordner für css files
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')


#========================[ SEITEN REDIRECTION BEGINNT AB HIER ]=============================
#path zur index seite (mainpage)
@app.route('/')
def index():
   return render_template('index.html') #muss bei templates untergeordnet sein

#path zur zweiten seite
@app.route('/test/')
def test():
   return render_template('index2.html')


#ist wichtig damit das programm als standalone läuft (check), wenn nicht könnte zu fehlern führen
if __name__ == '__main__':
   app.run(debug=True)
