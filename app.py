
from flask import Flask
app = Flask(__name__)

appName = "feastwell"

@app.route(f"/{appName}")
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
