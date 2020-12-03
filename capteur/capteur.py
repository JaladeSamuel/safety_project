import sys
import time
from numpy import random
import paho.mqtt.publish as publish

class capteur :
	"""docstring for meteo"""
	def __init__(self, failrate):
		self.failrate = failrate

	def get_temp(self):
		temp = -1
		if (self.failrate*random.random_sample() < 0.5):
			temp = 10 * (self.failrate + random.random_sample())
		return temp
	def get_failrate(self):
		return self.failrate

	def publish(self):
		while(1):
			temp  = capteur(0.7).get_temp()
			publish.single("capteur/temp", str(temp), hostname="localhost")
			time.sleep(.100)
		
def main(args):
	print(capteur(.9).publish())

if __name__ == '__main__':
    main(sys.argv[1:])