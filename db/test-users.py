#!/bin/python3

import base64
from passlib.hash import pbkdf2_sha256 as pwhash
import random
import sys

import psycopg

def add_test_accounts(cur):
	accounts = [(f'tester{k}', base64.b64encode(random.randbytes(6)).decode('ascii')) for k in range(1, 100)]
	cur.executemany('insert into Kvantland.Student (login, password) values (%s, %s)', [(login,  pwhash.hash(password)) for login, password in accounts])
	with open('testers.txt', 'w') as f:
		for login, password in accounts:
			f.write(f'{login}\t{password}\n')

db = 'postgres://kvantland:quant@127.0.0.1'
if len(sys.argv) > 1:
	db = sys.argv[1]
with psycopg.connect(db) as con:
	with con.transaction():
		with con.cursor() as cur:
			add_test_accounts(cur)
