from flask import Flask

app = Flask(__name__)

def get_hello_message():
    return "Hello, World!"

@app.route('/')
def hello_world():
    return get_hello_message()

if __name__ == '__main__':
    app.run(host='0.0.0.0')