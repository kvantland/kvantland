#!/usr/bin/python3
import io

import http
import http.server
import socketserver
import pathlib
import os
import copy
import urllib
import sys
import select

PORT = 8000

class HTTPError(Exception):
	def __init__(self, code: http.HTTPStatus, text: str | None = None, /):
		self.code = http.HTTPStatus(code)
		self.message = text

	def __str__(self):
		return f'HTTP {self.code} {self.code.phrase}'

class Server(socketserver.TCPServer):
	server_name = "Me!"
	server_port = PORT
	allow_reuse_address = True

class Handler(http.server.CGIHTTPRequestHandler):
	cgi_directories = ['']

	def do_GET(self):
		try:
			self.run_cgi()
		except HTTPError:
			super().do_GET()

	def do_POST(self):
		try:
			self.run_cgi()
		except HTTPError as e:
			self.send_error(e.code, e.text)

	def run_cgi(self):
		path = self.path
		dir, rest = '', path
		i = path.find('/', len(dir) + 1)
		while i >= 0:
			nextdir = path[:i]
			nextrest = path[i+1:]

			scriptdir = self.translate_path(nextdir)
			if os.path.isdir(scriptdir):
				dir, rest = nextdir, nextrest
				i = path.find('/', len(dir) + 1)
			else:
				break

		# find an explicit query string, if present.
		rest, _, query = rest.partition('?')

		# dissect the part after the directory name into a script name &
		# a possible additional path, to be stored in PATH_INFO.
		i = rest.find('/')
		if i >= 0:
			script, rest = rest[:i], rest[i:]
		else:
			script, rest = rest, ''

		scriptname = dir + '/' + script
		scriptfile = self.translate_path(scriptname)
		if not os.path.exists(scriptfile):
			raise HTTPError(
				http.HTTPStatus.NOT_FOUND,
				"No such CGI script (%r)" % scriptname)
		if not os.path.isfile(scriptfile):
			raise HTTPError(
				http.HTTPStatus.FORBIDDEN,
				"CGI script is not a plain file (%r)" % scriptname)
		ispy = self.is_python(scriptname)
		if self.have_fork or not ispy:
			if not self.is_executable(scriptfile):
				raise HTTPError(
					http.HTTPStatus.FORBIDDEN,
					"CGI script is not executable (%r)" % scriptname)

		# Reference: http://hoohoo.ncsa.uiuc.edu/cgi/env.html
		# XXX Much of the following could be prepared ahead of time!
		env = copy.deepcopy(os.environ)
		env['SERVER_SOFTWARE'] = self.version_string()
		env['SERVER_NAME'] = self.server.server_name
		env['GATEWAY_INTERFACE'] = 'CGI/1.1'
		env['SERVER_PROTOCOL'] = self.protocol_version
		env['SERVER_PORT'] = str(self.server.server_port)
		env['REQUEST_METHOD'] = self.command
		uqrest = urllib.parse.unquote(rest)
		env['PATH_INFO'] = uqrest
		env['PATH_TRANSLATED'] = self.translate_path(uqrest)
		env['SCRIPT_NAME'] = scriptname
		env['QUERY_STRING'] = query
		env['REMOTE_ADDR'] = self.client_address[0]
		authorization = self.headers.get("authorization")
		if authorization:
			authorization = authorization.split()
			if len(authorization) == 2:
				import base64, binascii
				env['AUTH_TYPE'] = authorization[0]
				if authorization[0].lower() == "basic":
					try:
						authorization = authorization[1].encode('ascii')
						authorization = base64.decodebytes(authorization).\
										decode('ascii')
					except (binascii.Error, UnicodeError):
						pass
					else:
						authorization = authorization.split(':')
						if len(authorization) == 2:
							env['REMOTE_USER'] = authorization[0]
		# XXX REMOTE_IDENT
		if self.headers.get('content-type') is None:
			env['CONTENT_TYPE'] = self.headers.get_content_type()
		else:
			env['CONTENT_TYPE'] = self.headers['content-type']
		length = self.headers.get('content-length')
		if length:
			env['CONTENT_LENGTH'] = length
		referer = self.headers.get('referer')
		if referer:
			env['HTTP_REFERER'] = referer
		accept = self.headers.get_all('accept', ())
		env['HTTP_ACCEPT'] = ','.join(accept)
		ua = self.headers.get('user-agent')
		if ua:
			env['HTTP_USER_AGENT'] = ua
		co = filter(None, self.headers.get_all('cookie', []))
		cookie_str = ', '.join(co)
		if cookie_str:
			env['HTTP_COOKIE'] = cookie_str
		# XXX Other HTTP_* headers
		# Since we're setting the env in the parent, provide empty
		# values to override previously set values
		for k in ('QUERY_STRING', 'REMOTE_HOST', 'CONTENT_LENGTH',
				  'HTTP_USER_AGENT', 'HTTP_COOKIE', 'HTTP_REFERER'):
			env.setdefault(k, "")

		decoded_query = query.replace('+', ' ')

		import subprocess
		cmdline = [scriptfile]
		if self.is_python(scriptfile):
			interp = sys.executable
			if interp.lower().endswith("w.exe"):
			# On Windows, use python.exe, not pythonw.exe
				interp = interp[:-5] + interp[-4:]
			cmdline = [interp, '-u'] + cmdline
		if '=' not in query:
			cmdline.append(query)
		self.log_message("command: %s", subprocess.list2cmdline(cmdline))
		try:
			nbytes = int(length)
		except (TypeError, ValueError):
			nbytes = 0
		p = subprocess.Popen(cmdline,
					stdin=subprocess.PIPE,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE,
					env = env
					)
		if self.command.lower() == "post" and nbytes > 0:
			data = self.rfile.read(nbytes)
		else:
			data = None
		# throw away additional data [see bug #427345]
		while select.select([self.rfile._sock], [], [], 0)[0]:
			if not self.rfile._sock.recv(1):
				break
		stdout, stderr = p.communicate(data)
		out = io.BytesIO(stdout)
		status = http.HTTPStatus.OK, "Script output follows"
		headers = {}
		while True:
			headline = out.readline().strip()
			if not headline:
				break
			key, value = headline.split(b':')
			value = value.strip()
			if key.lower() == b'status':
				status = value.split(maxsplit=1)
				status[0] = http.HTTPStatus(int(status[0]))
				continue
			headers[key] = value

		self.send_response(*status)
		for key, value in headers.items():
			self.send_header(key.decode('ascii'), value.decode('ascii'))
		self.end_headers()
		self.wfile.write(out.read())
		if stderr:
			self.log_error('%s', stderr)
		p.stderr.close()
		p.stdout.close()
		status = p.returncode
		if status:
			self.log_error("CGI script exit status %#x", status)
		else:
			self.log_message("CGI script exited OK")

with Server(("127.0.0.1", PORT), Handler) as httpd:
	print("serving at port", PORT)
	httpd.serve_forever()
