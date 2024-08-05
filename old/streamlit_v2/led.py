import streamlit as st
import subprocess
import sys
import os



def main():

    if st.button('Conectar ao CLP'):

        diretorio_atual = os.getcwd()
        script_alvo_path = os.path.join(diretorio_atual, 'teste.py')
        
    # Chama o script_alvo.py em um novo processo
        subprocess.Popen(f'cmd /k python "{script_alvo_path}"', shell=True)
        
        st.text('Conexão bem sucedida!')


if __name__ == "__main__":
    main()
