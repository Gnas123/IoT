#pip install paho-mqtt==1.6.1
# https://www.youtube.com/watch?v=t3kNm9uFSxA&ab_channel=chipfc

# note: dung MQTT lam thi feed la tansang1/feeds/"name"

import paho.mqtt.client as mqtt
import time

# MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_SERVER = "io.adafruit.com"
# default port: 1883
MQTT_PORT = 1883
# MQTT_PASSWORD = ""
MQTT_PASSWORD = "aio_SYpN66ebu5Bxw4maAWQmBNO2BMg8"
# MQTT_USERNAME = "testing12345"
MQTT_USERNAME = "tansang1"
# MQTT_TOPIC_PUB = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/cambien1"



a= None

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_recv_message(client, userdata, message):
    global a
    a = message.payload.decode("utf-8")
    #print("Received: ", message.payload.decode("utf-8"))
    print(" Received message " + message.payload.decode("utf-8")
          + " on topic '" + message.topic
          + "' with QoS " + str(message.qos))

# Tạo MQTT client
mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message

mqttClient.loop_start()

# counter = 0
# while True:
#     time.sleep(5)
#     counter += 1
#     mqttClient.publish(MQTT_TOPIC_PUB, counter)

def main():
    counter = 0
    
    while True:
        # Đăng ký topic
        # print("Đang lắng nghe dữ liệu...")
        mqttClient.subscribe(MQTT_TOPIC_SUB)
        time.sleep(5)

        global a
        print("a: ", a)
        # client.loop_forever()
        

if __name__ == "__main__":
    main()