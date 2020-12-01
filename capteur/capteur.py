import sys
from numpy import random


class capteur :
	"""docstring for meteo"""
	def __init__(self, failrate):
		self.failrate = failrate

	def get_temp(self):
		temp = -1
		if (self.failrate*random.random_sample() < 0.5):
			temp = 10 * (self.failrate + random.random_sample())
		return temp
		
def main(args):
	print(capteur(.9).get_temp())

if __name__ == '__main__':
    main(sys.argv[1:])