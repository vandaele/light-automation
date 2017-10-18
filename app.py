import functools
import json
import threading

from flask import Flask, Response, abort, g
from flask import request
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler

from utils import random6

app = Flask('simple API for the modbus light automaton')

from automaton_client import AutomatonClient

c = AutomatonClient()
socketio = SocketIO(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def modbus_decorator(func):
    @functools.wraps(func)
    def _wrap(*args,**kwargs):
        if not c.is_open():
            if not c.open():
                print("unable to connect to %s:%s" % (c.host(), c.port()))
        if c.is_open():
            return func(*args,**kwargs)
        return abort(500)

        c.close()
    return _wrap

@modbus_decorator
def do_leds_put_all(values):
    for id, value in enumerate(values):
        ivalue = int(value)
        if not c.write(id, ivalue):
            return Response('cant change led panel %u, data %s' % (id, value))
    socketio.emit('leds', {'data': json.dumps({id:value for id, value in enumerate(values)})})
    return Response('OK, led panels to %s' % (values), status=200)


def task_loop_random():
    random_values = random6()
    do_leds_put_all(random_values)


@app.route('/leds/<int:id>', methods=['PUT'])
@modbus_decorator
def leds(id):
    value = int(request.data)
    if c.write(id, value):
        socketio.emit('leds',{'data':json.dumps(dict(id=value))})
        return Response('OK, led panel %u to %s' % (id, value),status=200)
    else:
        return Response('cant change led panel %u, data %s' % (id, request.data))


@app.route('/leds', methods=['PUT'])
def leds_put_all():
    values = json.loads(request.data)
    return do_leds_put_all(values)


@app.route('/leds/<int:id>', methods=['GET'])
@modbus_decorator
def leds_read(id):
    def generate():
        while True:
            yield c.read(id)

    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (c.host(), c.port()))
    if c.is_open():
        return Response(generate(),status=200)
    return abort(500)


@app.route('/leds', methods=['GET'])
@modbus_decorator
def leds_read_all():
    return Response(json.dumps(c.read_all()),status=200)


LOOP_RANDOM_INTERVAL = 5

job = {
    'id': 'loop_random',
    'func': 'app:task_loop_random',
    'trigger': 'interval',
    'seconds': LOOP_RANDOM_INTERVAL
}

SCHEDULER_API_ENABLED = True

@app.route('/loop_random/start', methods=['POST'])
@modbus_decorator
def loop_random_start():
    if scheduler.get_job('loop_random') is not None:
        return 'Already started', 304
    else:
        scheduler.add_job(**job)
        return Response('OK', status=200)


@app.route('/loop_random/stop', methods=['POST'])
@modbus_decorator
def loop_random_stop():
    if scheduler.get_job('loop_random') is not None:
        scheduler.delete_job('loop_random')
        return Response('OK', status=200)
    else:
        return Response('No loop_random to stop', status=304)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0',port=3001, debug=True)
    except (KeyboardInterrupt, SystemExit):
        # interrupting this script sets all panels to off
        c.clear_all()
        c.close()