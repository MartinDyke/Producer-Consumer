class Printer:
	def __init__(self, file):
		self.file = file
	
	def printToFile(self, text):
		open(self.file, "a").write(text)
