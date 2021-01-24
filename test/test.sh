#!/bin/bash

gnome-terminal -- python3 capteur/capteur.py & echo $!
gnome-terminal -- python3 services/service1.py & echo $!
gnome-terminal -- python3 services/service2.py & echo $!

SERVICE1=`ps -au | pgrep -f service1`
echo "$SERVICE1"

kill -9 $SERVICE1