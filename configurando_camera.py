import cv2
import time
import threading
from source.class_PDI import Processamentos

def mudando_foco():

    while True:
            
        global foco

        foco = int(input('valor do foco que deseja: '))
                    
foco = 80


th_foco = threading.Thread(target = mudando_foco)

th_foco.start()

print('abrindo a camera')
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
cap.set(cv2.CAP_PROP_SATURATION, 255)
cap.set(cv2.CAP_PROP_SHARPNESS, 255)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, foco)

print('camera aberta')

while True:

    _, frame = cap.read()     

    height, width, _ = frame.shape

    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 0, 255), 2)

    cv2.imshow('Ajeitando posicao da camera', frame)   
    
    cap.set(cv2.CAP_PROP_FOCUS, foco)
    
    if cv2.waitKey(1) & 0xFF == ord(' '):

        break

cv2.destroyAllWindows()
