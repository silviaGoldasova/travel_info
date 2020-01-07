from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world1():
    return 'Hello World! - /'


@app.route('/home')
def hello_world2():
    return 'Hello World! - Home'

if __name__ == '__main__':
    app.run()
