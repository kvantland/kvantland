#!/usr/bin/python3

from pathlib import Path
from bottle import route, run, static_file, install

try:
	import tomllib
except ImportError:
	import tomli as tomllib

import db
import land, town, problem

ROOT = Path(__file__).parent

with open(ROOT / 'config.toml', 'rb') as f:
	config = tomllib.load(f)

cfg_static = config.get('static')
if cfg_static:
	@route('/static/<path:path>')
	def static(path: str):
		return static_file(path, root=ROOT / cfg_static['root'])

install(db.Plugin(url=config['db']['url']))
run(**config['server'])
