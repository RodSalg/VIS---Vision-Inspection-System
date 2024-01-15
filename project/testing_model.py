from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator

print('Abrindo o modelo...')
model = YOLO('models/best.pt')
print('Modelo aberto!')



foco = 55 #foco bom na planta

print('abrindo a camera')

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_SATURATION, 255)
cap.set(cv2.CAP_PROP_SHARPNESS, 255)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, foco)

print('camera aberta')


print('Iniciando Aplicacao...\n')

while True:

    _, img = cap.read()
    
    results = model.predict(img)

    annotator = Annotator(img)
    
    for r in results:

        boxes = r.boxes
        
        print('numero de boxes: ', len(boxes))

        for box in boxes:

            b = box.xyxy[0] 
            c = box.cls 

            print(model.names[int(c)])
            
            # if model.names[int(c)] == 'tampinha':

            x = int(b[0])  # Valor x
            y = int(b[1])  # Valor y
            w = int(b[2])  # Largura
            h = int(b[3])  # Altura

            # print('coordendas: {}, {}, {}, {}'.format(x, y, w, h))
            
            # print(b) bound box puro

            if model.names[int(c)] == 'CORRETO':

                nome = 'CORRECT'
                color = (0, 255, 0)

            elif model.names[int(c)] == 'INCORRETO':

                nome = 'INCORRECT'
                color = (255, 0, 0)
            
            else:
                
                nome = model.names[int(c)]

            annotator.box_label(b, nome, color)
                
          
    img = annotator.result()

    scale_percent = 220

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)

    dim = (width, height)
    
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)   

    cv2.imshow('Avaliando Pecas', resized)

    if cv2.waitKey(1) & 0xFF == ord(' '):

        break

cv2.destroyAllWindows()
