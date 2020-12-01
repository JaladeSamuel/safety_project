import paho.mqtt.client as mqtt

buffer = []
seuil = 30

def on_message(client, userdata, message):
    global buffer

    if message.topic == "capteur/temp":
        if len(buffer) > seuil:
            print("Buffer rempli : " + str(buffer))
            traitement(buffer)
            buffer = []
        
        buffer.append(message.payload.decode("utf-8"))
    pass

def traitement(donnees):
    # thomas à toi de jouer
    pass

if __name__ == "__main__":
    print("Initialisation du service 1")
    
    client = mqtt.Client("service1")
    client.on_message = on_message

    client.connect("localhost")
    client.subscribe("capteur/temp")
    client.loop_start()

    while True:
        pass