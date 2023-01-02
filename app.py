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

app = Flask(__name__) #hält den namen des python moduls

@app.route('/') #wenn die webpage abgefragt wird dann startet die software von hier

def main():
    return render_template('index.html')


