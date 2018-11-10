import pubsub
import upload
import rpiCamera
import argparse
parser = argparse.ArgumentParser(prog="Client Program to run on Raspberry pi")
parser.add_argument('-c', '--cam',
            action="store", dest="cam",required=True,
            help="Enter Camera ID, Camera1 or Camera2")
args = parser.parse_args()
camName=args.cam
initStatus=rpiCamera.cameraInit(camName)
print ("Camera init Status "+initStatus) 
pubsub.init()
# pubsub.subscribe("agricert/capture")
# upload.upload("./images/text.txt","text.txt")
while True:
    pass