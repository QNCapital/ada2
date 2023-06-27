import sys
import time
import random
import requests
from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["button1" , "button2" , "equation"]
AIO_USERNAME = ""
AIO_KEY = ""
global_equation = "x1-x2 -x3"
def init_global_equation():
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/QNCapital/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global_equation = data["last_value"]
    print("Get lastest value:", global_equation)

def modify_value(x1, x2, x3):
    result = eval(global_equation)
    print(result)
    return result

def connected(client):
    print("Server connected ...")
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("equation")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribeb!!!")

def disconnected(client):
    print("Disconnected from the server!!!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload)
    if(feed_id == "equation"):
        global_equation = payload
        print(global_equation)

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()
init_global_equation()

while True:
    time.sleep(10)
    s1 = random.randint(1,100)
    s2 = random.randint(1,100)
    s3 = random.randint(1,100)
    client.publish("sensor1", s1)
    client.publish("sensor2", s2)
    client.publish("sensor3", s3)
    s4 = modify_value(s1, s2, s3)
    print(s4)
    pass
