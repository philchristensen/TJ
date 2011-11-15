# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
Pugme is the most important thing in your life

  pug me - Receive a pug
  pug bomb N - get N pugs

Ported from hubot (http://hubot.github.com)
"""

import re

from zope.interface import classProvides

from twisted import plugin
from twisted.internet import defer
from twisted.words.xish import domish

from tj.plugins import IBotPlugin
from twisted.web.client import getPage

import simplejson

def createReply(msg, content):
	reply = domish.Element((None, "message"))
	reply["to"] = msg["from"]
	reply["from"] = msg["to"]
	reply["type"] = 'chat'
	reply.addElement("body", content=content)
	return reply

class PugMe(object):
	classProvides(plugin.IPlugin, IBotPlugin)
	
	name = u'echo'
	
	PUGME = re.compile(r'pug me')
	PUGBOMB = re.compile(r'pug bomb (\d+)?')
	HOWMANY = re.compile(r'how many pugs')
	
	@defer.inlineCallbacks
	def heard(self, protocol, msg):
		result = None
		if(self.PUGME.search(str(msg.body))):
			data = yield getPage('http://pugme.herokuapp.com/random')
			json = simplejson.loads(data)
			reply = createReply(msg, json['pug'])
			protocol.send(reply)
			return
		
		pug_bomb = self.PUGBOMB.search(str(msg.body))
		if(pug_bomb):
			data = yield getPage('http://pugme.herokuapp.com/bomb?count=%s' % pug_bomb.group(1))
			json = simplejson.loads(data)
			for pug in json['pugs']:
				reply = createReply(msg, pug)
				protocol.send(reply)
			return
