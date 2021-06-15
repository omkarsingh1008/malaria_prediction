from types import MethodDescriptorType
from flask.json import jsonify
from flask.wrappers import Request
import tensorflow as tf
import cv2
from flask import Flask, render_template , app, request
import os
UPLOAD_FOLDER='upload_image'
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_image',methods=['POST','GET'])
def predict():
    if request.method=='POST':
        file=request.files['fileToUpload']
        if file:
            filename=file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    model = tf.keras.models.load_model("mymodel")
    img=cv2.imread(UPLOAD_FOLDER+'/'+filename)
    img=img/255
    img=cv2.resize(img,(100,100))
    img=img.reshape(1,100,100,3)
    pre=model.predict(img)
    label=['Parasitized','Uninfected']
    result=dict(zip(label,pre[0]))
    return render_template('predict.html',result=result)
if __name__=='__main__':
    app.run('localhost',8016,debug=True)
       