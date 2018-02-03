#!/usr/bin/env python
import unittest

class ModuleImportTestCase(unittest.TestCase):
	def test_gensim(self):
		result = False
		print "try to test gensim installation..."
		try:	
			import gensim
			print "succeed in importing gensim" 		
		except:
			print "Failed to import gensim"
			raise	

if __name__=='__main__':
	unittest.main()

