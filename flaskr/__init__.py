import os
from flask import Flask
from flask_mysqldb import MySQL
import mysql.connector
from flask_login import LoginManager  , UserMixin , current_user


try :
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='fitsum_new',
        database = 'flaskr'
    )
    print("connection successful")

except:
    print("some error")

class User(UserMixin):
    def __init__(self , id , username):
        self.id = id
        self.username = username

    def is_authenticated(self):
        # cursor = mydb.cursor(dictionary=True)
        # cursor.execute('SELECT * FROM user WHERE id= %s' , (self.id , ))
        # user = cursor.fetchone()
        # cursor.close()
        #
        # if user:
        #     return user['username']
        # else:
        #     return False
        return True


    @property
    def is_active(self):
        return True

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
         SECRET_KEY='dev')
    app.config['TESTING'] = False
    app.config.update(
        SECRET_KEY ='fitsum' ,
        TESTING = True ,
        DEBUG = True,
        PROPAGATE_EXCEPTIONS = True,
        TRAP_HTTP_EXCEPTIONS = True ,
        TRAP_BAD_REQUEST_ERRORS = True
    )
    app.config['PERMANENT_SESSION_LIFETIME'] = 5
    app.config['REMEMBER_COOKIE_DURATION']   = 60
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    @login_manager.user_loader
    def load_user(user_id):
        cursor= mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE id = %s ', (user_id ,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return User(user['id'] , user['username'])
        else:
            return None



    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # from . import db
    # db.init_app(app)
    #
    # db.init_db(app)

    from . import auth
    app.register_blueprint(auth.bp)

    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/' , endpoint='index')

    from . import comment
    app.register_blueprint(comment.bp)

    return app

