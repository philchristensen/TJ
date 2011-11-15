# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

import ez_setup
ez_setup.use_setuptools()

import sys, os, os.path, subprocess

try:
	from twisted import plugin
except ImportError, e:
	print >>sys.stderr, "setup.py requires Twisted to create a proper tj installation. Please install it before continuing."
	sys.exit(1)

from setuptools.command import easy_install
import pkg_resources as pkgrsrc

# disables creation of .DS_Store files inside tarballs on Mac OS X
os.environ['COPY_EXTENDED_ATTRIBUTES_DISABLE'] = 'true'
os.environ['COPYFILE_DISABLE'] = 'true'

postgenerate_cache_commands = ('build', 'build_py', 'build_ext',
	'build_clib', 'build_scripts', 'install', 'install_lib',
	'install_headers', 'install_scripts', 'install_data',
	'develop', 'easy_install')

pregenerate_cache_commands = ('sdist', 'bdist', 'bdist_dumb',
	'bdist_rpm', 'bdist_wininst', 'upload', 'bdist_egg', 'test')

def autosetup():
	from setuptools import setup, find_packages
	return setup(
		name			= "TJ",
		version			= "1.0",

		packages		= find_packages('src') + ['twisted.plugins'],
		package_dir		= {
			''			: 'src',
		},
		include_package_data = True,

		entry_points	= {
			'setuptools.file_finders'	: [
				'git = setuptools_git:gitlsfiles',
			],
		},
		
		zip_safe		= False,
		
		install_requires = ['%s%s' % x for x in dict(
			twisted				= ">=10.1.0",
			#wokkel				= "==0.6.3",
			python_dateutil		= "==1.5",
		).items()],
		
		# metadata for upload to PyPI
		author			= "Phil Christensen",
		author_email	= "phil@bubblehouse.org",
		description		= "a Twisted Words-based Jabber bot",
		license			= "MIT",
		keywords		= "tj twisted jabber bot eggdrop",
		url				= "https://github.com/philchristensen/tj",
	)


if(__name__ == '__main__'):
	if(sys.argv[-1] in pregenerate_cache_commands):
		dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
		if(dist_dir not in sys.path):
			sys.path.insert(0, dist_dir)

		from tj import setup
		print 'Regenerating plugin cache...'
		setup.regeneratePluginCache()

	dist = autosetup()
	if(sys.argv[-1] in postgenerate_cache_commands):
		subprocess.Popen(
			[sys.executable, '-c', 'from tj import setup; setup.regeneratePluginCache(); print "Regenerating plugin cache..."'],
		).wait()
