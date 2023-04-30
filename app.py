from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    #running with debug mode on by giving some error by ading  --debug
    return "<h1>Running with debug on </h1>" + name
