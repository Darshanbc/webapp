from picamera import PiCamera
import pubsub
import upload
import cv2
import matplotlib
matplotlib.use("Pdf")
from matplotlib import pyplot as plt
def cameraInit(CameraName):
    global camera
    global msg
    global CamName
    CamName=CameraName
    try:
        camera=PiCamera()
        
        msg=CamName
    except:
        msg="disconnected"
        print ("camera not connected")
    return msg

def camStaus():
    global camera
    # camera._init_defaults
    print ("exception status "+str(camera._camera_exception))
    print ("message "+msg)
    if camera._camera_exception==None and msg!="disconnected":
        pubsub.publish("agricert/pingBack",CamName)
    else:
        pubsub.publish("agricert/pingBack","disconnected")

def capture(fileName):
    global msg
    if camera._camera_exception==None and msg!="disconnected":
        camera.capture("./images/"+fileName)
        upload.Upload(filePath="./images/"+fileName,filename= fileName,topic="agricert/image/uploadStatus")

    else:
        pubsub.publish("agricert/pingBack","disconnected")

def Analyse(fileName):
    img=cv2.imread('./images/'+fileName)
    cv2.imwrite("./images/red_comp_"+fileName,img[:,:,2])
    y=img[:,:,2].mean(axis=0)
    xAxis=[i for i in range(len(y))]
    plt.plot(xAxis,y)
    plt.xlabel("width of Image in pixels")
    plt.ylabel("Average of Red component along the columns")
    plt.title("Average of Red component v/s pixel density")
    plt.savefig("./images/hist-"+fileName)
    upload.Upload(filePath="./images/hist-"+fileName,filename="hist-"+fileName,topic="agricert/hist")
    upload.Upload(filePath="./images/red_comp_"+fileName,filename="red_comp_"+fileName,topic="agricert/red_comp")
