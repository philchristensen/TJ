# antioch
# Copyright (c) 1999-2010 Phil Christensen
#
#
# See LICENSE for details

"""
Plugins add bot functionality.
"""

import os, sys

from zope import interface

from twisted import plugin

__path__ = [os.path.abspath(os.path.join(x, 'tj', 'plugins')) for x in sys.path]

__all__ = []

def iterate():
	import tj.plugins
	for module in plugin.getPlugins(IBotPlugin, tj.plugins):
		m = module()
		print m
		yield m

def get(name):
	import tj.plugins
	for module in plugin.getPlugins(IBotPlugin, tj.plugins):
		if(module.name == name):
			m = module()
			print m
			return m
	return None

class IBotPlugin(interface.Interface):
	name = interface.Attribute('Name of this plugin.')
	
	def connected(self, protocol):
		"""
		The bot has connected to the server.
		"""
	
	def disconnected(self, protocol, reason):
		"""
		The bot has disconnected from the server.
		"""
	
	def heard(self, protocol, data):
		"""
		The bot heard something.
		"""
	
	def joined(self, protocol, data):
		"""
		Someone joined one of the bot's channels.
		"""
	
	def left(self, protocol, data):
		"""
		Someone left one of the bot's channels.
		"""
