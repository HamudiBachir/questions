#------------------------------------------------

#name: questions
#info: bau einer website mit flask
#version: 0.1
#devs: furkan adigüzel, muhammad el bahir, kâan turan

#notes:
#       flask run - startet website

#------------------------------------------------


from flask import Flask, session, render_template, request, g
import sqlite3
import db
import os


#templates = ordner für html files
#static_folder = ordner für css files
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')


#========================[ ALLES DATENBANK RELEVANTE AB HIER ]=============================
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment', #private key
    DATABASE=os.path.join(app.instance_path, 'todos.sqlite')
)
app.cli.add_command(db.init)
app.teardown_appcontext(db.close)

#------------------- hier wird halt etwas in die datenbank eingefügt und rausgenommen ---
@app.route('/insert/sample')
def insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'




#========================[ SEITEN REDIRECTION BEGINNT AB HIER ]=============================
#path zur index seite (mainpage)
@app.route('/')
def index():
   return render_template('index.html') #muss bei templates untergeordnet sein

#path zur zweiten seite
@app.route('/test/')
def test():
   return render_template('index2.html')


###################################### auch dass datenbank zeug ############
@app.route('/lists')
def get_lists():
    sql_query = 'SELECT * from list ORDER BY name'
    db_con = db.get()
    lists_temp = db_con.execute(sql_query).fetchall()
    lists = []
    for list_temp in lists_temp:
        list = {}
        for key in list_temp.keys():
            list[key] = list_temp[key]
        sql_query = (
            'SELECT COUNT(complete) = SUM(complete) '
            'AS complete FROM todo '
            f'JOIN todo_list ON list_id={list["id"]} '
                'AND todo_id=todo.id; '
        )
        complete = db_con.execute(sql_query).fetchone()['complete']
        list['complete'] = complete
        lists.append(list)
    return render_template('lists.html', lists=lists)

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    sql_query_1 = f'SELECT name FROM list WHERE id={list_id}'
    sql_query_2 = (
        'SELECT id, complete, description FROM todo '
        f'JOIN todo_list ON todo_id=todo.id AND list_id={list_id} '
        'ORDER BY id;'
    )

    db_con = db.get()
    list_name = db_con.execute(sql_query_1).fetchone()['name']
    todos = db_con.execute(sql_query_2).fetchall()
    return render_template(
        'todos.html', list_name=list_name, todos=todos)


#ist wichtig damit das programm als standalone läuft (check), wenn nicht könnte zu fehlern führen
if __name__ == '__main__':
   app.run(debug=True)
