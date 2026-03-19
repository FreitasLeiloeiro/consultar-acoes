import streamlit as st
import pandas as pd
import unicodedata
from datetime import datetime

from tribunais.tjsp import buscar_tjsp

# -------------------------------
# CONFIG
# -------------------------------

st.set_page_config(page_title="Consultar Ações", layout="centered")

st.title("Consultar Ações")
st.write("Busca de processos que possam suspender leilões de imóveis")

# -------------------------------
# INPUTS
# -------------------------------

nome = st.text_input("Nome do Devedor (obrigatório)")
cpf = st.text_input("CPF ou CNPJ (opcional)")
matricula = st.text_input("Matrícula do imóvel")
data_leilao = st.date_input("Data do leilão")

# -------------------------------
# DATA BR
# -------------------------------

if data_leilao:
    data_formatada = data_leilao.strftime("%d/%m/%Y")
    st.info(f"Data do leilão selecionada: {data_formatada}")

    dias = (data_leilao - datetime.today().date()).days

    if dias <= 0:
        st.error("⚠️ Risco máximo: leilão em 0 dias")
    elif dias <= 10:
        st.warning(f"Atenção: leilão em {dias} dias")
    else:
        st.success(f"Leilão em {dias} dias")

# -------------------------------
# FUNÇÃO SIMPLES
# -------------------------------

def normalizar_nome(nome):
    nome = nome.lower()
    nome = unicodedata.normalize('NFKD', nome)
    nome = "".join([c for c in nome if not unicodedata.combining(c)])
    return nome.strip()

# -------------------------------
# BOTÃO
# -------------------------------

if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite o nome para busca")
    else:

        nome_busca = normalizar_nome(nome)

        st.write("Buscando por:")
        st.write(nome_busca)

        with st.spinner("Consultando TJSP..."):

            resultados = buscar_tjsp(nome_busca)

        # 🔥 GARANTE QUE NÃO TRAVA
        if resultados is None:
            resultados = []

        if resultados:

            df = pd.DataFrame(resultados)

            df = df.drop_duplicates(subset=["Processo"])

            st.subheader("Resultados encontrados")

            st.dataframe(df)

        else:
            st.warning("Nenhum processo encontrado ou consulta bloqueada")
