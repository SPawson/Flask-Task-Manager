import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World ... again' #test file


if __name__ == '__main__':
    host = os.environ.get('IP')
    port = int(os.environ.get('PORT'))

    app.run(host = host, port = port, debug=True)