# Read Fixed length text file
import pandas as pd

def ler_cotacoes_historicas_b3(file_path_read):
    cols = ['tp_registro',
            'dt_pregao',
            'cod_BDI',
            'cod_negociacao',
            'tp_mercado',
            'nm_resumido',
            'ds_especificacao',
            'vl_prazo_termo',
            'ds_moeda_referencia',
            'vl_preco_abertura',
            'vl_preco_maximo',
            'vl_preco_minimo',
            'vl_preco_medio',
            'vl_preco_ultimo',
            'vl_preco_melhor_compra',
            'vl_preco_melhor_venda',
            'nr_negocios',
            'qt_titulos_negociados',
            'vl_titulos_negociados',
            'vl_preco_opcoes',
            'cd_indicador_correcao',
            'dt_vencimento_opcoes',
            'cd_fator_cotacao',
            'cd_sistema_isin',
            'nr_distribuicao',
            ]
    df = pd.read_fwf(file_path_read,
                     header=None,widths=[2,8,2,12,3,12,10,3,4,13,13,13,13,13,13,13,5,18,13,1,8,7,13,12,3],
                     names=cols,
                     skiprows=1)
    return df

file_path_read = 'D:\\Flavio GDrive\\Flavio Cloud\\Investimentos\\Bovespa\\COTAHIST_A2023.TXT'

df = ler_cotacoes_historicas_b3(file_path_read)
print (df)
