from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getclient")
def getclient():
    return [1,2,3,4,8]

app.run()

