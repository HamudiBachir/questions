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
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')
   
if __name__ == '__main__':
   app.run()
