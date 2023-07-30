#!/usr/bin/python3

from pathlib import Path
from bottle import route, run, static_file, install

import db
import land, town, problem

STATIC_ROOT = Path(__file__).parent / 'static'

@route('/static/<path:path>')
def static(path: str):
	return static_file(path, root=STATIC_ROOT)

install(db.Plugin(url='postgres://kvantland:quant@127.0.0.1'))
run(host='localhost', port=8080, debug=True, reloader=True)
