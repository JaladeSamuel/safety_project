import paho.mqtt.client as mqtt
import numpy as np 

buffer = []
seuil = 30

client = mqtt.Client("service1")


def on_message(client, userdata, message):
    global buffer

    if message.topic == "capteur/temp":
        if len(buffer) > seuil:
            result = traitement(buffer)
            print("Buffer rempli : " + str(buffer) + " ==> " + str(result))
            buffer = []
        
        buffer.append(float(message.payload.decode("utf-8")))
    elif message.topic == "service2/fail_req":
        client.publish("service1/fail_ack", "yes")


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
    

if __name__ == "__main__":
    print("Initialisation du service 1")
    
    client.on_message = on_message
    client.connect("localhost")
    client.subscribe("capteur/temp")
    client.subscribe("service2/fail_req")
    client.loop_start()

    while True:
        pass
