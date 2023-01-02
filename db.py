import click
import os
import sqlite3
from flask import current_app, g


def get(pragma_foreign_keys = True): #stellt verbindung mit der datenbank her
    if 'db_con' not in g:
        g.db_con = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db_con.row_factory = sqlite3.Row
    
        if pragma_foreign_keys:
            g.db_con.execute('PRAGMA foreign_keys = ON;')
    return g.db_con


def close(e=None): #trennt die verbindung mit der datenbank
    db_con = g.pop('db_con', None)

    if db_con is not None:
        db_con.close()

@click.command('db-init')
def init():
    try:
        os.makedirs(current_app.instance_path)
    except OSError:
        pass

    db_con = get(False)
    with current_app.open_resource('sql/drop_tables.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    close()
    db_con = get()
    with current_app.open_resource('sql/create_tables.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    click.echo('Database has been initialized.')


#dass was eingefügt wird in die datenbank ist auch bei app.py da
def insert_sample():
    db = get()
    with current_app.open_resource('sql/insert_sample.sql') as f:
        db.executescript(f.read().decode('utf8'))