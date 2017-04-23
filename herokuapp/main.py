#!/usr/bin/env python

import bottle
from bottle import Bottle
from copycat import Copycat, Reporter
import gevent
from gevent import monkey
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError
import json
import os
import time


monkey.patch_all()
app = Bottle()


class TimeLimitExceeded(Exception):
    pass


class HerokuReporter(Reporter):
    def __init__(self, ws, time_limit_in_seconds):
        self.ws = ws
        self.end_time = time.time() + time_limit_in_seconds

    def report_temperature(self, _):
        if time.time() > self.end_time:
            raise TimeLimitExceeded()

    def report_answer(self, answer):
        self.ws.send(json.dumps(answer))
        message = 'I thought of a possible answer: "%s" (temperature %.1f)' % (answer['answer'], answer['temp'])
        self.ws.send(json.dumps({
            'message': message,
        }))


@app.get('/robots.txt')
def robots_txt():
    bottle.response.content_type = 'text/plain'
    return 'User-agent: *\nDisallow: /\n'


@app.route('/websocket')
def websocket():
    ws = bottle.request.environ.get('wsgi.websocket')
    if not ws:
        bottle.abort(400, 'Expected WebSocket request')
    try:
        while True:
            message = ws.receive()
            d = json.loads(message)
            copycat = Copycat(reporter=HerokuReporter(ws, 20))
            try:
                copycat.run(
                    d['a'],
                    d['b'],
                    d['c'],
                    10
                )
            except TimeLimitExceeded:
                ws.send(json.dumps({'message': 'Time limit exceeded!'}))
            finally:
                ws.send(json.dumps({'finished': True}))
    except WebSocketError:
        pass


@app.get('/')
@app.get('/index.html')
def home():
    return bottle.static_file('index.html', root='./herokuapp/static', mimetype='text/html')


@app.get('/<filename:path>')
def static(filename):
    return bottle.redirect('/index.html', 302)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    server = gevent.pywsgi.WSGIServer(('0.0.0.0', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
