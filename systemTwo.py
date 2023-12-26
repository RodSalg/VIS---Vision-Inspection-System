from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
import pymysql


# ---------- Camera ----------

print('Abrindo a camera')

try:
    
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    print('Camera aberta')

except cv2.error as e:
    
    print(f'Erro ao abrir a câmera: {e}')

# ---------- Configuração da câmera ----------

try:

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
    cap.set(cv2.CAP_PROP_SATURATION, 255)
    cap.set(cv2.CAP_PROP_SHARPNESS, 255)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cap.set(cv2.CAP_PROP_FOCUS, 105)

except cv2.error as e:

    print(f'Erro ao configurar a câmera: {e}')


while True:

    _, img = cap.read()     

    cv2.imshow('Camera 1', img)

    if cv2.waitKey(1) & 0xFF == ord(' '):

        break

cv2.destroyAllWindows()
