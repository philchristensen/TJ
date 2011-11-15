# TJ, a Twisted Jabber bot
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
Parse command strings sent by the client. 

This parser can understand a variety of phrases, but they are all represented
by the (BNF?) form:

<verb>[[[<dobj spec> ]<direct-object> ]+[<prep> [<pobj spec> ]<object-of-the-preposition>]*]

There are a long list of prepositions supported, some of which are interchangeable.
"""

import re

#Here are all our supported prepositions
preps = [['with', 'using'],
		['at', 'to'],
		['in front of'],
		['in', 'inside', 'into', 'within'],
		['on top of', 'on', 'onto', 'upon', 'above'],
		['out of', 'from inside', 'from'],
		['over'], 
		['through'], 
		['under', 'underneath', 'beneath', 'below'],
		['around', 'round'],
		['between', 'among'],
		['behind', 'past'],
		['beside', 'by', 'near', 'next to', 'along'],
		['for', 'about'],
		#['is'],
		['as'],
		['off', 'off of']]

prepstring = ""
for item in preps:
	prepstring += "|".join(item)
	if(item != preps[len(preps) - 1]):
		prepstring += "|"

PREP_SRC = r'(?:\b)(?P<prep>' + prepstring + r')(?:\b)'
SPEC = r"(?P<spec_str>my|the|a|an|\S+(?:\'s|s\'))"
PHRASE_SRC = r'(?:' + SPEC + r'\s)?(?P<obj_str>.+)'

PREP = re.compile(PREP_SRC)
PHRASE = re.compile(PHRASE_SRC)
POBJ_TEST = re.compile(PREP_SRC + "\s" + PHRASE_SRC)
MULTI_WORD = re.compile(r'((\"|\').+?(?!\\).\2)|(\S+)')

def parse(sentence):
	return Parser(Lexer(sentence))

class Lexer(object):
	"""
	Identify the various parts of a imperative sentence.
	"""
	def __init__(self, command):
		self.command = command
		
		self.dobj_str = None
		self.dobj_spec_str = None
		
		# First, find all words or double-quoted-strings in the text
		iterator = re.finditer(MULTI_WORD, command)
		self.words = []
		qotd_matches = []
		for item in iterator:
			if(item.group(1)):
				qotd_matches.append(item)
			word = item.group().strip('\'"').replace("\\'", "'").replace("\\\"", "\"")
			self.words.append(word)
		
		# Now, find all prepositions
		iterator = re.finditer(PREP, command)
		prep_matches = []
		for item in iterator:
			prep_matches.append(item)
		
		#this method will be used to filter out prepositions inside quotes
		def nonoverlap(item):
			(start, end) = item.span()
			for word in qotd_matches:
				(word_start, word_end) = word.span()
				if(start > word_start and start < word_end):
					return False
				elif(end > word_start and end < word_end):
					return False
			return True
		
		#nonoverlap() will leave only true non-quoted prepositions
		prep_matches = filter(nonoverlap, prep_matches)
		
		#determine if there is anything after the verb
		if(len(self.words) > 1):
			#if there are prepositions, we only look for direct objects
			#until the first preposition
			if(prep_matches):
				end = prep_matches[0].start()-1
			else:
				end = len(command)
			#this is the phrase, which could be [[specifier ]object]
			dobj_phrase = command[len(self.words[0]) + 1:end]
			match = re.match(PHRASE, dobj_phrase)
			if(match):
				result = match.groupdict()
				self.dobj_str = result['obj_str'].strip('\'"').replace("\\'", "'").replace("\\\"", "\"")
				if(result['spec_str']):
					self.dobj_spec_str = result['spec_str'].strip('\'"').replace("\\'", "'").replace("\\\"", "\"")
				else:
					self.dobj_spec_str = ''
		
		self.prepositions = {}
		#iterate through all the prepositional phrase matches
		for index in range(len(prep_matches)):
			start = prep_matches[index].start()
			#if this is the last preposition, then look from here until the end
			if(index == len(prep_matches) - 1):
				end = len(command)
			#otherwise, search until the next preposition starts
			else:
				end = prep_matches[index + 1].start() - 1
			prep_phrase = command[start:end]
			phrase_match = re.match(POBJ_TEST, prep_phrase)
			if not(phrase_match):
				continue
			
			result = phrase_match.groupdict()
			
			#if we get a quoted string here, strip the quotes
			result['obj_str'] = result['obj_str'].strip('\'"').replace("\\'", "'").replace("\\\"", "\"")
			
			if(result['spec_str'] is None):
				result['spec_str'] = ''
			
			#if there is already a entry for this preposition, we turn it into
			#a list, and if it already is one, we append to it
			if(result['prep'] in self.prepositions):
				item = self.prepositions[result['prep']]
				if not(isinstance(item[0], list)):
					self.prepositions[result['prep']] = [[result['spec_str'], result['obj_str'], None], item]
				else:
					self.prepositions[result['prep']].append([result['spec_str'], result['obj_str'], None])
			#if it's a new preposition, we just save it here.
			else:
				self.prepositions[result['prep']] = [result['spec_str'], result['obj_str'], None]
	
	def get_details(self):
		return dict(
			command			= self.command,
			dobj_str		= self.dobj_str,
			dobj_spec_str	= self.dobj_spec_str,
			words			= self.words,
			prepositions	= self.prepositions,
		)

class Parser(object):
	"""
	The parser interface.
	"""
	def __init__(self, lexer):
		"""
		Create a new parser object for the given command, as issued by
		the given caller, using the registry.
		"""
		self.lexer = lexer
		
		self.this = None
		self.verb = None
		
		for key, value in self.lexer.get_details().items():
			self.__dict__[key] = value
	
	def get_dobj_str(self):
		"""
		Get the direct object **string** for this parser. If there was no
		direct object **string** found, raise a NoSuchObjectError
		"""
		if not(self.dobj_str):
			raise NoSuchObjectError('direct object')
		return self.dobj_str
	
	def get_pobj_str(self, prep, return_list=False):
		"""
		Get the object **string** for the given preposition. If there was no
		object **string** found, raise a NoSuchObjectError; if the preposition
		was not found, raise a NoSuchPrepositionError.
		"""
		if not(self.prepositions.has_key(prep)):
			raise NoSuchPrepositionError(prep)
		if(isinstance(self.prepositions[prep][0], list)):
			matches = []
			for item in self.prepositions[prep]:
				if(item[1]):
					matches.append(item[1])
			if(len(matches) > 1):
				if(return_list):
					return matches
				else:
					raise matches[0]
			elif not(matches):
				raise NoSuchObjectError(self.prepositions[prep][0][1])
		return self.prepositions[prep][1]
	
	def get_pobj_spec_str(self, prep, return_list=False):
		"""
		Get the object **specifier** for the given preposition. If there was no
		object **specifier** found, return the empty string; if the preposition
		was not found, raise a NoSuchPrepositionError.
		"""
		if not(self.prepositions.has_key(prep)):
			raise NoSuchPrepositionError(prep)
		if(isinstance(self.prepositions[prep][0], list)):
			matches = []
			for item in self.prepositions[prep]:
				matches.append(item[0])
			if(len(matches) > 1):
				if(return_list):
					return matches
				else:
					return matches[0]
		return self.prepositions[prep][0]
	
	def has_dobj_str(self):
		"""
		Was a direct object string found?
		"""
		return self.dobj_str != None
	
	def has_pobj_str(self, prep):
		"""
		Was a object string for this preposition found?
		"""
		if(prep not in self.prepositions):
			return False
		
		found_prep = False
		
		if(isinstance(self.prepositions[prep][0], list)):
			for item in self.prepositions[prep]:
				if(item[1]):
					found_prep = True
					break
		else:
			found_prep = bool(self.prepositions[prep][1])
		return found_prep
