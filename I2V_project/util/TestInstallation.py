#!/usr/bin/env python
'''
'''
import unittest
import logging
from logging import config

config.fileConfig("I2V_project/conf/I2V.cfg")
logger = logging.getLogger()

class ModuleImportTestCase(unittest.TestCase):
	def test_gensim(self):
		test_result = False
		logger.info("try to test gensim installation...")
		try:
			import gensim
			logger.info("succeed in importing gensim")
			test_result = True
		except:
			logger.error("Failed to import gensim")
			raise
		self.assertEqual(True, test_result)

if __name__=='__main__':
	unittest.main()
