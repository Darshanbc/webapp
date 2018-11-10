from flask import Flask, render_template, flash, request, redirect, url_for,jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf.csrf import CSRFProtect
import os
import dbops
import register
import hashlib
import camera
import pubsub
import time
import json
# App config.
csrf = CSRFProtect()
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 

@app.route('/',methods=['GET'])
def home():
    form = ReusableForm(request.form)
    print form.errors
    print request.form 
    if not(pubsub.initStatus):
        pubsub.init()
    # pubsub.subscribe("test")
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def signup():
    form = ReusableForm(request.form)
    print form.errors
    print request.form
    attr={}
    if request.method == 'POST':
        attr['fname']=request.form['fname']
        attr['lname']=request.form['lname']
        attr['uname']=request.form['uname']
        password=request.form['password']
        phash=hashlib.sha256()
        hashobj=register.twoWordHash(attr['uname'],password)
        attr['PassHash']=hashobj.getHash()
        message=register.signup(attr)
        print message
        return message
        # return render_template('login.html', form=form, status_msg=message)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = ReusableForm(request.form)
    print form.errors
    print request.form
    attr={}
    if request.method=='POST':
        attr['uname']=request.form['uname']
        password=request.form['password']
        print str(attr)+" "+str(password)

        authResult=register.authcreds(attr['uname'],password) 
        if authResult:
            return render_template('demo.html', form=form)
        else:
            return render_template('login.html',form =form ,auth_msg="authentication Failed")

@app.route("/capture",methods=['GET'])
def capture():
    imgName=camera.capture()
    # # closeTime=time.time()+15
    while not(camera.uploadStatusCam1 and camera.uploadStatusCam2):
        time.sleep(3)
        pass
    camera.uploadStatusCam1=camera.uploadStatusCam2=False
    resp["front"]="https://s3-us-west-2.amazonaws.com/agricert.resources/images/"+imgName
    resp["back"]="https://s3-us-west-2.amazonaws.com/agricert.resources/images/back-"+imgName
    return json.dumps(resp)
    
@app.route('/getIcons',methods=['GET'])
def getIcons():
        imgpath='./images/image_icon.png'
        return imgpath
    # return redirect(url_for('refresh_Camera'),cap_image="./images/image_icon.png",analysis_image="./images/image_icon.png",camStatus=message)

@app.route('/pingCamera',methods=['GET'])
def pingCamera():
    response=camera.isConnected()
    print "ping status"+response
    return response

@app.route("/analyse",methods=['GET'])
def analyse():
        imgObj=camera.getAnalysedImage()
        hist= imgObj["image-hist"]
        red=imgObj['image-red']
        imgObj["image-hist"]="https://s3-us-west-2.amazonaws.com/agricert.resources/images/"+hist
        imgObj["image-red"]="https://s3-us-west-2.amazonaws.com/agricert.resources/images/"+red
        return json.dumps(imgObj)
if __name__ == "__main__":
    app.run(port=3000)
    

