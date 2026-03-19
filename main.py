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

nome = st.text_input("Nome do Devedor (ou avalista / garantidor / fiador / emitente / cônjuge)")
cpf = st.text_input("Números do CPF ou CNPJ")
matricula = st.text_input("Matrícula do local")
data_leilao = st.date_input("Dados do")

# -------------------------------
# FUNÇÕES
# -------------------------------

def normalizar_nome(nome):

    nome = nome.lower()
    nome = unicodedata.normalize('NFKD', nome)
    nome = "".join([c for c in nome if not unicodedata.combining(c)])

    remover = [" de ", " da ", " dos ", " das "]
    for r in remover:
        nome = nome.replace(r, " ")

    return nome.strip()


def gerar_variacoes(nome):

    nome = normalizar_nome(nome)

    partes = nome.split()

    variacoes = []

    variacoes.append(nome)

    if len(partes) > 1:
        variacoes.append(partes[0] + " " + partes[-1])

    if len(partes) > 2:
        variacoes.append(partes[-1] + " " + partes[0])

    return list(set(variacoes))

# -------------------------------
# BOTÃO
# -------------------------------

if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite um nome para buscar")
    else:

        variacoes = gerar_variacoes(nome)

        st.write("Variações do nome utilizado na busca:")
        st.write(variacoes)

        resultados = []

        # 🔥 ESSA É A LÓGICA ORIGINAL QUE FUNCIONAVA
        for v in variacoes:
            processos = buscar_tjsp(v)
            resultados.extend(processos)

        if resultados:

            df = pd.DataFrame(resultados)

            df = df.drop_duplicates(subset=["Processo"])

            st.subheader("Resultados encontrados")

            st.dataframe(df)

        else:
            st.warning("Nenhum processo encontrado")
