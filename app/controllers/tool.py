#!/usr/bin/env python2
# encoding: utf-8
"""
tool.py
use to manage pic files from cmd
"""

import sys
import os
import getopt
from store import Store
from store import getImageType

help_message = '''
Usage: store.py [options] [filename]

Options:
  -i, --import     Import file to storeage
  -q, --id        get a file by id
  -l, --list       List files
  -l, --list       test a file
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output

'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hi:q:lt:v", ["help", "import=", "id=", "list", "test", "verbose", "limit=", "start="])
		except getopt.error, msg:
			raise Usage(msg)
		
		#print(opts)
		#print(args)
		action = None
		store_file = None
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-i", "--import"):
				store_file = value
				print('store file: {0}'.format(store_file))
				action = 'import'
			elif option in ("-l", "--list"):
				action = 'list'
			elif option in ("-t", "--test"):
				action = 'test'
				filename = value
			elif option in ("-q", "--id"):
				action = 'get'
				id = value
			else:
				pass
		
		print('action: {}'.format(action))
		if (action == 'list'):
			store = Store()
			gallery = store.browse()
			for img in gallery['items']:
				#print(img)
				print("{0[filename]}\t{0[length]:8,d}".format(img))
			return 0
		elif (action == 'get') and id is not None:
			store = Store()
			if not store.getFs().exists(id):
				print ('not found')
				return 1
			gf = store.get(id)
			#print(gf)
			print ("found: {0.name}\t{0.length}".format(gf))
			return 0
		elif (action == 'test'):
			print('filename: %r' % filename)
			fp = open(filename, 'rb')
			h = fp.read(32)
			print(getImageType(h))
			return 0
		elif (action == 'import'):
			print('storing: %r' % store_file)
			fp = open(store_file, 'rb')
			type = "IMAGE"
			data = fp.read()
#			h = fp.read(32)
#			type =  getImageType(h)
#			print(store_file+": "+type )
			store = Store()
			result = store.store(data, type, store_file)
			print result
			return 0
				

	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())

