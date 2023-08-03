import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

sns.set_style("whitegrid")

def plotar(value, index, func, ylabel='', xlabel='', opcao='nada'):
    if opcao == 'nada':
        plot = pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        plot = pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        plot = pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None

URL = './input/SINASC_RO_2019.csv'
df = pd.read_csv(URL)
df.DTNASC = pd.to_datetime(df.DTNASC)
min_data = df['DTNASC'].min()
max_data = df['DTNASC'].max()

st.set_page_config(page_title='SINASC Rondônia 2019',
                   page_icon='./input/logo_rondonia.png'
                   )

with st.sidebar:
    st.title('SINASC Rondônia 2019')
    st.markdown('---')
    data_inicial = st.date_input('Data incial',
                                 value = min_data,
                                 min_value = min_data,
                                 max_value = max_data)
    data_final = st.date_input('Data Final',
                               value = max_data,
                               min_value = min_data,
                               max_value = max_data)
    with st.expander('Como selecionar?'):
        st.write('Selecione uma data inicial e uma data final, após isso os dados do banco de dados aparecerão filtrados.')

st.title('Bem Vindo!!')
st.write('---')

st.write('## Datas Selecionadas:')
st.write(f'Data Inicial: {data_inicial}')
st.write(f'Data Final: {data_final}')
st.write('---')

df = df[(df['DTNASC'] <= pd.to_datetime(data_final)) & (df['DTNASC'] >= pd.to_datetime(data_inicial))]

st.write(df)
st.write('---')

st.write('## Media idade mãe por data')
MIM = plotar('IDADEMAE', 'DTNASC', 'mean', ylabel='media idade mãe')

st.write('---')

st.write('## Quantidade de bebês ao longo do ano')
QTNASC = plotar('IDADEMAE', 'DTNASC', 'count', ylabel='quantidade de nascimentos')

st.write('---')

st.write('## Quantidade de bebês fem e masc por mês')
QTBB = plotar('IDADEMAE', ['DTNASC', 'SEXO'], 'count', opcao='unstack')

st.write('---')

st.markdown('## Média peso dos bebês fem e masc')
MPBB = plotar('PESO', ['DTNASC', 'SEXO'], 'count', opcao='unstack')

st.markdown('---')

st.markdown('## Peso mediano por escolaridade')
PMESCM = plotar('PESO', ['ESCMAE'], 'median', opcao='sort')

st.markdown('---')

st.markdown('## Media apgar1 por gestacao')
MAPGAR1 = plotar('APGAR1', 'GESTACAO', 'mean', ylabel='apgar1 medio', xlabel='gestacao', opcao='sort')
