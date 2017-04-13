from flask import Flask, render_template, Response, request
import redis

"""Redis host"""
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
# Note that we don't pesist data for now - bring problem
REDIS_DB = 0

"""Flask host"""
FLASK_HOST = '127.0.0.1'
FLASK_PORT = '9999'

app = Flask(__name__)
# app.config['DEBUG'] = True
r = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB)


def event_stream():
    pubsub = r.pubsub()
    pubsub.subscribe('twitterchannel')
    for msg in pubsub.listen():
        # print msg
        yield 'data: %s\n\n' % msg['data']

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/stream')
def data_stream():
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ =='__main__':
    app.run(threaded = True, host = FLASK_HOST, port=FLASK_PORT)