from flask import Flask ,url_for,request , render_template

app = Flask(__name__)
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] and
                       request.form['password']):
            return request.form['username']
        else:
            error = 'Invald username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', name=error)