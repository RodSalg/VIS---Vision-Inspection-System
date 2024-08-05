

import streamlit as st
from datetime import datetime, date
from source.DAO import VIS_DAO
from PIL import Image

st.set_page_config( layout = 'wide', page_title = "VIS Project")

database = VIS_DAO()


indice_imagem_atual = database.get_control_element(1)
# print('indice da imagem atual: ', indice_imagem_atual)

on = st.toggle('VER SOMENTE IMAGENS NÃO AVALIADAS')

modelos = database.get_models()
modelos.append('todos')



modelo = st.selectbox(
'Selecione um modelo',
modelos,index=(len(modelos) - 1))

# if modelo is None:

#     modelo == 'todos'

if on:
    
    st.button('Atualizar')
    database.update_indice_image(0)
    lista_imagens = database.get_not_evaluated(1, modelo) #1 imagens nao avaliadas #0 todas as imagens

else:

    database.update_indice_image(0)
    
    lista_imagens = database.get_not_evaluated(0, modelo)
    
    print('MINHA LISTA DE IMAGENS \n\n', lista_imagens)

st.text(indice_imagem_atual)

column_1, column_2 = st.columns(2)

st.divider()

if len(lista_imagens) == 0:

    st.text('Não há imagens para serem avaliadas')

else:

    filename = lista_imagens[indice_imagem_atual]


    with column_1:
        
        original_image = Image.open(f'results/{filename}')

        col_A, col_B, col_C = st.columns(3)

        resized_image = original_image.resize((800, 500))


        resultado_IA, status_image, ind = database.get_status_image(filename)
        
        col_A.metric('Imagem atual:', f'{filename}')
        col_B.metric('INSPEÇÃO HUMANA:', F'{status_image}')
        col_C.metric('RESULTADO DA IA:', f'{resultado_IA}')

        st.image(resized_image)

    with column_2:

        

        column_A, column_B = st.columns(2)
        st.text(f'Imagem atual: {filename}')
        
        
        option = st.selectbox(
        "QUAL O RESULTADO",
        ("1 - DETECTOU CORRETAMENTE", "2 - DETECTOU ERRADO", "3 - DETECTADO MAS NAO EXISTE ", "4 -NAO DETECTADO E  NÃO EXISTE "),
        index=ind,
        placeholder="SELECIONE SUA OPÇÃO DE CLASSIFICAÇÃO...",
        )
        st.text(ind)

        st.write('SUA OPÇÃO:', option)



        area_b1, area_b2, area_b3, area_b4 = st.columns(4)

        if area_b1.button('CLASSIFICAR'):

            option_chosed = int(option[0])
            database.update_avaliacao_humana(filename, option_chosed)
    
        if area_b2.button('PRÓXIMA IMAGEM'):

            indice_imagem_atual = indice_imagem_atual + 1
            database.update_indice_image(indice_imagem_atual)

            if indice_imagem_atual == (len(lista_imagens)):
                # print('entrei na condição')
                database.update_indice_image(0)

        if area_b3.button('VOLTAR IMAGEM'):

            indice_imagem_atual = indice_imagem_atual - 1
            database.update_indice_image(indice_imagem_atual)

            if indice_imagem_atual <= (0):
                # print('entrei na condição')

                database.update_indice_image((len(lista_imagens)) - 1)

        area_b4.button('ATUALIZAR')
            
        if on:

            df = database.get_all_not_availables(1, modelo)

        else:

            df = database.get_all_not_availables(0, modelo)


        st.table(df)


