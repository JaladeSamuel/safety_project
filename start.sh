#!/bin/bash

rm data/historique.txt

gnome-terminal -- python3 capteur/capteur.py
gnome-terminal -- python3 services/service1.py
gnome-terminal -- python3 services/service2.py