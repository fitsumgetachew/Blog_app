import sqlite3
import click
from flask.cli import with_appcontext
from flask import  current_app , g
import mysql.connector

def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #             current_app.config['DATABASE'] ,
        #             detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory =sqlite3.Row
        g.db = mysql.connector.connect(
            host='localhost' ,
            user='root',
            database='flaskr',
            password = 'fitsum_new'
        )
        g.db.row_factor = mysql.connector.Row

    return g.db

def close_db(e = None):
    db = g.pop('db' , None)

    if db is not None:
        db.close()

def init_db(app):

    with app.app_context():
        db = get_db()
        # result = db.execute(
        #     "SELECT name FROM sqlite_master WHERE type='table' AND name='user';"
        # ).fetchone()
        #
        # if result is None:
        #     with current_app.open_resource('schema.sql') as f:
        #         db.executescript(f.read().decode('utf8'))
        # else:
        #     pass
        #
        # result = db.execute(
        #     "SELECT name FROM sqlite_master WHERE type='table' AND name='post';"
        # ).fetchone()
        #
        # if result is None:
        #     with current_app.open_resource('schema.sql') as f:
        #         db.executescript(f.read().decode('utf8'))
        # else:
        #     pass
        cursor = db.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'user'"
        )
        result = cursor.fetchone()[0]
        if not result:
            with current_app.open_resource('schema.sql') as f:
                cursor.execute(f.read().decode('utf8'))

        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'post'"
        )
        result = cursor.fetchone()[0]
        if not result:
            with current_app.open_resource('schema.sql') as f:
                cursor.execute(f.read().decode('utf8'))

        cursor.close()



@click.command('init-db')
@with_appcontext
def init_db_command():
        #init_db(app)
        click.echo("Initialized the database")


#Register with the application

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)