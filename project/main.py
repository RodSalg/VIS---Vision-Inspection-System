from ultralytics import YOLO
import cv2
import time
from ultralytics.utils.plotting import Annotator
from source.class_OPCUA import Opcua
from source.DAO import DAO


# ------------------- FUNÇÕES ----------------------
# -------------------------------------------------- 


def get_estado_esteira(press_opcua: Opcua) -> bool:

    '''
    
        Utilizando-se da classe OPC UA, pega o valor atual do que a esteira está fazendo. 
        True: ela está ativada,
        False: desativada.

        :param
            opcua_object
        
        :return
            estado_esteira
    
    '''

    node = 'xBG6'
    resultado = press_opcua.get_value(node)

    return resultado


# ---------------------- MAIN ----------------------
# --------------------------------------------------

if __name__ == '__main__':


    # --------------- Objetos e variáveis --------------
    # --------------------------------------------------   

    # ip = 'opc.tcp://172.21.7.1:4840' #IP da PRESS
    # press = Opcua(ip)
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


    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    print('Iniciando Aplicacao...\n')

    while True:

        _, img = cap.read()

        #identifica o estado da esteira
        # estado_esteira = get_estado_esteira(press)
        estado_esteira = True
        
        if (estado_esteira == True):
        
            results = model.predict(img)

            annotator = Annotator(img)
            
            for r in results:

                boxes = r.boxes
                
                print('numero de boxes: ', len(boxes))

                for box in boxes:

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

                    if label == 'CORRETO':

                        color = (0, 255, 0)
                        result = True

                    elif label == 'INCORRETO':

                        color = (255, 0, 0)
                        result = False

                    annotator.box_label(b, label, color)
                    
                    database.insert_gap_result(result)
                    break #arranjar forma melhor de parar (quero somente o primeiro, usar [0])

                img = annotator.result()

                

                break
                
                

            scale_percent = 150

            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)

            dim = (width, height)
            
            imagem_saida = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)   

            cv2.imshow('Sistema de inspecao', imagem_saida)
    

        if cv2.waitKey(1) & 0xFF == ord(' '):

            break

    cv2.destroyAllWindows()
