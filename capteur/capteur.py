import sys
import time
from numpy import random
import paho.mqtt.publish as publish

class capteur :
	"""docstring for meteo"""
	def __init__(self, failrate):
		self.failrate = failrate

	def get_temp(self):
		tmp = random.random_sample()
        if (tmp+self.failrate < 1):
            res = 19.5 + random.random_sample()
        else:
            res = -1
        return res 
	def get_failrate(self):
		return self.failrate

	def publish(self):
		while(1):
			publish.single("capteur/temp", str(self.get_temp()), hostname="localhost")
			time.sleep(.100)
		
def main(args):
	print(capteur(.9).publish())

if __name__ == '__main__':
    main(sys.argv[1:])
