import functools
from flask import \
    (Blueprint , flash , g , redirect , render_template ,request , session , url_for
     )
from werkzeug.security import check_password_hash , generate_password_hash
from flaskr.db import get_db
from flaskr import mydb
from mysql.connector.errors import IntegrityError


bp = Blueprint('auth' , __name__ , url_prefix='/auth')

@bp.route('/register' , methods = ('GET' , 'POST'))
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #db = get_db()
        cursor = mydb.cursor()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error= 'Password is required'

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO user(username , password)  VALUES (%s , %s)" ,
                    (username , generate_password_hash(password))
                )
                mydb.commit()

            except IntegrityError:
                error = f"User {username} is already taken"

            else:
                return  redirect(url_for("auth.login"))
        cursor.close()
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login' , methods= ('GET' , 'POST'))
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #db = get_db()
        cursor = mydb.cursor(dictionary=True)
        error = None

        cursor.execute(
            'SELECT * FROM  user WHERE username = %s' , (username , )
        )
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            error = 'Incorrect username. '

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Password . '

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user =None
    else:
        #db = get_db()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM user WHERE  id = %s' , (user_id ,)
        )
        g.user = cursor.fetchone()
        cursor.close()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view