#!/bin/python3

# Automatically set that last four tournaments are of current seasons. Use only for dev.

import base64
import sys
import psycopg

import os
import sys
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)
from config import config

current_tournament = config['tournament']['version']
current_season = config['tournament']['season']

db = 'postgres://kvantland:quant@127.0.0.1'
if len(sys.argv) > 1:
	db = sys.argv[1]
with psycopg.connect(db) as con:
	with con.transaction():
		with con.cursor() as cur:
			for tournament_diff in range(min(4, current_tournament)):
				tournament = current_tournament - tournament_diff
				cur.execute('insert into Kvantland.Season values(%s, %s)', (current_season, tournament))
