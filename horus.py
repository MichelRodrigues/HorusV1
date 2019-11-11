#!/usr/bin/python3

import crud_utils
import cv2
from datetime import datetime
import requests
import json

face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_frontalface_alt2.xml")

videoPath = "/home/pi/tim.mp4"
#cap = cv2.VideoCapture(videoPath)
cap = cv2.VideoCapture(0)

ContadorSaidas=0
bboxes = []
bbox=[]
boxes = []
tempoIni = datetime.now()
tempoIni1 = datetime.now()
tempoIni2 = datetime.now()
b=0
face_ja=0
a =0
beta=0
flag=0
numFaces = 0
frame_altura =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
flag1=0
flag2=0
soma=0
soma1=0
soma2=0

while True:
      face_anterior = a
            
      ret, frame = cap.read()
      frame = cv2.flip(frame, 0)
      
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
      
      faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    
      a=len(faces)
      
      for (x,y,w,h) in faces:
          
          coord=(x+10,y+20,w-20,h+40)    
          bbox=tuple(coord)
          cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 1, 1)
      
      while(numFaces < a):
          numFaces=a+numFaces  
         
      if(face_anterior < a ):
        tempoIni = datetime.now()
        
        bboxes.append(bbox)
        
        if (bbox[1] < 260):
          b=a
      
      if(a > 0):
        tempoIni1 = datetime.now()
        tempoIni2 = datetime.now()
        if(bbox[1] > 300 and  bbox[0]>100 and  bbox[0] < 250):
            flag1 = 1
            
        
        if(bbox[1] > 300 and  bbox[0]>300 and  bbox[0] < 400):
            flag2 = 1
            
       
      
      if(a <b):
          
          timeOut = datetime.now()-tempoIni
          
          
          if(timeOut.seconds >= 6):
             
             if(b <= numFaces): 
               ContadorSaidas=b+ContadorSaidas
               crud_utils.inserir_dado(2, 2, 'd3f2d810-1193-4cef-8a7a-971890a4157d', ContadorSaidas)
               print("enviado")
               numFaces=0
      
      if(a < flag1 or a < flag2 ):
          timeOut1 = datetime.now()-tempoIni1
          timeOut2 = datetime.now()-tempoIni2
          
          if(timeOut1.seconds >= 6):
            soma1 = flag1 + soma1
            crud_utils.inserir_dado(2, 1, 'ef9f40de-cf83-48f5-b360-e5d269bbe71a', soma)
            
            flag1=0
          if(timeOut2.seconds >= 6):
            soma2 =  flag2 + soma2
            
            
            flag2=0  
          
      
      soma = soma1+soma2
      
      cv2.putText(frame, "Ultimos visitantes do estande: {}".format(str(b)), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
      cv2.putText(frame, "Total de visitantes: {}".format(str(ContadorSaidas)), (5, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
      cv2.putText(frame, "Total de visitantes nos simuladores: {}".format(str(soma)), (5, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
      #simulador 1
      cv2.putText(frame, "Simulador 1", (5, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (250, 255, 55), 2)
      cv2.putText(frame, "{}".format(str(flag1)), (80, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (250, 255, 55), 2)

      cv2.line(frame, (100,300), (100 ,frame_altura), (250, 255, 55), 2)
      cv2.line(frame, (250,300), (250 ,frame_altura), (250, 255, 55), 2)
    
    
      #simulador 2
      cv2.putText(frame, "Simulador 2", (460, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
      cv2.putText(frame, "{}".format(str(flag2)), (520, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

      cv2.line(frame, (300,300), (300 ,frame_altura), (0, 0, 255), 2)
      cv2.line(frame, (460,300), (460 ,frame_altura), (0, 0, 255), 2)   
    
      #cv2.putText(frame, "Pressione ESC para sair", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 100), 2)
      cv2.putText(frame, "Horus V1.0", (5, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, (0, 0, 255), 2)
      #cv2.putText(frame, "Total de usuarios: {}".format(str(ContadorSaidas)), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
      cv2.imshow("Trudata - Rota simuladores", frame)
      
    
    
      if cv2.waitKey(1) == 27 & 0xFF :
        
          break
    
cap.release()  
cv2.destroyAllWindows()
