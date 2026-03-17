import streamlit as st
import pandas as pd
import unicodedata
from datetime import date

from tribunais.tjsp import buscar_tjsp

# =============================
# TÍTULO
# =============================
st.title("Consultar Ações")
st.write("Busca de processos que possam suspender leilões de imóveis")

# =============================
# CAMPOS
# =============================
nome = st.text_input("Nome do Devedor (ou avalista / garantidor / fiador / emitente / cônjuge)")
cpf = st.text_input("CPF ou CNPJ somente números")
matricula = st.text_input("Matrícula do imóvel")

data_leilao = st.date_input("Data do leilão")

# =============================
# DATA BRASIL + ALERTA
# =============================
if data_leilao:
    data_br = data_leilao.strftime("%d/%m/%Y")
    st.info(f"Data do leilão selecionada: {data_br}")

    dias = (data_leilao - date.today()).days

    if dias > 60:
        st.success(f"Leilão em {dias} dias")
    elif dias > 30:
        st.info(f"Leilão em {dias} dias")
    elif dias > 7:
        st.warning(f"Atenção: leilão em {dias} dias")
    else:
        st.error(f"⚠ Risco máximo: leilão em {dias} dias")

# =============================
# FUNÇÕES
# =============================
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

    if nome:
        variacoes.append(nome)

    if len(partes) > 1:
        variacoes.append(partes[0] + " " + partes[-1])

    if len(partes) > 2:
        variacoes.append(partes[-1] + " " + partes[0])

    return list(set(variacoes))

def buscar_processos(nome):
    resultados = []
    resultados += buscar_tjsp(nome)
    return resultados

# =============================
# BOTÃO
# =============================
if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite um nome para buscar")
    else:
        variacoes = gerar_variacoes(nome)

        st.write("Variações do nome utilizadas na busca:")
        st.write(variacoes)

        dados = buscar_processos(nome)

        if dados:
            df = pd.DataFrame(dados)

            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime("%d/%m/%Y")

            st.subheader("Resultados encontrados")
            st.dataframe(df)

        else:
            st.warning("Nenhum processo encontrado")