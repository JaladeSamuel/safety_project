import paho.mqtt.client as mqtt
import time

flag_check = False
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Service2 Connected with result code "+str(rc))
    print("Watching service1...")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("fail_ack")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    global flag_check
    #print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    if msg.topic == "service1/fail_ack":
        if str(msg.payload.decode("utf-8")) == "yes":
            flag_check = True


client = mqtt.Client("service2")
client.on_connect = on_connect
client.on_message = on_message

if __name__ == "__main__":
    print("Initialisation du service 2")

    client.connect("localhost")
    client.subscribe("service1/fail_ack")
    time.sleep(2)
    client.loop_start()

    while True:
        
        flag_check = False
        client.publish("service2/fail_req")
        time.sleep(2)
        if not flag_check:
            #service1 down
            print("service1 down")
        print("service1 up")