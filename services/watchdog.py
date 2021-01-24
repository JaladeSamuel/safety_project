from threading import Thread
import paho.mqtt.client as mqtt
import time

class WatchThread(Thread):

    def __init__(self, service_to_watch, sleep_time=1):
        def on_connect(client, userdata, flags, rc):
            self.client.subscribe(self.topic)

        def on_message(client, userdata, msg):
            if msg.topic == self.topic and str(msg.payload.decode("utf-8")) == "im_alive":
                self.message_count += 1

        self.service_to_watch = service_to_watch
        self.sleep_time = sleep_time
        self.is_service_up = True
        self.topic = "service" + str(self.service_to_watch) + "/is_alive"
        self.message_count = 0

        self.client = mqtt.Client("watchdog_for_" + str(self.service_to_watch))
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("localhost")
        self.client.loop_start()

    def run(self):
        while True:
            last_message_count = self.message_count
            time.sleep(self.sleep_time)

            print(last_message_count, "vs", self.message_count)
            if self.message_count > last_message_count:
                self.is_service_up = True
            else:
                self.is_service_up = False