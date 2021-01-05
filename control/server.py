#! /home/pi/.pyenv/shims/python

from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
import subprocess
from database import Database
import logging

db = Database()

app = Flask(__name__)
CORS(app)
log = logging.getLogger('control-server')
logging.basicConfig(filename='/home/pi/logs/server.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    encoding='utf-8', level=logging.INFO)


@app.route("/api")
def home():
    return "Hello from the raspberry pi"


def serve_props():
    kv_tuple = db.get_all()
    kv = {}
    [kv.update({k: v}) for k, v in kv_tuple]

    return jsonify(kv)


def restart_main_loop():
    subprocess.call(
        ['sh', '/home/pi/raspi-room-control/control/restart_main.sh'])


def save_props(data):
    for k in data:
        db.set(k, data[k])
    log.info('saved data: {}'.format(data))
    restart_main_loop()
    return jsonify(data)


@app.route("/api/logs")
def logs():
    server_log = open('/home/pi/logs/server.log').read()
    control_log = open('/home/pi/logs/control.log').read()

    return {
        "server_log": server_log,
        'control_log': control_log
    }


@app.route("/api/props", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return save_props(request.json)

    return serve_props()


if __name__ == "__main__":

    port = 5000
    log.info('[started] server listening on {}'.format(port))
    serve(app, host="0.0.0.0", port=port, url_scheme='http', threads=6)
