import streamlit as st
from PIL import Image
from PIL import Image
from threading import Thread
from time import time
from keras.preprocessing.image import img_to_array
from streamlit_webrtc import webrtc_streamer
import streamlit as st
import numpy as np
import os
from source.DAO import VIS_DAO

database = VIS_DAO()

st.set_page_config( layout = 'wide', page_title = "VIS Project")

def main():

    a1, a2 = st.columns([100, 200])

    logo = Image.open('images/ufam.png')
    logo = logo.resize((120, 150))

    a1.image(logo)

    a2.title("VIS - VISION INSPECTION SYSTEM")


    st.subheader('SEJA BEM VINDO')

    planta = Image.open('images/capa.png')
    planta = planta.resize((600, 400))

    c1, c2= st.columns([500, 500])


    c1.image(planta)

    with c2:

        st.subheader('Cadastro de novo modelo')

        uploaded_file = st.file_uploader("Arraste o modelo ou selecione no ícone abaixo", type=["pt"])

        if uploaded_file is not None:

            nome_modelo = uploaded_file.name

            filename_model = (nome_modelo.split(r'\\'))[-1]

            modelos = os.listdir('models')

            if filename_model in modelos:

                st.error('Ja existe um modelo com este nome cadastrado no sistema.')
            
            else:

                model_path = os.path.join("models", uploaded_file.name)
                
                progress_bar = st.progress(0) 
                
                with open(model_path, "wb") as f:

                    content = uploaded_file.getvalue()
                    

                    total_size = len(content)

                    chunk_size = 1024

                    chunks = int(total_size / chunk_size)

                    for i in range(chunks):

                        f.write(content[i * chunk_size: (i + 1) * chunk_size])

                        progress_bar.progress((i + 1) / chunks) 

                database.insert_new_model(filename_model)
                
                st.success(f"Modelo de IA carregado e cadastrado com sucesso!")
                st.success(f"Modelo copiado para: {filename_model}")

        
        
        
        st.subheader('Deletar um modelo')

        modelos_cadastrados = database.get_models()

        model_selected = st.selectbox(
            'que modelo deseja excluir?',
            (modelos_cadastrados))
        
        col1_, col2_ = st.columns(2)
        
        if col1_.button('Excluir modelo'):

            try:

                database.delet_model(model_selected)
            
            except ValueError as e:

                st.error('Modelo nao encontrado no banco')

            model_path = os.path.join("models", model_selected)

            if os.path.exists(model_path):

                os.remove(model_path)
                st.success("Modelo excluído com sucesso!")

            else:
                st.error("O modelo não foi encontrado na pasta 'models'.")

        col2_.button('Atualizar pagina')





if __name__ == "__main__":

    main()
