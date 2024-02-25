#!/usr/bin/python3

from html import escape

def display_breadcrumbs(*path):
	yield '<nav class="breadcrumbs">'
	for url, name in path:
		yield f'<a href="{url}">{escape(name)}</a>'
		yield '<div class="between">'
		yield '<img src="/static/design/icons/breadcrumbs.svg" />'
		yield '<img src="/static/design/icons/breadcrumbs.svg" />'
		yield '</div>'
	yield '</nav>'
