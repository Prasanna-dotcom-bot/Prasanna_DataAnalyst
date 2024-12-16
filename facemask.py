import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
st.set_page_config(page_title="MASK DETECTION SYSTEM",page_icon="https://w7.pngwing.com/pngs/340/263/png-transparent-computer-icons-facial-recognition-system-face-detection-face-perception-face-recognition-technology-face-text-photography.png")
st.title("FACE MASK DETECTION SYSTEM")
st.sidebar.image("C:/Users/sande/Desktop/side.png")
choice=st.sidebar.selectbox("My Menu",("HOME","IP CAMERA","CAMERA"))
if(choice=="HOME"):
   st.image("https://www.easetrack.com/wp-content/uploads/2023/11/faceRecognition.gif")
   st.write("This Application is developed by Prasanna")
elif(choice=="IP CAMERA"):
   url=st.text_input("Enter IP Camera URL")
   btn=st.button("Start Detection")
   window=st.empty()
   if btn:
      vid=cv2.VideoCapture(url)
      btn2=st.button("stop detection")
      if btn2:
          vid.release()
          st.rerun()
      facemodel=cv2.CascadeClassifier("face.xml")
      maskmodel=load_model("model.h5",compile=False)
      i=1
      while(True):
        flag,frame=vid.read()
        if(flag):
           faces=facemodel.detectMultiScale(frame)
           for(x,y,l,w)in faces:
              face_img=frame[y:y+w,x:x+l]
              face_img=cv2.resize(face_img,(224,224),interpolation=cv2.INTER_AREA)#resize the image
              face_img=np.asarray(face_img,dtype=np.float32).reshape(1,224,224,3)#reshape the image
              face_img=(face_img/127.5)-1#normalize the image
              pred=maskmodel.predict(face_img)[0][0]
              #print(pred)
              if(pred>0.9):
                 cv2.rectangle(frame,(x,y),(x+l,y+w),(0,255,0),3)
              else:
                 path="data/"+str(i)+".jpg"
                 cv2.imwrite(path,frame[y:y+w,x:x+l])
                 i=i+1
                 cv2.rectangle(frame,(x,y),(x+l,y+w),(0,0,255),3)
           window.image(frame,channels="BGR")
elif(choice=="CAMERA"):
   cam=st.selectbox("choose 0 for primary camera and 1 for secondary camera",(0,1,2,3))
   btn=st.button("Start Detection")
   window=st.empty()
   if btn:
      vid=cv2.VideoCapture(cam)
      btn2=st.button("stop detection")
      if btn2:
          vid.release()
          st.rerun()
      facemodel=cv2.CascadeClassifier("face.xml")
      maskmodel=load_model("model.h5",compile=False)
      i=1
      while(True):
        flag,frame=vid.read()
        if(flag):
           faces=facemodel.detectMultiScale(frame)
           for(x,y,l,w)in faces:
              face_img=frame[y:y+w,x:x+l]
              face_img=cv2.resize(face_img,(224,224),interpolation=cv2.INTER_AREA)#resize the image
              face_img=np.asarray(face_img,dtype=np.float32).reshape(1,224,224,3)#reshape the image
              face_img=(face_img/127.5)-1#normalize the image
              pred=maskmodel.predict(face_img)[0][0]
              #print(pred)
              if(pred>0.9):
                 cv2.rectangle(frame,(x,y),(x+l,y+w),(0,255,0),3)
              else:
                 path="data/"+str(i)+".jpg"
                 cv2.imwrite(path,frame[y:y+w,x:x+l])
                 i=i+1
                 cv2.rectangle(frame,(x,y),(x+l,y+w),(0,0,255),3)
           window.image(frame,channels="BGR")
        
           
          
   
