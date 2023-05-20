from flask import (
                    Blueprint , flash , g , redirect , render_template , request , url_for , get_flashed_messages
)
import datetime
from flaskr.auth import login_required
from flaskr import mydb

bp  = Blueprint('comment' , __name__ , url_prefix='/comment')

@bp.route('/send' , methods = ['GET' , 'POST'])
@login_required
def send():
    cursor = mydb.cursor()
    cursor.execute('SELECT username FROM user;')
    listUsername = cursor.fetchall()
    cursor.close()
    flash_message = ['']
    if request.method == 'POST':
        recieverUsername = request.form['name-select']
        comment = request.form['comment']
        #senderUsername = g.user['id']
        error = None

        if not recieverUsername:
            error = 'Slelect User name '
        elif not comment:
            error = "say something on the comment"

        if error is not None:
            flash(error)

        else:
            cursor = mydb.cursor()

            cursor.execute(
                'INSERT INTO  comment(senderUsername , recieverUsername , message) values (%s , %s,%s )' ,
                (g.user['username'] , recieverUsername , comment)
            )
            mydb.commit()
            cursor.close()
            flash("Successfully Sent" , 'congrate')
            flash_message = get_flashed_messages()
        #return  redirect(url_for('blog.index'))
    return render_template('comment/send.html' ,  listUsername =  listUsername , flash_message = flash_message)

@bp.route('/inbox')
@login_required
def inbox():
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(*) FROM  comment")
    count = cursor.fetchone()[0]
    cursor.close()
    cursor = mydb.cursor(dictionary = True)
    #current_time = datetime.now()

    if count >0 :
        cursor.execute(
            'SELECT senderUsername , message , sent FROM comment WHERE recieverUsername = %s' ,
             [g.user['username']])
        messages = cursor.fetchall()
    else :
        messages = []
    cursor.close()

    return render_template('comment/recieved.html' ,  messages = messages , datetime = datetime)
