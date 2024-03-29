# TJ
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
Plugins add bot functionality.
"""

import os, sys

from zope import interface

from twisted import plugin

from tj import conf

__path__ = [os.path.abspath(os.path.join(x, 'tj', 'plugins')) for x in sys.path]

__all__ = []

def iterate():
	import tj.plugins
	for module in plugin.getPlugins(IBotPlugin, tj.plugins):
		if(module.__module__ not in conf.get('active-plugins')):
			continue
		m = module()
		yield m

def get(name):
	import tj.plugins
	for module in plugin.getPlugins(IBotPlugin, tj.plugins):
		if(module.__module__ not in conf.get('active-plugins')):
			continue
		if(name in (module.name, module.__module__)):
			m = module()
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
