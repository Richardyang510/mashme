from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/smooth-test')
def smooth_test():
    urls = [
        'https://storage.googleapis.com/download/storage/v1/b/dropdowns-stems/o/Smooth_133_5.mp3?alt=media',
        'https://storage.googleapis.com/download/storage/v1/b/dropdowns-stems/o/Smooth_100_11.mp3?alt=media'
    ]
    return ','.join(urls)

@app.route('/mix/<query>', methods=['POST'])
def mix(query):
    print("The user has entered: " + query)
    return 'hello'

@app.route('/cached-songs')
def getCachedSongs():
    pass


app.run()