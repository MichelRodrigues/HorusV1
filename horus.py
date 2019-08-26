#!/usr/bin/python3

#Atualizacao 6 (por Michel Rodrigues)
#numero reduzidos de biblioteca
#Detecta e efetua a contagem
#conta e envia os registros para nuvem
#Diminuidos scaleFactor de 1.5 para 1.3
#Contagem com maior qualidade
#Dados e status mostrados na tela
#Numero de contagem impresso na tela
#Removidos framecounter
#arrumado contador que nao estava incrementando corretamente
#retirados boxes que circulam as pessoas
#ajuste da 'linha de referencia' (mais alta) para melhorar a deteccao e rastreio
#A tela limpa servira para estimativa de genero e idade


import cv2
import dlib
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

video_capture = cv2.VideoCapture(0)
#video_capture = cv2.VideoCapture("/home/pi/teste.mp4")

tracker = dlib.correlation_tracker()

detects=[]
tracked = False
numFaces=0
y_=0

coord=[]

tempoIni = datetime.now()

objectID=0

def printa_faces(a,num):
    x,y,w,h = a
          
    end_cord_x = x + w
    end_cord_y = y + h
    cv2.rectangle(image, (x,y), (end_cord_x, end_cord_y), (255,0,0), 1)
    '''
    dlib_rect = dlib.rectangle(x, y, end_cord_x, end_cord_y)
    tracked = True
    tracker.start_track(image, dlib_rect)
    
    track()
    '''

flag=0

while True:
    
    ok=None
    
    ret, frame = video_capture.read()

    if ret:
        image = frame
        
        coord=[]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
        faces_cont=len(faces)
        
        if faces_cont == 0:
          timeOut = datetime.now() - tempoIni
        else:
          tempoIni = datetime.now()
        
         
        
        while(numFaces < faces_cont):
            
          timeOut=datetime.now()-tempoIni
          detects.append(numFaces)
          coord.append(faces)
          #
          #print(coord[0][numFaces])
          a=(coord[0][numFaces])
          numFaces+=1
          tracked= True
          
        if (timeOut.seconds > 7) :
        
          tracked=False
          numFaces=0
        
        
          
        for (x,y,w,h) in faces:
          end_cord_x = x + w
          end_cord_y = y + h
          #cv2.rectangle(image, (x,y), (end_cord_x, end_cord_y), (255,0,0), 1)
          dlib_rect = dlib.rectangle(x, y, end_cord_x, end_cord_y)
          
          tracker.start_track(image, dlib_rect)
          
        if tracked == True:
            
            tracker.update(image)
            track_rect = tracker.get_position()
            x_  = int(track_rect.left())
            y_  = int(track_rect.top())
            x1 = int(track_rect.right())
            y1 = int(track_rect.bottom())
            #cv2.rectangle(image, (x_,y_), (x1,y1), (255,0,0), 1)
            cv2.putText(image, "rastreando" , (int(x_+(x1/2)), int(y_)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 0), 2)
            
            if(y_<90):
              attempts = 0
              flag=0
              
              
            if(y_ > 300 and flag==0):
                
                flag=1
                
                ContadorSaidas = ContadorSaidas + numFaces
                
                numFaces=0
                
                ok=1
                
        if(numFaces==0):
          
          Tracked = False
                  
                
          
    
    cv2.putText(frame, "Contagem: {}".format(str(ContadorSaidas)), (5, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
              
                    #cv2.rectangle(image, (x_, y_), (x1, y1), (255, 0, 100), 2)
    cv2.putText(image, "Pessoas detectadas: {}".format(str(numFaces)), (5, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 55), 2)
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
       # show the current frame.
    cv2.imshow("Output", image)
       
 

    # press "q" to quit the program.
    if cv2.waitKey(1) == 27 & 0xFF :
      break

# cleanup.
video_capture.release()
cv2.destroyAllWindows()
