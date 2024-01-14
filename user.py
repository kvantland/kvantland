#!/usr/bin/python3
from html import escape
from urllib.parse import quote
from bottle import route, request, response, redirect

def display_banner():
	yield '<nav class="user_nav">'
	yield '<ul class="flex_ul">'
	yield f'<li><a href="/rules">Правила</a>'
	yield '</ul>'
	yield '</nav>'
