import sqlite3
import click
from flask.cli import with_appcontext
from flask import  current_app , g
import MySQLdb

def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #             current_app.config['DATABASE'] ,
        #             detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory =sqlite3.Row
        g.db = MySQLdb.connect(
            host = current_app.config['MYSQL_HOST'],
            user = current_app.config['MYSQL_USER'] ,
            password = current_app.config['MYSQL_PASSWORD'],
            database = current_app.config['MYSQL_DB']
        )


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
        cursor.execute("SHOW TABLES LIKE 'user'")
        result = cursor.fetchone()

        if not result:
            with current_app.open_resource('schema.sql') as f:
                cursor.execute(f.read().decode('utf8'))
            db.commit()

        cursor.execute("SHOW TABLES LIKE 'post'")
        result = cursor.fetchone()

        if not result:
            with current_app.open_resource('schema.sql') as f:
                cursor.execute(f.read().decode('utf8'))
            db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
        #init_db(app)
        click.echo("Initialized the database")


#Register with the application

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)