from ultralytics import YOLO
import cv2
import numpy as np
from ultralytics.utils.plotting import Annotator
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, date
from source.DAO import VIS_DAO
from PIL import Image
from threading import Thread
from time import time
from keras.preprocessing.image import img_to_array
from streamlit_webrtc import webrtc_streamer
import plotly.express as px
import os
import av
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



st.set_page_config( layout = 'wide', page_title = "VIS - Application")

# ------------------- FUNÇÕES ----------------------
# --------------------------------------------------
 

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


def save_image(imagem, resultado, model): #vai rodar de forma assincrona

    

    horario = get_hora_atual()

    filename = 'results/{}.bmp'.format(horario)

    database.insert_data_db(f'{horario}.bmp', resultado, model)

    #sendDataBase

    print(filename)

    cv2.imwrite(filename, imagem)





def video_frame_callback_tampa(img):

    img = img.to_ndarray(format="bgr24")

    results = model_tampa.predict(img, conf=0.75)

    annotator = Annotator(img)

    
    for r in results:

        boxes = r.boxes
        
        print('numero de boxes: ', len(boxes))

        for box in boxes:
            
            registro = 0

            b = box.xyxy[0] 
            c = box.cls 
            
            label = model_tampa.names[int(c)]

            color = (0, 0, 255)


            



            annotator.box_label(b, label, color)
            annotator.box_label(b, label, color)

            img = annotator.result()

    return av.VideoFrame.from_ndarray(img, format="bgr24")






def video_frame_callback_gap(img):

    img = img.to_ndarray(format="bgr24")

    results = model_gap.predict(img, conf=0.6)

    annotator = Annotator(img)

    
    for r in results:

        boxes = r.boxes
        
        print('numero de boxes: ', len(boxes))

        for box in boxes:
            
            registro = 0

            b = box.xyxy[0] 
            c = box.cls 
            
            label = model_gap.names[int(c)]

            registro = 0

            if label == 'CORRECT':
                
                resultado = 'CORRETO'

                color = (0, 255, 0)

                registro = 1

                database.resultado_final_esteira(1)
                

            elif label == 'INCORRECT':

                resultado = 'INCORRETO'

                color = (0, 0, 255)

                registro = 1

                database.resultado_final_esteira(2)

            
            if registro == 1:

                atual = database.get_tempo_atual(6)
                final = time()

                total = final - atual

                if total > 10:
                    
                    #upo para o banco
                    dataSave = Thread(target = save_image, args = (img, resultado, "fim_esteira_gap.pt"))
                    dataSave.start()
                


            annotator.box_label(b, label, color)
            annotator.box_label(b, label, color)

            img = annotator.result()

    return av.VideoFrame.from_ndarray(img, format="bgr24")




database = VIS_DAO()

c_1, c_2 =  st.columns(2)

quantity_camera = 1

quantity_camera = c_1.radio(
    "Quantos modelos / câmeras voce deseja utilizar?",
    [1, 2],
    index=0,
)


if quantity_camera == 1:

    modelos_do_banco = database.get_models()

    model_1 = st.selectbox(
    "SELECIONE O MODELO:",
    (modelos_do_banco),
    placeholder="Selecione o seu modelo",
    )

    model_tampa = YOLO(f'models/{model_1}')


    st.header("MONITORAMENTO DO PROCESSO")

    st.write("CLIQUE EM START PARA INICIAR O VIS")


    webrtc_streamer(key="example", video_frame_callback = video_frame_callback_tampa)


    st.divider()

    st.button('Atualizar')


    modelos = database.get_models() 

    modelo = st.selectbox(
    'Selecione um modelo para analise dos dados',
    modelos)

    tab2_col_1, tab2_col_2 = st.columns(2)



    df_hora = database.get_quant_por_hora(modelo)

    fig = px.bar(df_hora, x='hora', y=['correto', 'incorreto'], title='Estatísticas por Hora')

    tab2_col_1.plotly_chart(fig)

    # Plotar com Plotly Express
    df = database.get_reprovacoes_dia(modelo)

    fig = px.pie(df, values=[df['reprovações'].iloc[0], df['aprovações'].iloc[0]],
                names=['Reprovações', 'Aprovações'],
                title='Índice de Reprovação e Aprovação no Dia')

    # Exibir no Streamlit
    tab2_col_2.plotly_chart(fig)




else:


    modelos_do_banco = database.get_models()

    colmodel_1, colmodel_2 = st.columns(2)

    model_1 = colmodel_1.selectbox(
    "SELECIONE O MODELO 1:",
    (modelos_do_banco),
    placeholder="Selecione o seu modelo 1",
    )

    model_2 = colmodel_2.selectbox(
    "SELECIONE O MODELO 2:",
    (modelos_do_banco),
    placeholder="Selecione o seu modelo 2",
    )

    model_tampa = YOLO(f'models/{model_1}')
    model_gap = YOLO(f'models/{model_2}')




    st.header("MONITORAMENTO DO PROCESSO")

    st.write("CLIQUE EM START PARA INICIAR O VIS")



    tab1, tab2 = st.columns(2)

    with tab1:
        
        webrtc_streamer(key="example", video_frame_callback = video_frame_callback_tampa)

    with tab2:
        
        webrtc_streamer(key="sample", video_frame_callback=video_frame_callback_gap)

    st.divider()

    st.button('Atualizar')

    modelos = database.get_models() 

    modelo = st.selectbox(
    'Selecione um modelo para analise dos dados',
    modelos)

    tab2_col_1, tab2_col_2 = st.columns(2)


    df_hora = database.get_quant_por_hora(modelo)

    fig = px.bar(df_hora, x='hora', y=['correto', 'incorreto'], title='Estatísticas por Hora')

    tab2_col_1.plotly_chart(fig)

    df = database.get_reprovacoes_dia(modelo)

    fig = px.pie(df, values=[df['reprovações'].iloc[0], df['aprovações'].iloc[0]],
                names=['Reprovações', 'Aprovações'],
                title='Índice de Reprovação e Aprovação no Dia')

    tab2_col_2.plotly_chart(fig)
