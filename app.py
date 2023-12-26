import streamlit as st
from PIL import Image
from source.class_OPCUA import Opcua

# -- objetos -- 
dados = Opcua("192.168.0.10")

st.set_page_config(layout = "wide", page_title = "VIS Project")

tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Dashboard', 'Realtime', 'Data'])


# ----- SIDE BAR ----- 
with st.sidebar:
    
    st.header('Filters')
    # Views filter
    data_calendar = st.date_input("Qual data deseja analisar?", value = None)

    view = st.radio("Select view:", ["monthly", "weekly", "daily"], index=1, horizontal = True, key = "sidebar")





# --- HEADER ---
    
a1, a2, a3 = st.columns(3)

logo = Image.open('images/ufam.png')
logo = logo.resize((200, 230))

a1.image(logo)

no = a2.text_input('digite aqui')

if len(no) < 2:

    resposta_opcua = 'vazio'

else:

    resposta_opcua = dados.get_value(no)

if no is None:

    a2.metric("Resposta: ", 'no')

else:

    a2.metric("Resposta: ", resposta_opcua)

a3.metric("Ulitma Atualização", 'TESTE')


b1, b2, b3 = st.columns(3)

with b1:

    teste = b1.radio("Selecione uma ação:", ["True", "False"], index=1, horizontal = True)

    no2 = st.text_input('qual nó deseja alterar')

    if st.button('Confirmar'):

        if teste == 'True':

            dados.set_value(no2, True)

        elif teste == 'False':

            dados.set_value(no2, False)

    picture = b2.camera_input('TIRANDO FOTO')

    if picture:
        b2.image(picture)






b2.metric("Ulitma Atualização", 'TESTE')
b3.metric("Ulitma Atualização", 'TESTE')


with tab1:

    st.title('Vision Inspect System - Ind 4.0')



    c1, c2 = st.columns((7,3))

    
    









