# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
twistd plugin support

This module adds a 'tjbot' server type to the twistd service list.
"""

import warnings

from zope.interface import classProvides

from twisted import plugin
from twisted.python import usage, log
from twisted.internet import reactor
from twisted.application import internet, service

from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient

from tj import conf, xmpp

class botServer(object):
	"""
	The TJ bot server startup class.
	"""

	classProvides(service.IServiceMaker, plugin.IPlugin)

	tapname = "tjbot"
	description = "Run a TJ Jabber bot."

	class options(usage.Options):
		"""
		Implement option-parsing for the TJ twistd plugin.
		"""
		optParameters = [
						 ["conf", "f", conf.DEFAULT_CONF_PATH, "Path to configuration file, if any.", str],
						]

	@classmethod
	def makeService(cls, config):
		"""
		Setup the necessary network services for the application server.
		"""
		if(conf.get('suppress-deprecation-warnings')):
			warnings.filterwarnings('ignore', r'.*', DeprecationWarning)

		master_service = service.MultiService()
		
		xmpp_client = XMPPClient(jid.internJID(conf.get('jid')), conf.get('secret'))
		xmpp_client.setName("xmpp-client")
		xmpp_client.setServiceParent(master_service)
		
		bot = xmpp.BotProtocol()
		bot.setHandlerParent(xmpp_client)
		
		for room in conf.get('join-rooms'):
			print 'creating room client for %s' % room
			muc_client = xmpp.MUCBotClient(*room)
			muc_client.setHandlerParent(xmpp_client)
		
		return master_service
