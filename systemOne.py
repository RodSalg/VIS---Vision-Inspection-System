import cv2
import time
import threading
from source.class_PDI import Processamentos
from source.class_analisa_gap import Gap

# ----- Functions -----

sensor_capacitivo = False

def simulador_OPCUA():

    global sensor_capacitivo

    contador = 0
    
    while True:

        contador = contador + 1

        time.sleep(2)

        if contador == 5:

            contador = 0

            print('Ativando esteira')

            sensor_capacitivo = True

            time.sleep(1)

            print('Desativando esteira')

            sensor_capacitivo = False
            



# ---- configurando variáveis ----

gap = Processamentos()


thread_esteira = threading.Thread(target = simulador_OPCUA)

thread_esteira.start()
            


print('abrindo a camera')
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_SATURATION, 255)
cap.set(cv2.CAP_PROP_SHARPNESS, 255)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 60)

print('camera aberta')

while True:

    _, frame = cap.read()     

    cv2.imshow('Extraindo informações da esteira', frame)   
    cv2.imwrite('teste.bmp', frame)
    
    if(sensor_capacitivo == True):

        print('Iniciando Análise do GAP')

        inicio = time.time()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        testando = Gap()

        testando.main(gray_frame)

        # resultado = gap.processamento_de_imagem(gray_frame, 20, 50)
        
        # cv2.imwrite('resultado2.bmp', resultado)
        
        fim = time.time()

        print('tempo do processo: ', (fim - inicio))
    
    if cv2.waitKey(1) & 0xFF == ord(' '):

        break

cv2.destroyAllWindows()
