from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    #make the server publicly by adding --host=0.0.0.0
    return "<h1>Runing publicly</h1>"
