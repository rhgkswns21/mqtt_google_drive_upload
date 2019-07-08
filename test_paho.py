from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime as date
import paho.mqtt.client as mqtt
import os
import logging

logging.basicConfig(level=logging.DEBUG)

log = 'log'
logflag = False

f = open('E:\MyFolder\Source\Python\PycharmProjects\External Data\mqtt_info\mqtt_info.txt', 'r')

broker = f.readline()
mqtt_topic = f.readline()
file_path = f.readline().strip()
f.close()

# 클라이언트가 서버에게서 CONNACK 응답을 받을 때 호출되는 콜백
def on_connect(client, userdata, rc):
    print ("Connected with result coe " + str(rc))
    client.subscribe("Entity/SHM/Node/353041080754218/Device/Status")

# 서버에게서 PUBLISH 메시지를 받을 때 호출되는 콜백
def on_message(client, userdata, msg):
    now_time = str(date.datetime.now())
    print("Time: ", now_time)
    print("Topic: ", msg.topic)
    mqtt_data = str(msg.payload)
    split_topic = str(msg.topic).split('/')

logger = logging.getLogger(__name__)

client = mqtt.Client()        # MQTT Client 오브젝트 생성
print("Test Step 01")
client.enable_logger(logger)
print("Test Step 02")
client.on_connect = on_connect     # on_connect callback 설정
print("Test Step 03")
client.on_message = on_message   # on_message callback 설정
print("Test Step 04")
client.connect(broker.strip())   # MQTT 서버에 연결
print("Test Step 05")

client.subscribe(mqtt_topic.strip())

client.loop_forever()