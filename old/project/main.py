from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
from source.class_OPCUA import Opcua
from source.DAO import DAO
from datetime import datetime, date
from threading import Thread
from time import time


# ------------------- FUNÇÕES ----------------------
# -------------------------------------------------- 

def get_estado_sensor(press_opcua: Opcua) -> bool:

    '''
    
        Utilizando-se da classe OPC UA, pega o valor atual do que a esteira está fazendo. 
        True: ela está ativada,
        False: desativada.

        :param
            opcua_object
        
        :return
            estado_esteira
    
    '''

    node = 'xBG6' #nó do sensor capacitivo
    resultado = press_opcua.get_value(node)

    return resultado

def get_hora_atual():

    horario_atual = datetime.now()

    hora = horario_atual.strftime("%H")
    min = horario_atual.strftime("%M")
    seg = horario_atual.strftime("%S")
    dia = date.today().day
    mes = date.today().month
    ano = date.today().year

    timestamp = "{}{}{}_{}{}{}".format(dia, mes, ano, hora, min, seg)

    return timestamp


def save_image(imagem, resultado): #vai rodar de forma assincrona

    horario = get_hora_atual()

    filename = 'results/{}.bmp'.format(horario)
    #sendDataBase

    print(filename)
    cv2.imwrite(filename, imagem)



# ---------------------- MAIN ----------------------
# --------------------------------------------------

estado = 0

if __name__ == '__main__':


    # --------------- Objetos e variáveis --------------
    # --------------------------------------------------   

    ip = '172.21.7.1' #IP da PRESS
    PRESS = Opcua(ip)

    database = DAO()


    # -------------- Abrindo o modelo ------------------
    # --------------------------------------------------

    try:

        print('Abrindo o modelo')

        model = YOLO('models/best.pt')

    except ValueError as e:

        print('Erro ao abrir o modelo: ', e)

    finally:

        print('Modelo aberto com sucesso!')

    # ----------------- Abrindo e configurando a camera ------------------
    # --------------------------------------------------------------------
        

    foco = 40 #foco bom na planta

    print('abrindo a camera')

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # cap.set(cv2.CAP_PROP_SATURATION, 255)
    # cap.set(cv2.CAP_PROP_SHARPNESS, 255)

    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cap.set(cv2.CAP_PROP_FOCUS, foco)   

    print('camera aberta')

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    print('Iniciando Aplicacao...\n')

    tempo_total = 0    

    while True:

        _, img = cap.read()

        resposta_sensor = get_estado_sensor(PRESS)

        if resposta_sensor == False: #borda de descida

            estado = 0
        
        if estado == 0:
        
            if (resposta_sensor == True): #borda de subida
                
                estado = 1

                final = time()

                results = model.predict(img)

                annotator = Annotator(img)

                contador = 0
                
                for r in results:

                    boxes = r.boxes
                    
                    print('numero de boxes: ', len(boxes))

                    for box in boxes:
                        
                        registro = 0

                        b = box.xyxy[0] 
                        c = box.cls 
                        
                        print(model.names[int(c)])
                        
                        # if model.names[int(c)] == 'CORRETO':

                        x = int(b[0])  # Valor x
                        y = int(b[1])  # Valor y
                        w = int(b[2])  # Largura
                        h = int(b[3])  # Altura

                        # print('coordendas: {}, {}, {}, {}'.format(x, y, w, h))
                        
                        # print(b) bound box puro

                        label = model.names[int(c)]

                        registro = 0

                        if label == 'CORRETO':
                            
                            resultado = 'CORRETO'

                            color = (0, 255, 0)

                            registro = 1
                            

                        elif label == 'INCORRETO':

                            resultado = 'INCORRETO'

                            color = (0, 0, 255)

                            registro = 1
                        
                        if registro == 1:

                            #upo para o banco
                            dataSave = Thread(target = save_image, args = (img, resultado))
                            dataSave.start()


                        annotator.box_label(b, label, color)

                        img = annotator.result()


            
        # scale_percent = 150

        # width = int(img.shape[1] * scale_percent / 100)
        # height = int(img.shape[0] * scale_percent / 100)

        # dim = (width, height)
        
        # imagem_saida = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)   

        cv2.imshow('Sistema de inspecao', img)
    

        if cv2.waitKey(1) & 0xFF == ord(' '):

            break

    cv2.destroyAllWindows()
