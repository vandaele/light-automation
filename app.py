import functools
import json

from flask import Flask, Response, abort
from flask import request

app = Flask('simple API for the modbus light automaton')

from automaton_client import AutomatonClient

c = AutomatonClient()


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



@app.route('/leds/<int:id>', methods=['PUT'])
@modbus_decorator
def leds(id):
    value = int(request.data)
    if c.write(id, value):
        return Response('OK, led panel %u to %s' % (id, value),status=200)
    else:
        return Response('cant change led panel %u, data %s' % (id, request.data))


@app.route('/leds', methods=['PUT'])
@modbus_decorator
def leds_put_all():
    values = json.loads(request.data)
    for id, jvalue in enumerate(values):
        value = int(jvalue)
        if not c.write(id, value):
            return Response('cant change led panel %u, data %s' % (id, jvalue))
    return Response('OK, led panels to %s' % (values), status=200)


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


@app.route('/leds_random', methods=['POST'])
@modbus_decorator
def leds_random():
    if c.set_random():
        return Response('OK, set_random',status=200)
    else:
        return Response('cant change led panel set_random' % (id, request.data))


@app.route('/loop_write/start', methods=['POST'])
@modbus_decorator
def loop_write_start():
    pass


@app.route('/loop_write/stop', methods=['POST'])
@modbus_decorator
def loop_write_stop():
    pass

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0',port=3001, debug=True)
    except (KeyboardInterrupt, SystemExit):
        # interrupting this script sets all panels to off
        c.clear_all()
        c.close()