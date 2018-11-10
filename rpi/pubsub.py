import paho.mqtt.client as paho
import os
import socket
import ssl
from thread import start_new_thread as newthread
import rpiCamera

awshost = "a3psvjaq4yieuf-ats.iot.us-west-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "noirCamera"                                     # Thing_Name
thingName = "noirCamera"                                    # Thing_Name
caPath = "./awsiot/root-CA.crt"                                      # Root_CA_Certificate_Name
certPath = "./awsiot/noirCamera.cert.pem"                            # <Thing_Name>.cert.pem
keyPath = "./awsiot/noirCamera.private.key"                          # <Thing_Name>.private.key
initStatus=False
def on_connect(client, userdata, flags, rc):                # func for making connection
        print("Connection returned result: " + str(rc) )
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        mqttc.subscribe("#" , 1 )  
        print("subscribed")                            # Subscribe to all topics
 
def on_message(client, userdata, msg):                      # Func for receiving msgs
        print("topic: "+msg.topic)
        print("payload: "+str(msg.payload))
        if msg.topic=="agricert/capture":
            rpiCamera.capture(str(msg.payload))
            print "capture completed"
            rpiCamera.Analyse(str(msg.payload))
        #     rpiCamera.Analyse("histogram_"+str(msg.payload))
        elif msg.topic=="agricert/pingRpi":
                rpiCamera.camStaus()
            
        
 

def on_disconnect(client, userdata, rc):
        print("disconnected"+str(rc))
        mqttc.connect(awshost, awsport, keepalive=60)

def init():
    global initStatus    
    initStatus=True
    print("executing init")
    global mqttc
    mqttc = paho.Client()                                       # mqttc object
    mqttc.on_connect = on_connect                               # assign on_connect func
    mqttc.on_message = on_message
    mqttc.on_disconnect = on_disconnect                               # assign on_message func    
    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      # pass parameters
    
    mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
    newthread(mqttc.loop_forever,())                                        # Start receiving in loop

def subscribe(topic):
    mqttc.subscribe(topic)
    print ("subscribed to"+topic)


def publish(topic,message):
    mqttc.publish(topic,message,qos=1)
