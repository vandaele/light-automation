import functools

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


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

@app.route('/leds/<int:id>', methods=['PUT'])
@modbus_decorator
def leds(id):
    value = str2bool(request.data)
    c.write(id, value)
    return Response('OK',status=200)


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
        app.run(host='0.0.0.0',port=3001)
    except (KeyboardInterrupt, SystemExit):
        # interrupting this script sets all panels to off
        c.clear_all()
        c.close()