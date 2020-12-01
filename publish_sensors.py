import sys
import time
import numpy as np
from capteur.capteur import capteur
import paho.mqtt.publish as publish


def main(args):
	while(1):
		temp  = capteur(0.7).get_temp()
		publish.single("capteur/temp", str(temp), hostname="localhost")
		time.sleep(.100)


if __name__ == '__main__':
    main(sys.argv[1:])
