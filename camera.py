import pubsub
import time
import dbops
uploadStatusCam1=uploadStatusCam2=False
def isConnected():
    if not(pubsub.initStatus):
        pubsub.init()
        time.sleep(1)
    global statusCam1
    global statusCam2
    statusCam1=statusCam2=False
    pubsub.publish(getpingTopic(),"")
    closeTime=time.time()+6
    while True:
        if (statusCam1 and statusCam2) or time.time() > closeTime:
            break
    return str(statusCam1 and statusCam2)

def setStatus(msg):
    global statusCam1
    global statusCam2
    if str(msg)=="Camera1":
        statusCam1=True
    elif str(msg)=="Camera2":
        statusCam2=True

def capture():
    imgName=str(int(time.time()))+".png"
    obj=dbops.dbConn()
    obj.operation("insert_image")
    obj.insert({"image":imgName,"image-hist":"hist-"+imgName,"image-red":"red_comp_"+imgName})
    pubsub.publish("agricert/capture",imgName)
    print ("cappture method")
    return imgName

# def isUploaded():
#     global uploadStatusCam2
#     global uploadStatusCam1
    
#     if  uploadStatusCam1 and  uploadStatusCam2:
#         # print "upload=true"
#         return not( uploadStatusCam1)
#     else:
#         # print "upload =false"
#         return uploadStatus
#     print ("isuopload method")

def setUploadStatus(msg):
    global uploadStatusCam2
    global uploadStatusCam1
    print ("seting UploadStatus")
    if msg=="Camera1":
        uploadStatusCam1=True
    elif msg=="Camera2":
        uploadStatusCam2=True

def getpingTopic():
    return pingTopic

def setpingTopic():
    global pingTopic
    pingTopic="agricert/pingRpi"

def getAnalysedImage():
    obj=dbops.dbConn()
    obj.operation("insert_image")
    return obj.queryRecentAddedItem()
setpingTopic()