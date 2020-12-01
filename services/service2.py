import paho.mqtt.client as mqtt




topic_fail_req = "fail_req"
topic_fail_ack = "fail_ack" 
host_name = "local_host"
client_name = "fail_detector"
Client(client_id=client_name, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_fail_ack
    	return True


def call_primary():
	failDet.publish(topic_fail_req, "are you alive")


failDet = mqtt.Client(client_name)

failDet.on_connect = on_connect
failDet.on_message = on_message


failDet.connect(host_name)
failDet.subscribe(topic_fail_ack)
primary_alive = True

while primary_alive :
	call_primary
	time.sleep(5)
	if !failDet.on_message:
		primary_alive = False
		print("Primary system seams dead...\n")
	else :
		print("Primary system is alive\n")










