from bottle import route, static_file
from pathlib import Path

import sys

@route("/favicon.ico")
def display_icon():
	path = "static/design/icons"
	ico_path = Path(__file__).parent / path
	return static_file('logo.svg', root=ico_path)