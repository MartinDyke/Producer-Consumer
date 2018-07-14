from lib1.Printer import *
import time

class Consumer:
	def __init__(self, buff, companies, file):
		self.buffer = buff  # initializes a buffer attribute buff
		self.values = {i: [0, 100, 0, 0] for i in
		               companies}  # [counter, min, average,max]
		self.companies = companies
		self.printer = Printer(file)
	
	def reset(self):
		self.values = {i: [0, 100, 0, 0] for i in self.companies}
	
	def run(self):
		Day = 1
		while Day != 11:  # for 100 days do:
			quoteNo = 0
			while quoteNo != 2500:  # while quoteNo is less than 1000 do:
				if not self.buffer.isEmpty():
					a = self.buffer.remove()
					self.values[a.company][0] += 1
					self.values[a.company][2] += a.value
					if a.value < self.values[a.company][1]: self.values[a.company][1] = a.value
					if a.value > self.values[a.company][3]: self.values[a.company][3] = a.value
					quoteNo += 1
			self.printer.printToFile('Day ' + str(Day) + "\n")
			for key in self.values:
				if self.values[key][0] !=0:
					self.printer.printToFile('The highest value for ' + key + ' is ' + str(self.values[key][3]) + "\n" +
						'The lowest value for ' + key + ' is ' + str(self.values[key][1]) + "\n" +
						'The average value for ' + key + ' is ' +
						str("{0:.1f}".format(self.values[key][2]/self.values[key][0])) + '\n' )
			
			#Print to console:
			#print('Day ' + str(Day) + ":\n")
			#for key in self.values:
			#	if self.values[key][0] != 0:
			#		print('The highest value for ' + key + ' is ' + str(self.values[key][3]) + "\n" +
			#                                   'The lowest value for ' + key + ' is ' + str(self.values[key][1]) + "\n" +
			#                                   'The average value for ' + key + ' is ' + str(
			#              "{0:.1f}".format(self.values[key][2] / self.values[key][0])) + '\n')
			
			time.sleep(0.001)
			Day += 1
			self.reset()