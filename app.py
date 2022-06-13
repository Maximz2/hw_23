import os
import re
from typing import Iterator

from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def slice_limit(it: Iterator, value: int) -> Iterator:
    i = 0
    for item in it:
        if i < value:
            yield item
        else:
            break
        i += 1


def build_query(it: Iterator, cmd: str, value: str) -> Iterator:
    res = map(lambda v: v.strip(), it)
    match cmd:
        case 'filter':
            return filter(lambda v: value in v, res)
        case 'sort':
            return iter(sorted(res, reverse=bool(value)))
        case 'unique':
            return iter(set(res))
        case 'limit':
            return slice_limit(res, int(value))
        case 'map':
            return map(lambda v: v.split(' ')[int(value)], res)
        case 'regex':
            regex = re.compile(value)
            return filter(lambda x: regex.search(x), res)
    return res


@app.route("/perform_query", methods=['POST'])
def perform_query() -> Response:
    try:
        cmd1 = request.args['cmd1']
        cmd2 = request.args['cmd2']
        val1 = request.args['value1']
        val2 = request.args['value2']
        file_name = request.args['file_name']
    except KeyError:
        raise BadRequest

    path_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        raise BadRequest

    with open(path_file) as f:
        res = build_query(f, cmd1, val1)
        res = build_query(res, cmd2, val2)
        content = "\n".join(res)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run()
