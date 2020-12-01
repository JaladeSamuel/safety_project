import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    if message.topic == "/sensors/temp":
        if len(buffer) > seuil:
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
    client.subscribe("/sensors/temp")

    buffer = []
    seuil = 30

    client.loop_start()