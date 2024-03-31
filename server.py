#!/usr/bin/python3

from pathlib import Path
from bottle import route, run, static_file, install

import db
import nav
import start_page, policy, icon
from config import config, ROOT

cfg_static = config.get('static')
if cfg_static:
	@route('/static/<path:path>')
	def static(path: str):
		return static_file(path, root=ROOT / cfg_static['root'])

install(db.Plugin(url=config['db']['url']))
run(**config['server'])
