# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
Bot plugin interaction.
"""

import sys

from wokkel.xmppim import MessageProtocol, AvailablePresence

from tj import plugins

class BotProtocol(MessageProtocol):
	def connectionMade(self):
		print "Connected!"
		# send initial presence
		self.send(AvailablePresence())
		for p in plugins.iterate():
			if(hasattr(p, 'connected')):
				p.connected(self)
	
	def connectionLost(self, reason):
		print "Disconnected!"
		for p in plugins.iterate():
			if(hasattr(p, 'disconnected')):
				p.disconnected(self, reason)
	
	def onMessage(self, msg):
		if msg["type"] == 'chat' and hasattr(msg, "body"):
			print >>sys.stderr, str(msg.__dict__)
			for p in plugins.iterate():
				if(hasattr(p, 'heard')):
					p.heard(self, msg)
		else:
			print >>sys.stderr, "UNKNOWN MESSAGE: %r" % msg