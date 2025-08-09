import pandas as pd
import sqlite3
from datetime import datetime

# Definir o caminho do json
df = pd.read_json('data/data.jsonl', lines=True)

# Setar pandas para exibir todas as colunas
pd.options.display.max_columns = None

# Adicionar a coluna_source com valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/informatica/portateis-acessorios/notebooks/notebook"

# Adicionar a coluna _coleta com a data e hora atual
df['_datetime'] = datetime.now()

# Tratar nulos
df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_rating'] = df['reviews_rating'].fillna('0')
df['reviews_total'] = df['reviews_total'].fillna('(0)')

# Garantir que estao como string antes de usar .str
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['reviews_total'] = df['reviews_total'].astype(
    str).str.replace('[\(\)]', '', regex=True)


# Converter para numeros
df['old_money'] = df['old_money'].astype(float)
df['new_money'] = df['new_money'].astype(float)
df['reviews_rating'] = df['reviews_rating'].astype(float)
df['reviews_total'] = df['reviews_total'].astype(int)

# manter apenas produtos com preço entre 1000 e 10000 reais
df = df[
    ((df['old_money'] >= 1000) & (df['old_money'] <= 10000)) |
    ((df['new_money'] >= 1000) & (df['new_money'] <= 10000))
]

print(df)


# Remover as colunas antigas de preços

# Conectar ao banco de dados SQLite ou criar um novo
conn = sqlite3.connect('data/mercadolivre.db')

# Salvar o DataFrame no banco de dados
df.to_sql('notebook', conn, if_exists='replace', index=False)

conn.close()
