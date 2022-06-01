from codigo_ejecucion import *
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

#CONFIGURACION DE LA PÁGINA
st.set_page_config(
     page_title = 'MEIDAT',
     page_icon = 'meidat.png',
     layout = 'wide')
#MAIN
st.title('MEIDAT - MANTENIMIENTO PREVENTIVO')

#SIDEBAR
with st.sidebar:
    st.image('meidat.jpg')


#INPUTS DE LA APLICACIÓN

    campaña = st.selectbox('Tipo de campaña', ['Esparrago','Judia'])
    vel_prod = st.slider("Velocidad (Tarros/hora)", 1, 10000)
    turnos = st.radio( "Turnos de producción",('1', '2', '3'))
    volumen = st.number_input("Volumen de producción (kg x dia)", 1, 100000)

#Valores fijos
    horas_arreglo = 8
    euros_hora = 15
    personal_mant = 2
    personal_prod = 2
    valor_esparrago = 4
    valor_judia = 2
    valor_tarro = 0.1
    turnos = int(turnos)
    tarro_judia = 0.5
    tarro_esparrago = 0.7
    coste_rep = 500


#CALCULOS Y CARGA DE DATOS



if (vel_prod <= 5000):
    df = pd.read_csv("Averia_1.csv",index_col= 'Date', sep = ',')
elif (vel_prod > 6000) & (vel_prod <= 7500) & ((turnos == 1) or (turnos == 2)):
    df = pd.read_csv("Averia_38.csv",index_col= 'Date', sep = ',')
elif (vel_prod > 5000) & (vel_prod <= 6000) & ((turnos == 1) or (turnos == 2)):
    df = pd.read_csv("Averia_11.csv",index_col= 'Date', sep = ',')
elif (vel_prod <= 7500) & (turnos == 3):
    df = pd.read_csv("Averia_46.csv",index_col= 'Date', sep = ',')
else:
    df = pd.read_csv("Averia_95.csv",index_col= 'Date', sep = ',')

impacto_judia = int(coste_rep + horas_arreglo * (personal_prod *euros_hora + personal_mant*euros_hora) + volumen * valor_judia + (volumen/tarro_judia*valor_tarro))
impacto_esparrago = int(coste_rep + horas_arreglo * (personal_prod *euros_hora + personal_mant*euros_hora) + volumen * valor_esparrago + (volumen/tarro_esparrago*valor_tarro))


#EJECUCIÓN DEL PIPE
if st.sidebar.button('CLICK PARA CALCULAR'):
    scoring = ejecutar_modelo(df)
    scoring = int(scoring)
    
    if campaña == 'Esparrago':
        perdida = int(impacto_esparrago * scoring/100)
        impacto = impacto_esparrago
    else:
        perdida = int(impacto_judia * scoring/100)
        impacto = impacto_judia

    pd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "PD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": scoring, "name": "%"}],
                }
            ],
        }
    
    
    st.write('La probabilidad de fallo por avería es de:')
    st_echarts(options=pd_options,width = "85%")
        
#kpis
    col1,col2 = st.columns(2)
    with col1:
        st.write('El valor económico del proceso es (Euros):')
        st.metric(label="Valor económico €", value=impacto, delta="- Impacto",delta_color="normal")
    with col2:
        st.write('La pérdida esperada es de (Euros):')
        st.metric(label="Pérdida esperada €", value=perdida, delta="- Pérdida",delta_color="normal")
else:
    st.write('DEFINE LOS PARÁMETROS DE PRODUCCIÓN Y HAZ CLICK EN CALCULAR')