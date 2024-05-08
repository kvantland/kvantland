#!/usr/bin/python3

from pathlib import Path
from bottle import route, run, static_file, install, response, request

import db
import nav
import land, town, problem, login, loginvk, registration, acc, start_page, pw_recovery, policy, icon
from config import config, ROOT

install(db.Plugin(url=config['db']['url']))
run(**config['server'])
