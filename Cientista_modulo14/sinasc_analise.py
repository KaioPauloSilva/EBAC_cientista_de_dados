from typing import Any

import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import sys

SCRIPT_NAME = sys.argv[0]
print(f'O nome do script é :', SCRIPT_NAME)
MESES = sys.argv[1:]
for mes in MESES:
    URL = './input/SINASC_RO_2019_' + mes + '.csv'
    df = pd.read_csv(URL)

    max_data = df.DTNASC.max()[:7]
    print(max_data)


    def plotar(value, index, func, ylabel='', xlabel='', opcao='nada'):
        if opcao == 'nada':
            pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
        elif opcao == 'unstack':
            pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
        elif opcao == 'sort':
            pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        return None


    os.makedirs('./output/figs/' + max_data, exist_ok=True)

    plotar('IDADEMAE', 'DTNASC', 'mean', ylabel='media idade mãe')
    plt.savefig('./output/figs/' + max_data + '/media idade mãe por data.png')

    plotar('IDADEMAE', 'DTNASC', 'count', ylabel='quantidade de nascimentos')
    plt.savefig('./output/figs/' + max_data + '/quantidade de bebês ao longo do ano.png')

    plotar('IDADEMAE', ['DTNASC', 'SEXO'], 'count', opcao='unstack')
    plt.savefig('./output/figs/' + max_data + '/quantidade de bebês fem e masc por mês')

    plotar('PESO', ['DTNASC', 'SEXO'], 'count', opcao='unstack')
    plt.savefig('./output/figs/' + max_data + '/média peso dos bebês fem e masc.png')

    plotar('PESO', ['ESCMAE'], 'median', opcao='sort')
    plt.savefig('./output/figs/' + max_data + '/peso mediano por escolaridade mae.png')

    plotar('APGAR1', 'GESTACAO', 'mean', ylabel='apgar1 medio', xlabel='gestacao', opcao='sort')
    plt.savefig('./output/figs/' + max_data + '/media apgar1 por gestacao.png')
