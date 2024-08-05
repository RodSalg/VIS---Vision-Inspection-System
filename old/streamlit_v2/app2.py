from ultralytics import YOLO
import cv2
import numpy as np
from ultralytics.utils.plotting import Annotator
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, date
from source.class_OPCUA import Opcua
from source.DAO import DAO
from threading import Thread
from time import time
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, VideoProcessorBase, WebRtcMode


print('Abrindo o modelo')

model = YOLO('yolov8n.pt')


ip = '172.21.7.1' #IP da PRESS
PRESS = Opcua(ip)

database = DAO()

st.set_page_config( layout = 'wide', page_title = "VIS Project")


RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

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


class Faceemotion(VideoTransformerBase):
    
    def transform(self, frame):

        frame = frame.to_ndarray(format="bgr24")

        resposta_sensor = get_estado_sensor(PRESS)

        if resposta_sensor == False: #borda de descida

            estado = 0
        
        if estado == 0:
        
            if (resposta_sensor == True): #borda de subida
                
                estado = 1

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

        return frame

def main():

    # Face Analysis Application #

    a1, a2 = st.columns([100, 200])

    logo = Image.open('images/ufam.png')
    logo = logo.resize((100, 130))

    a1.image(logo)

    a2.title("VIS - VISION INSPECTION SYSTEM")

    options = ["Home", "VIS - Program", "Dashboard", "Sobre"]

    choice = st.sidebar.selectbox("MENU", options)
    
    st.sidebar.markdown("Selecione a página")
    

    if choice == "Home":

        st.title('HOME PAGE')

    elif choice == "VIS - Program":
        
        st.header("IMAGEM DO PROCESSO")
        st.write("CLIQUE EM START PARA INICIAR O VIS")

        tab1, tab2 = st.columns(2)

        with tab1:

            webrtc_streamer(key="example", 
                            mode=WebRtcMode.SENDRECV, 
                            rtc_configuration=RTC_CONFIGURATION,
                            video_processor_factory=Faceemotion)
        
        with tab2:

            data = {
                'Nome': np.random.choice(['Alice', 'Bob', 'Charlie', 'David'], 10),
                'Idade': np.random.randint(18, 65, 10),
                'Pontuação': np.random.randint(0, 100, 10)
            }

            df = pd.DataFrame(data)

            # Exibindo a tabela no Streamlit
            st.bar_chart(df)



    elif choice == "Sobre":

        st.subheader("Sobre o projeto")
        
        html_temp_about1= """<div style="background-color:#6D7B8D;padding:10px">
                                    <h4 style="color:white;text-align:center;">
                                    É um projeto de gradução.</h4>
                                    </div>
                                    </br>"""
        
        st.markdown(html_temp_about1, unsafe_allow_html=True)

        html_temp4 = """
                             		<div style="background-color:#98AFC7;padding:10px">
                             		<h4 style="color:white;text-align:center;">De Thiago Rodrigo Monteiro Salgado. </h4>
                             		</div>
                             		<br></br>
                             		<br></br>"""

        st.markdown(html_temp4, unsafe_allow_html=True)

    else:
        
        pass


if __name__ == "__main__":

    main()
