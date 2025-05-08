# note: dung MQTT lam thi feed la tansang1/feeds/"name"
# pythonIoT
# ket noi adafruit vs may tinh

import sys
from Adafruit_IO import MQTTClient
import time
# import random
import keyboard
# from keras_openCV import *
import requests
import threading
import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from model.camera.Handcontrol import *

# class xu_li_tt:
#     def __init__(self):
#         pass


AIO_USERNAME = "tansang1"
AIO_KEY = ""

# kenh nhan data
AIO_FEED_IDs = ["cambien-anhsang", 
                "cambien-nhietdo", 
                "cambien-doam", 
                "cambien-dat", 
                "ai", 
                "nut-quat",
                "nutnhan-bom",
                "nutnhan2",
                "data-quat",
                ]

data_anhsang=None   # light             
data_nhietdo=None   # temp              
data_doam=None      # Humidity          
data_dat=None       # Soil Moisture     

data_nut_quat=None  # nut quat
data_nut_bom=None   # nut bom

have_data = False

def is_data_tree():
    global data_anhsang, data_nhietdo, data_doam, data_dat
    if data_anhsang and data_nhietdo and data_doam and data_dat:
        return True
    return False

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " feed id: " + feed_id)

    if feed_id:
        #* update data
        if feed_id == "cambien-anhsang":
            global data_anhsang
            data_anhsang = payload
        elif feed_id == "cambien-doam":
            global data_doam
            data_doam = payload
        elif feed_id == "cambien-nhietdo":
            global data_nhietdo
            data_nhietdo = payload
        elif feed_id == "cambien-dat":
            global data_dat
            data_dat = payload
        elif feed_id == "nut-quat":
            global data_nut_quat
            data_nut_quat = payload

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_subscribe = subscribe
client.connect()
client.loop_background()


def process_data_deceision_tree(data):
    # Load the model
    with open('model/model_phantich/decision_tree_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    # input : [Light, Temperature, Humidity, Soil Moisture]
    test_input = np.array([data]) 

    # Predict the label using the model
    prediction = loaded_model.predict(test_input)

    #! tesing printing
    # print("Prediction:", prediction)  # Output will be 'Normal' or 'Not Normal'
    # print("Prediction:", prediction[0])  # Output will be 'Normal' or 'Not Normal'

    return prediction[0]

#? gia su dk cay phat trien bth
#     light_ok = 10000 <= row['Light (lux)'] <= 50000
#     temp_ok = 15 <= row['Temperature (°C)'] <= 25
#     humid_ok = 50 <= row['Humidity (%)'] <= 70
#     soil_ok = 20 <= row['Soil Moisture (%)'] <= 40
def main(client):
    max_thread_number = 1

    # start push information into adafruit
    while True:
        # * nhan thong tin
        client.on_message = message

        # todo: receive data from adafruit
        # !tesing
        # * dieu khien quat
        global data_nut_quat
        if data_nut_quat and data_nut_quat == "OFF":
            # client.publish("nut-quat", "OFF")
            data_nut_quat = None
            print("nut-quat: ", "OFF")
        if data_nut_quat and data_nut_quat == "ON" and get_thread_number() < max_thread_number:
            data_nut_quat = None

            thread = threading.Thread(target=start_camera
                                      , args=(client, ))
            
            print("thread start...")
            thread.start()

        # * nhan dc 4 tt cho cay        
        if is_data_tree():
            global data_anhsang, data_nhietdo, data_doam, data_dat
            data = [data_anhsang, data_nhietdo, data_doam, data_dat]
            
            prediction = process_data_deceision_tree(data)

            #* Reset data after processing   
            data_anhsang = data_nhietdo = data_doam = data_dat = None  

            client.publish("ai", prediction)
    
        if keyboard.is_pressed('q'):  # Check if 'q' is pressed
            # print("Disconnecting...")
            client.disconnect()  # Disconnect the MQTT client
            break

        # end 1 loop
        time.sleep(3)




if __name__ == "__main__":
    main(client)

    # start_camera(client, True)