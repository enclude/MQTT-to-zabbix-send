import json
import os

from paho.mqtt import client as mqtt_client
broker = os.environ['MQTT_broker']
port = 1883
topic = os.environ['MQTT_topic']
client_id = os.environ['MQTT_clientid']

from zabbix_utils import Sender,ZabbixAPI,ItemValue
sender = Sender(os.environ['ZABBIX_address'],10051)

api = ZabbixAPI(os.environ['ZABBIX_address'],10051)
api.login(token=os.environ['ZABBIX_token'])
zabbixhosts = api.host.get()
temp = ' '.join(str(x) for x in zabbixhosts)
zabbixhosts = temp

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("========================")
        mqtttopic = msg.topic
        mqtttopic = mqtttopic.lstrip("zigbee2mqtt/")
        mqttpayload = msg.payload.decode()
        mqttpayload = mqttpayload.replace("\\","")
        print(mqtttopic, mqttpayload)
        # print("=")

        data = json.loads(mqttpayload)
        items = []
        print("--------------")
        print(mqtttopic)

        for key, value in data.items():
            print(key,value)
            item = ItemValue(mqtttopic, key, value)
            items.append(item)
        # print(items)
        response = sender.send(items)
        print(response)

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
