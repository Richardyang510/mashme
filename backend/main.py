from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/smooth-test')
def smooth_test():
    urls = ['http://34.117.53.148/Smooth_133_5.mp3', 'http://34.117.53.148/Smooth_100_11.mp3']
    return ','.join(urls)

app.run()