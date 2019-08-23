#!/usr/bin/python3

#Atualizacao 5 (por Michel Rodrigues)
#Programa somente com o contador
#conta e envia os registros para nuvem
#Diminuidos scaleFactor de 1.5 para 1.1
#Contagem com maior qualidade
#Dados e status mostrados na tela
#Numero de contagem impresso na tela
#Removidos framecounter
#arrumado contador que não estava incrementando corretamente
#retirados boxes que circulam as pessoas
#retirada linha de referência por enquanto para melhorar a detecção e rastreio

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

#cap = cv2.VideoCapture("/home/pi/teste2.mp4")
cap = cv2.VideoCapture(0)

numFaces=0

frame_largura = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_altura =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

y=0

flag=0

tempoIni = datetime.now()

numFaces=0

objectID=0

while(True):
    
    ok=None
  
    ret, frame = cap.read()
    
    #frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    for (x,y,w,h) in faces:
        color = (255,200,0) #BGR
        stroke = 1
        end_cord_x = x + w
        end_cord_y = y + h
        #cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
        if(y>(240)):
            flag=1
            cv2.putText(frame, "Iniciando processo de contagem...", (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        else:
            attempts=0
            flag=0
    
    faces_cont=len(faces)
    
    if faces_cont == 0:
        
        timeOut = datetime.now() - tempoIni
    else:
        tempoIni = datetime.now()
    
    
    while(numFaces < faces_cont):
      timeOut=datetime.now()-tempoIni 
      numFaces+=1
      
    if (timeOut.seconds > 5) :
      
      if(flag==1):  
        ContadorSaidas=ContadorSaidas+numFaces
        ok=1
      numFaces=0
      
    
    cv2.putText(frame, "Contagem: {}".format(str(ContadorSaidas)), (5, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)  
      
    cv2.putText(frame, "Pessoas detectadas: {}".format(str(numFaces)), (5, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 55), 2)
    
    file1 = open("contagem.txt", "w")
    #salva registros txt
    L = ["Id: "+str(objectID)+" \n", "Flag: "+str(flag)+" \n", "Contagem:"  +str(ContadorSaidas)+" \n"]

    file1.write("Registros: \n")
    file1.writelines(L)
    file1.close()
    
    if (ok != None and attempts == 0):
        
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
           
    cv2.putText(frame, "Pressione ESC para sair", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 100), 2)
    cv2.imshow("Output", frame)
    
    if cv2.waitKey(1) == 27 & 0xFF :
      break
cap.release()  
cv2.destroyAllWindows()
    
