import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(it, cmd, value):
    res = map(lambda v: v.strip(), it)
    match cmd:
        case 'filter':
            res = filter(lambda v: value in v, res)
        case 'sort':
            value = bool(value)
            res = sorted(res, reverse=value)
        case 'unique':
            res = set(res)
        case 'limit':
            value = int(value)
            res = list(res)[:value]
        case 'map':
            value = int(value)
            res = map(lambda v: v.split(' ')[value], res)
    return res

    # if cmd == 'filter':
    #     res = filter(lambda v: value in v, res)
    # if cmd == 'sort':
    #     value = bool(value)
    #     res = sorted(res, reverse=value)
    # if cmd == 'unique':
    #     res = set(res)
    # if cmd == 'limit':
    #     value = int(value)
    #     res = list(res)[:value]
    # if cmd == 'map':
    #     value = int(value)
    #     res = map(lambda v: v.split(' ')[value], res)
    # return res


@app.route("/perform_query")
def perform_query():
    try:
        cmd1 = request.args['cmd1']
        cmd2 = request.args['cmd2']
        val1 = request.args['value1']
        val2 = request.args['value2']
        file_name = request.args['file_name']
    except KeyError:
        return BadRequest

    path_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        return BadRequest

    with open(path_file) as f:
        res = build_query(f, cmd1, val1)
        res = build_query(res, cmd2, val2)
        res = "\n".join(res)

    return app.response_class(res, content_type="text/plain")
