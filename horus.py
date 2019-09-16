#!/usr/bin/python3


#Atualizacao de teste v2

import cv2
import imutils
from datetime import datetime
import requests
import json

file1 = open("contagem.txt", "r+")
file1.seek(37)
contagem = (file1.read(6))

#ContadorSaidas = int(contagem)
ContadorSaidas=0

attempts = 0
status = 400


face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_frontalface_alt2.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_upperbody.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/cascadeH5.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/models/upperbody_recognition_model.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_profileface.xml")

videoPath = "/home/pi/tem.mp4"
#cap = cv2.VideoCapture(videoPath)
cap = cv2.VideoCapture(0)

bboxes = []
bbox=[]
boxes = []

frame_largura = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_altura =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

numFaces=0
numMov=0
coord=[]
track=False
seg=4
a=0
areaMin=50000
areaMax=150000
tempoIni = datetime.now()

objectID=0
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg = cv2.createBackgroundSubtractorMOG2(history = 6, varThreshold = 56, detectShadows = False)
#fgbg = cv2.createBackgroundSubtractorKNN()
#fgbg = cv2.createBackgroundSubtractorMOG2()
#multiTracker = cv2.MultiTracker_create()

def track_system():
    
    success, boxes = multiTracker.update(frame)
    return boxes

while(True):
    
    flag=0
    #area=0
    ok=None
    
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dim= cv2.GaussianBlur(gray, (7, 7), 0)
    fgmask = fgbg.apply(dim)
    if(numMov==0):
      
      (x, y, w, h) = cv2.boundingRect(fgmask) #x e y: coordenadas do vertice superior esquerdo
      area=w*h
    #200000 eh um valor grande
      if(area > areaMin and area < areaMax):
        #tempoIni = datetime.now()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 1)
        numMov=1
        coord=(x+60,y+60,w-80,h-90)
        
        
      else:
        numMov=0
        
    if(numFaces < numMov and flag==0):
      
      numFaces=1+numFaces
       
      flag=1
      
    
    '''
    print(coord)
    print(numMov)
    print(flag)
    '''
    if numMov != 0 and flag == 1 :
        tempoIni = datetime.now()
        bbox=tuple(coord)
        bboxes.append(bbox)
        tracker = cv2.TrackerMedianFlow_create()
        multiTracker = cv2.MultiTracker_create()
        for bbox in bboxes:
          
          multiTracker.add(tracker, frame, bbox) 
          
          track = True
    
        
    flag_anterior = flag        
    
    if track == True:
      
      
      timeOut=datetime.now()-tempoIni
      boxes = track_system()
      
      #print(boxes)
       
      for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 1, 1)
        cv2.putText(frame, "rastreando ...", (int(newbox[0]+100), int(newbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 0), 2)
        
        movement= abs((newbox[1]-60) - y)
        #print(y)
        #print(movement)
        
        #valor timeOut e movimento deve ser ajustado empiricamente
        if((timeOut.seconds >2 and movement < 60) or timeOut.seconds > 5 ):
          tracker.clear()
          flag=0
          numFaces-=1
          numMov=0
          track=False
          bboxes.remove(bbox)
        
        #if(int(newbox[1] + newbox[3]) > 460 ):
        if(int(newbox[1]) > 350 ):
          ok=1
          attempts = 0
          flag = 1
          coordF=tuple(newbox)
          seg=abs((newbox[1])-(bbox[1]))
          print(seg)
          if (flag > flag_anterior and seg > 30):
            ContadorSaidas +=1  
          
          
          tracker.clear()
          
           
          track=False
          
      boxes=[]
    
    if ok ==1:
        
        flag=0
        numFaces-=1
        numMov=0
        bboxes.remove(bbox)
    
          
    cv2.putText(frame, "Contagem: {}".format(str(ContadorSaidas)), (30, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
              
                    #cv2.rectangle(frame, (x_, y_), (x1, y1), (255, 0, 100), 2)
                 
    cv2.putText(frame, "Pessoas detectadas: {}".format(str(numFaces)), (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 55), 2)
    #cv2.putText(frame, "x: {}".format(str(numFaces)), (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 55), 2)
    file1 = open("contagem.txt", "w")
    #salva registros txt
    L = ["Id: "+str(objectID)+" \n", "Flag: "+str(flag)+" \n", "Contagem:"  +str(ContadorSaidas)+" \n"]

    file1.write("Registros: \n")
    file1.writelines(L)
    file1.close()
    
    
         
    cv2.putText(frame, "Entrada da loja", (450, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (250, 255, 55), 2)
    cv2.line(frame, (0,270), (frame_largura ,270), (250, 255, 55), 1)       
    cv2.putText(frame, "Pressione ESC para sair", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 100), 2)
    #cv2.imshow('frame_masc',fgmask)
    cv2.imshow("frame", frame)
    
    
    if cv2.waitKey(1) == 27 & 0xFF :
        
        break
    
cap.release()  
cv2.destroyAllWindows()
