from datetime import datetime, date
from source.DAO import VIS_DAO
import plotly.express as px
import streamlit as st


st.set_page_config( layout = 'wide', page_title = "VIS Project")


database = VIS_DAO()

modelos = database.get_models()

modelo = st.selectbox(
'Selecione um modelo',
modelos)

# logo = Image.open('resources/FIT-Logo-3-cores.png')
# logo = logo.resize((230, 230))#and make it to whatever size you want.


#Time
nowTime = datetime.now()
current_time = nowTime.strftime("%H:%M:%S")

today = str(date.today())

# st.write(today)
timeMetric, = st.columns(1)
# timeMetric.metric("data: ", today)

# Row A
a1, a2 = st.columns(2)

# a1.image(logo)


data = '12/01'


precision, recall, accuracy = database.calculate_metrics(modelo)

a1.metric("PRECISÃO", '{:.2f}%'.format(precision * 100))
a2.metric("RECALL: ", '{:.2f}%'.format(recall * 100 ))
# a3.metric("testando", contador)


# Row B

with st.expander('Mais informações'):

    b1, b2, b3, b4 = st.columns(4)

    b1.metric("Humidity", f"{12}"+"%")
    b2.metric("Feels like", f"{14}")
    b3.metric("Highest temperature", f"{35}")
    b4.metric("Lowest temperature", f"{39}")

# Row C
#C1 being the graph, C2 The Table.
c1, c2 = st.columns((4,3))


with c1:

    st.title('Quantidade de inferências hoje')

    df_hora = database.get_quant_por_hora(modelo)

    fig = px.bar(df_hora, x='hora', y=['correto', 'incorreto'], title='Estatísticas por Hora')
    
    c1.plotly_chart(fig)

with c2:

    
    df = database.get_reprovacoes_dia(modelo)

    fig = px.pie(df, values=[df['reprovações'].iloc[0], df['aprovações'].iloc[0]],
                names=['Reprovações', 'Aprovações'],
                title='Índice de Reprovação e Aprovação no Dia')

    # Exibir no Streamlit
    c2.plotly_chart(fig)


newb1, newb2 = st.columns(2)

st.title('últimos Registros')

df = database.get_all_not_availables(0, modelo)

st.table(df)    

st.button("Run me manually")

