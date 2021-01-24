# safety_project
Un service logiciel S acquiert des mesures au travers d’un capteur C. Le service calcule une fonction sur une fenêtre glissante de n valeurs numériques. Le résultat de la fonction de calcul sur les entrées du capteurs est retourné à l’environnement (affichage écran).

## Requierements:
Pour utiliser notre programme il faut avoir Python 3 et Mosquitto qui permet de communiqué en MQTT avec la commande `sudo apt-get install mosquitto
`. 

## Lancer le programme: 
Pour lancer le script start.sh sous linux. 

Celui ci va créer un document historique.txt. Puis dans un second temps, le script va lancer les programmes Python pour le capteur et les services. 
