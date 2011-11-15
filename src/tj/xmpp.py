# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
Bot plugin interaction.
"""

import sys

from twisted.internet import defer
from twisted.words.protocols.jabber import jid

from wokkel import muc
from wokkel.xmppim import MessageProtocol, AvailablePresence

from tj import plugins

fallback = lambda *a, **kw: None

def plugin(event, *args, **kwargs):
	for p in plugins.iterate():
		if(hasattr(p, event)):
			getattr(p, event, fallback)(*args, **kwargs)

class BotProtocol(MessageProtocol):
	def connectionMade(self):
		print "Connected!"
		# send initial presence
		self.send(AvailablePresence())
		plugin('connected', self)
	
	def connectionLost(self, reason):
		print "Disconnected!"
		plugin('disconnected', self, reason)
	
	def onMessage(self, msg):
		if msg["type"] == 'chat' and hasattr(msg, "body"):
			print >>sys.stderr, str(msg.__dict__)
			plugin('heard', self, msg)
		# else:
		# 	print >>sys.stderr, "UNKNOWN MESSAGE: %s" % msg.__dict__

class MUCBotClient(muc.MUCClient):
	def __init__(self, server, room, nick):
		muc.MUCClient.__init__(self)
		self.server = server
		self.room = room
		self.nick = nick
		self.room_jid = jid.internJID(self.room+'@'+self.server+'/'+self.nick)
		self.last = {}
		self.activity = None
	
	@defer.inlineCallbacks
	def connectionInitialized(self):
		"""
		The bot has connected to the xmpp server, now try to join the room.
		"""
		yield defer.maybeDeferred(muc.MUCClient.connectionInitialized, self)
		print 'initialized'
		room = yield self.join(self.room_jid, self.nick)
		# if int(room.status) == muc.STATUS_CODE_CREATED:
		# 	config_form = yield self.getConfigureForm(self.room_jid.userhost())
		# 	# set config default
		# 	config_result = yield self.configure(self.room_jid.userhost())
	
	def groupChatReceived(self, msg):
		msg = msg.toElement()
		if msg["type"] == 'groupchat' and hasattr(msg, "body"):
			print >>sys.stderr, str(msg.__dict__)
			plugin('heard', self, msg)
		# else:
		# 	print >>sys.stderr, "UNKNOWN GROUP MESSAGE: %s" % msg.__dict__
