#Tests to run on the Buffer script
#TO DO: Test buffer.remove() and buffer.isEmpty()

import unittest
from lib1.Buffer import *
from lib1.Quote import *


class testBuffer(unittest.TestCase):
	
	
	def testInit(self):
		self.assertEqual(Buffer().quotes, [])
		
	def testAdd(self):
		b = Buffer()
		q = Quote('ASDA')
		b.add('ASDA')
		print(b.quotes)
		self.assertTrue(b.quotes[0]=='ASDA')


if __name__ == '__main__':
	unittest.main()
