import paho.mqtt.client as mqtt

print("Initialisation du service 1")
client = mqtt.Client("service1")
client.connect("localhost")
client.subscribe("/sensors/temp")
client.on_message = on_message

buffer = []
seuil = 30

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

while True:
    pass