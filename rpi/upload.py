import boto3
import config  as con
from boto3.s3.transfer import S3Transfer
import pubsub
import rpiCamera
#have all the variables populated which are required below
client = boto3.client('s3', aws_access_key_id=con.access_key_id,aws_secret_access_key=con.access_key)
transfer = S3Transfer(client)

def Upload(filePath,filename,topic):
	print ("uploading started")
	transfer.upload_file(filePath,con.bucketName, "images/"+filename)
	print ("upload finished")
	pubsub.publish(topic,rpiCamera.CamName)
	# print "publish "+topic+" successful"





