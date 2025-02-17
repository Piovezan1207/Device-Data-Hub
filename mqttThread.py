import paho.mqtt.client as mqtt
import json

from dotenv import load_dotenv
import os

load_dotenv()

import threading


#Função que será chamada no momento que a conexão com o broker for feita
def on_connect(client, userdata, flags, rc):    
    print("Connected with result code "+str(rc))    
    # print(ROBOT_POSITION_TOPIC_CALLBACK)
    # client.subscribe(ROBOT_POSITION_TOPIC_CALLBACK) #Se inscreve em um tópico
#Função que vai ser chamada sxempre que chegar uma mensagem do tópico que está inscrito

def on_message(client, userdata, msg):    
    print(msg.topic+" "+str(msg.payload)) 
    # mensagem = msg.payload    
    # client.publish(DASHBOARD_TOPIC, testLatency(mensagem))
    # print()

BROKER_IP=os.getenv("BROKER_IP")
BROKER_PORT=int(os.getenv("BROKER_PORT"))
BROKER_USER=os.getenv("BROKER_USER")
BROKER_PASSWORD=os.getenv("BROKER_PASSWORD")



def startMqttThread():
    client = mqtt.Client() #Cria um cliente MQTT
    client.on_connect = on_connect #Define qual a função que será chamada quando se concetar ao broker
    client.on_message = on_message #Define qual a função que será chamada quando receber uma mensagem
    print("Conectando...")
    client.username_pw_set(BROKER_USER, BROKER_PASSWORD) #Configura o login e senha do broker (apenas é necessário se o broker tiver senha)
    client.connect(BROKER_IP, BROKER_PORT, 60) #Se conecta a um broker
    tread = threading.Thread(target=client.loop_forever)
    tread.start()
    return tread, client

