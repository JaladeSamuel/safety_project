import paho.mqtt.client as mqtt
import time
import numpy as np 
from datetime import datetime
import watchdog

flag_check = False
service2_launched = False
buffer = []
seuil = 30
state = 0 #State of this service (updated at launch with the number of writings in the history file of the service1)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Service2 Connected with result code "+str(rc))
    print("Watching service1...")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("fail_ack")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    global buffer
    global flag_check
    global service2_launched
    global state 
    
    if service2_launched:
        if message.topic == "capteur/temp":
            if len(buffer) > seuil:  
                result = traitement(buffer)
                print("30 dernières valeurs : " + str(buffer) + " ==> " + str(result))
                buffer = []
            buffer.append(float(message.payload.decode("utf-8")))
            
            data = float(message.payload.decode("utf-8"))
            save_historique(data)
            state += 1
            save_state(state)

def launch_service2(client):
    print("Launch service2")
    global service2_launched
    global state

    print("Recovering service1 state...")
    state = int(read_state_service1()) #recovering
    print("State recovered : " + str(state))

    service2_launched = True
    client.subscribe("capteur/temp")

def traitement(donnees,number_of_point_median_filter=3,number_of_point_smooth=4):
    """
    Applied a median filter to the function to reduce the noise. Then smooth the potential function to avoid noise by computing the mean of number_of_point_smooth for every value.

    Args:
    number_of_point_smooth = number of point in the average to smooth the function
    number_of_point_median_filter = number of point in the median filter
        
    Return:
    The mean of the clean donnnees
    """
    res = []
    for i in range(len(donnees)-number_of_point_median_filter+1):
        liste = []
        for j in range(number_of_point_median_filter):
            liste.append(donnees[i+j])
        
        # median filter
        test_list = liste
        test_list.sort()
        mid = len(test_list) // 2
        resu = (test_list[mid] + test_list[~mid]) / 2
        res.append(float(resu))

    for i in range(number_of_point_median_filter-1,0,-1):
        res.append(donnees[-i])
    
    potential_channel = res.copy()
    # median filter
    res = []
    for i in range(int(np.ceil(number_of_point_smooth/2))):
        res.append(potential_channel[i])
            
    for i in range(len(potential_channel)-number_of_point_smooth):
        mean = 0
        for j in range(number_of_point_smooth):
            mean += potential_channel[i+j]
        mean = mean / number_of_point_smooth
        res.append(mean)

    for i in range(int(np.floor(number_of_point_smooth/2)),0,-1):
        res.append(potential_channel[-i])
       
    return np.mean(potential_channel)    

def save_historique(data,path="./data/historique.txt"):
    """
    Save in the historique file the buffer, the output of the treatment and the date/time

    Agrs :
    data = a string which contains all the data (buffer, ...)
    path = path to the historique file
    """
    historique = open(path,'a')

    # get the date and hour
    datetime_object = datetime.now()
    historique.write(str(datetime_object)+"\n")
    # save data in historique
    historique.write(str(data))
    historique.write("\n")

    historique.close()

def save_state(sate,path="./state/service2_state.txt"):
    """
    Save in the state file the current sate of this service

    Args :
    state = a variable that represent the symbolic state of the current service (number of writings in the history file)
    path = path to the historique file
    """
    state_file = open(path,'w')

    # get the date and hour
    datetime_object = datetime.now()
    # save data in historique
    state_file.write(str(datetime_object) + "\n" + str(sate))
    state_file.close()

def read_state_service1(path="./state/service1_state.txt"):
    """
    Read the state of the service1

    Args : path
    """
    state_file = open(path,'r')
    service1_state = state_file.readlines()[1]
    return service1_state


if __name__ == "__main__":
    print("Initialisation du service 2")
    client = mqtt.Client("service2")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost")
    client.loop_start()

    time.sleep(3)

    watch_dog_thread = watchdog.WatchThread(1)
    watch_dog_thread.start()

    while True:
        if not service2_launched:
            # flag_check = False
            # client.publish("service2/fail_req")
            time.sleep(0.5)

            if watch_dog_thread.is_service_up:
                print("service1 up")
            else:
                #service1 down
                print("service1 down")
                launch_service2(client)