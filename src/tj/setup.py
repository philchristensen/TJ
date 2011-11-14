# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

def pluginModules(moduleNames):
	from twisted.python.reflect import namedAny
	for moduleName in moduleNames:
		try:
			yield namedAny(moduleName)
		except ImportError:
			pass
		except ValueError, ve:
			if ve.args[0] != 'Empty module name':
				import traceback
				traceback.print_exc()
		except:
			import traceback
			traceback.print_exc()

def regeneratePluginCache():
	pluginPackages = ['twisted.plugins']
	
	from twisted import plugin
	
	for pluginModule in pluginModules(pluginPackages):
		plugin_gen = plugin.getPlugins(plugin.IPlugin, pluginModule)
		try:
			plugin_gen.next()
		except StopIteration, e:
			pass
		except TypeError, e:
			print 'TypeError: %s' % e

