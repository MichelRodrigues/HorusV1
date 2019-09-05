#!/usr/bin/python3


#Atualizacao de teste

import numpy as np
import cv2
import imutils
from datetime import datetime
import requests
import json

file1 = open("contagem.txt", "r+")
file1.seek(37)
contagem = (file1.read(6))

ContadorSaidas = int(contagem)
#ContadorSaidas=0

attempts = 0
status = 400


face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_frontalface_alt2.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/models/upperbody_recognition_model.xml")
#face_cascade1 = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_profileface.xml")

videoPath = "/home/pi/teste.mp4"
#cap = cv2.VideoCapture(videoPath)
cap = cv2.VideoCapture(0)

bboxes = []
bbox=[]
boxes = []

frame_largura = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_altura =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

numFaces=0
coord=[]
track=False
seg=4
a=0
tempoIni = datetime.now()

objectID=0

#multiTracker = cv2.MultiTracker_create()

def track_system():
    
    success, boxes = multiTracker.update(frame)
    return boxes

while(True):
    flag=0
    
    ok=None
    
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if(numFaces==0):
       
      faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    
      a=len(faces)
    
    '''  
    if faces_cont == 0:
          timeOut = datetime.now() - tempoIni
        else:
          tempoIni = datetime.now()
    '''
    if(numFaces < a and flag==0):
      
      numFaces=1+numFaces
      
      for (x,y,w,h) in faces:
        coord=(x,y,w,h+40)
        
      
      flag=1 
    
    if a != 0 and flag == 1:
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
        #cv2.rectangle(frame, p1, p2, (255,0,0), 1, 1)
        cv2.putText(frame, "rastreando ...", (int(newbox[0]+150), int(newbox[1])), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 0), 2)
        
        movement= abs(newbox[1] - y)
        #print(movement)
        
        #valor timeOut e movimento deve ser ajustado empiricamente
        if((timeOut.seconds >2 and movement < 50) or timeOut.seconds >5 ):
          tracker.clear()
          flag=0
          numFaces-=1
          track=False
          bboxes.remove(bbox)
        
        if(int(newbox[1] + newbox[3]) > 460 ):
          ok=1
          attempts = 0
          flag = 1
          coordF=tuple(newbox)
          seg=abs(newbox[1]-bbox[1])
          if (flag > flag_anterior and seg > 3):
            ContadorSaidas +=1  
          
          
          tracker.clear()
          
           
          track=False
          
      boxes=[]
    
    if ok ==1:
        
        flag=0
        numFaces-=1
        
        bboxes.remove(bbox)
    '''
    
    if (ok != None and attempts == 0):
      ok=None  
      if ( status >= 400 and attempts <=5):
            attempts +=1
            timestamp = datetime.now()
            url = 'http://facesapi.trudata.com.br/api/v1/Login'
            payload = {
                      'userName': 'jedi@hansenautomacao.com',
                      'password': '@H4ns3n!.'
                      }
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            r.status_code
            status = r.status_code
      
            #print(status)
            #print(r.text)

            response = r.json()
      
            token=response.get('accessToken')
      else:
            attempts=1
            url1 = 'http://facesapi.trudata.com.br/api/v1/ReconData/Single'
            ts = timestamp.strftime("%m/%d/%Y %H:%M:%S")
            payload = {
                      "codigo": ContadorSaidas,
                      "cdEmpresa": 2,
                      "cdLocal": 1,
                      "raspId": "ef9f40de-cf83-48f5-b360-e5d269bbe71a",
                      "idadeAprox": 23,
                      "genero": "M",
                      "horarioRecon": ""+str(ts)+""
                      }
            head = {'Authorization': 'Bearer ' + token,'content-type': 'application/json'}
            recon = requests.post(url=url1, data=json.dumps(payload), headers=head)
            Tstatus = recon.status_code
            
            if (Tstatus > 200):
              cv2.putText(frame, "Erro no envio", (5, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
              time.sleep(5)
              break
            else:
              cv2.putText(frame, "Registro enviado para a nuvem!...", (5, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    '''        
    cv2.putText(frame, "Contagem: {}".format(str(ContadorSaidas)), (5, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
              
                    #cv2.rectangle(frame, (x_, y_), (x1, y1), (255, 0, 100), 2)
                 
    cv2.putText(frame, "Pessoas detectadas: {}".format(str(numFaces)), (5, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 55), 2)
    file1 = open("contagem.txt", "w")
    #salva registros txt
    L = ["Id: "+str(objectID)+" \n", "Flag: "+str(flag)+" \n", "Contagem:"  +str(ContadorSaidas)+" \n"]

    file1.write("Registros: \n")
    file1.writelines(L)
    file1.close()
    
    
         
    cv2.putText(frame, "Entrada da loja", (450, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (250, 255, 55), 2)
    cv2.line(frame, (0,270), (frame_largura ,270), (250, 255, 55), 1)       
    cv2.putText(frame, "Pressione ESC para sair", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 100), 2)
    
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) == 27 & 0xFF :
        
        break
    
cap.release()  
cv2.destroyAllWindows()
