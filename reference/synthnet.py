#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017 Jef Van den broeck, jef.vdb@gmail.com
import sys
import gevent

PROMPT = 'sweet> '

def hello():
	return "hello"

def connect(where):
	return "no"

commands = {
	'HELLO' : {
		'help': """This is HELLO's help string""",
		'params' : 0,
		'code' : hello,
	},
	'CONNECT' : {
		'help' : """Connect to something else.""",
		'params' : 1,
		'code' : connect,
	}
}

class Parser(object):
	def __init__(self, commands):
		self.commands = commands

	def parse(self, line):
		if not len(line.strip()):
			return ''

		a = line.split()
		opt, optarg = a[0].upper(), a[1:]
		if opt in self.commands:
			command = self.commands[opt]
			if len(optarg) != command['params']:
				return command['help']
			else:
				return command['code'](*optarg)

		return "HMM"

class Context(object):
	def __init__(self, cb_output):
		self.cb_output = cb_output
		self.parser = Parser(commands)
		self.handle('')

	def handle(self, data):
		self.cb_output(self.parser.parse(data) + "\n")
		self.cb_output(PROMPT)

class Connection(object):
	def __init__(self, peer, context, fn_input, cb_output):
		self.peer = peer
		self.context = context(cb_output)
		self.fn_input = fn_input
		self.cb_output = cb_output

	def run(self):
		while True:
			self.context.handle(self.fn_input())

if __name__ == '__main__':
	con = Connection('stdio', Context, sys.stdin.readline, sys.stdout.write)
	gevent.spawn(con.run)
	gevent.joinall([gevent.spawn(con.run)])
