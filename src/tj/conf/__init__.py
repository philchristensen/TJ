# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
JSON configuration file support.
"""

import sys, os.path
import pkg_resources as pkg

import simplejson

DEFAULT_CONF_PATH = '/etc/tjbot.json'

config = None

def load(path=DEFAULT_CONF_PATH):
	global config
	if(config):
		return config
	config = read_config(path)
	return config

def get(key):
	c = load()
	return c[key]

def read_config(path):
	result = {}

	with pkg.resource_stream('tj.conf', 'default.json') as f:
		result.update(_read_config(f))

	if(pkg.resource_exists('tj.conf', 'local.json')):
		print >>sys.stderr, "Loading local.json configuration..."
		with pkg.resource_stream('tj.conf', 'local.json') as f:
			result.update(_read_config(f))

	if(os.path.exists(path)):
		print >>sys.stderr, "Loading %s configuration..." % path
		with open(path) as f:
			result.update(_read_config(f))

	return result

def _read_config(f):
	with f:
		try:
			c = simplejson.load(f)
		except Exception, e:
			raise SyntaxError('%s: %s' % (f, e))
		if(not isinstance(c, dict)):
			raise SyntaxError("%s doesn't contain a single top-level object." % path)
		return c
