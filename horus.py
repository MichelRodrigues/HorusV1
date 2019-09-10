#!/usr/bin/python3


#Apenas para testes

import numpy as np
import cv2
#cap = cv2.VideoCapture("/home/pi/teste.mp4")
cap = cv2.VideoCapture(0)
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg = cv2.createBackgroundSubtractorKNN()
contador=0
flag=0
inc=0
while(1):
    flag=0
    flag_anterior=flag
    ret, frame = cap.read()
    dim = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dim= cv2.GaussianBlur(dim, (7, 7), 0)
    fgmask = fgbg.apply(dim)
    (x, y, w, h) = cv2.boundingRect(fgmask) #x e y: coordenadas do vertice superior esquerdo
    
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
    ''' #w e h: respectivamente largura e altura do retangulo
    
    if(y>=400):
      flag=1
            
    if (flag != flag_anterior ):
      contador +=1
      flag=0
      flag_anterior=0
      
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
    cv2.putText(frame, "Pressione ESC para sair", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 100), 2)
    cv2.putText(frame, "Cont. desativado: {}".format(str(contador)), (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    #cv2.imshow('frame',fgmask)
    cv2.imshow('frameloco',frame)
    if cv2.waitKey(1) == 27 & 0xFF :
        
      break
    
cap.release()  
cv2.destroyAllWindows()
   