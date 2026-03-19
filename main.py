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
        st.warning("Digite o nome para busca")
    else:

        variacoes = gerar_variacoes(nome)

        st.write("Variações do nome utilizadas na busca:")
        st.write(variacoes)

        resultados = []

        # 🔥 LOOP ORIGINAL QUE FUNCIONAVA
        for v in variacoes:
            dados = buscar_tjsp(v)
            resultados.extend(dados)

        if resultados:

            df = pd.DataFrame(resultados)

            # remover duplicados
            df = df.drop_duplicates(subset=["Processo"])

            st.subheader("Resultados encontrados")

            st.dataframe(df)

        else:
            st.warning("Nenhum processo encontrado")
