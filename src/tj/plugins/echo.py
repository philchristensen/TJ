# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
A basic echo plugin.
"""

from zope.interface import classProvides

from twisted import plugin
from twisted.words.xish import domish

from tj.plugins import IBotPlugin

class EchoPlugin(object):
	classProvides(plugin.IPlugin, IBotPlugin)
	
	name = u'echo'
	
	def heard(self, protocol, msg):
		reply = domish.Element((None, "message"))
		reply["to"] = msg["from"]
		reply["from"] = msg["to"]
		reply["type"] = 'chat'
		reply.addElement("body", content="echo: " + str(msg.body))
		protocol.send(reply)
