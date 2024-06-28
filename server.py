#!/usr/bin/python3

from pathlib import Path
from bottle import route, run, static_file, install, response, request

import db
import nav
import land, town, problem, login, loginvk, registration, acc, start_page, pw_recovery, policy, icon, approv
from config import config, ROOT

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = config['client']['url']
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'

            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors
    
cfg_static = config.get('static')
if cfg_static:
	@route('/static/<path:path>')
	def static(path: str):
		return static_file(path, root=ROOT / cfg_static['root'])

install(db.Plugin(url=config['db']['url']))
install(EnableCors())
run(**config['server'])
