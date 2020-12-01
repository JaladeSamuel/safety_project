import sys
import numpy as np
from capteur.capteur import capteur
import paho.mqtt.publish as publish


def main(args):
	temp  = capteur(0.6).get_temp()
	publish.single("capteur/temp", str(temp), hostname="localhost")

if __name__ == '__main__':
    main(sys.argv[1:])
