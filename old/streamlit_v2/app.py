from ultralytics import YOLO
import cv2
import numpy as np
import subprocess
import sys
import os
from ultralytics.utils.plotting import Annotator
import streamlit as st
import pandas as pd
from PIL import Image
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, VideoProcessorBase, WebRtcMode
import threading
import signal



st.set_page_config( layout = 'wide', page_title = "VIS Project")


RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

def run_script(script_path, stop_event):

    process = subprocess.Popen(f'cmd /k python "{script_path}"', shell=True)

    while not stop_event.is_set() and process.poll() is None:
        pass

    # Termina o processo quando a execução é interrompida
    if process.poll() is None:
        os.kill(process.pid, signal.CTRL_BREAK_EVENT)

class Vis(VideoTransformerBase):
    
    def transform(self, frame):

        global model

        frame = frame.to_ndarray(format="bgr24")

        results = model.predict(frame)

        annotator = Annotator(frame)
        
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

                annotator.box_label(b, label)

                frame = annotator.result()

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
    
    aberto = 0

    if choice == "Home":

        st.title('HOME PAGE')

        st.text('BEM VINDO AO MIAUMOCITOOO')
        st.button('atualizar')

        
        aberto = 0

        diretorio_atual = os.getcwd()
        script_alvo_path = os.path.join(diretorio_atual, 'teste.py')

        stop_event = threading.Event()

        if st.button('Conectar ao CLP'):
            st.text('Conexão bem sucedida!')
            # Inicia o script em uma thread separada
            thread = threading.Thread(target=run_script, args=(script_alvo_path, stop_event))
            thread.start()

        if st.button('Interromper Execução'):
            # Define o sinalizador para interromper a execução
            stop_event.set()
            st.text('Execução interrompida!')
            
        # Chama o script_alvo.py em um novo processo
            subprocess.Popen(f'cmd /k python "{script_alvo_path}"', shell=True)
            
            st.text('Conexão bem sucedida!')



    elif choice == "VIS - Program":
        
        st.header("IMAGEM DO PROCESSO")
        st.write("CLIQUE EM START PARA INICIAR O VIS")

        tab1, tab2 = st.columns(2)

        with tab1:

            print('Abrindo o modelo')   
            global model
            
            model = YOLO('yolov8n.pt')
            
            webrtc_streamer(key="example", 
                            mode=WebRtcMode.SENDRECV, 
                            rtc_configuration=RTC_CONFIGURATION,
                            video_processor_factory=Vis)
        
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
