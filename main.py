import streamlit as st
import pandas as pd
import unicodedata
from datetime import datetime

# 🔗 IMPORT DO TJSP
from tribunais.tjsp import buscar_tjsp

# -------------------------------
# CONFIGURAÇÃO
# -------------------------------

st.set_page_config(page_title="Consultar Ações", layout="centered")

st.title("Consultar Ações")
st.write("Busca de processos que possam suspender leilões de imóveis")

# -------------------------------
# INPUTS
# -------------------------------

nome = st.text_input("Nome do Devedor (ou avalista / garantidor / fiador / emitente / cônjuge)")
cpf = st.text_input("CPF ou CNPJ somente números")
matricula = st.text_input("Matrícula do imóvel")
data_leilao = st.date_input("Data do leilão")

# -------------------------------
# DATA BRASIL + ALERTA
# -------------------------------

if data_leilao:
    data_formatada = data_leilao.strftime("%d/%m/%Y")
    st.info(f"Data do leilão selecionada: {data_formatada}")

    dias = (data_leilao - datetime.today().date()).days

    if dias <= 0:
        st.error("⚠ Risco máximo: leilão em 0 dias")
    elif dias <= 10:
        st.warning(f"Atenção: leilão em {dias} dias")

# -------------------------------
# NORMALIZAÇÃO
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

    variacoes = [nome]

    if len(partes) > 1:
        variacoes.append(partes[0] + " " + partes[-1])

    if len(partes) > 2:
        variacoes.append(partes[-1] + " " + partes[0])

    return list(set(variacoes))

# -------------------------------
# CLASSIFICAÇÃO DE RISCO
# -------------------------------

def classificar_risco(texto):

    texto = texto.lower()

    alto = [
        "revisional",
        "anulat",
        "nulidade",
        "sustação",
        "liminar",
        "tutela"
    ]

    medio = [
        "embargos",
        "execução"
    ]

    if any(p in texto for p in alto):
        return "🔴 ALTO"

    elif any(p in texto for p in medio):
        return "🟠 MÉDIO"

    else:
        return "🟢 BAIXO"

# -------------------------------
# BUSCA
# -------------------------------

if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite um nome para buscar")

    else:
        variacoes = gerar_variacoes(nome)

        st.write("Variações do nome utilizadas na busca:")
        st.write(variacoes)

        resultados = []

        # 🔍 BUSCA EM TODAS VARIAÇÕES
        for v in variacoes:
            try:
                resultados += buscar_tjsp(v)
            except Exception as e:
                st.warning(f"Erro ao consultar TJSP: {e}")

        # -------------------------------
        # RESULTADOS
        # -------------------------------

        if resultados:

            df = pd.DataFrame(resultados)

            # 🔧 GARANTIR COLUNAS
            if "Autor" not in df.columns:
                df["Autor"] = ""

            if "Réu" not in df.columns:
                df["Réu"] = ""

            # 🚀 REMOVER DUPLICADOS
            df = df.drop_duplicates(subset=["Processo", "Tribunal"])

            # 🎯 CLASSIFICAR RISCO
            df["Risco"] = df["Classe"].apply(classificar_risco)

            # 🔗 LINK CLICÁVEL
            if "Link" in df.columns:
                df["Processo"] = df.apply(
                    lambda x: f'<a href="{x["Link"]}" target="_blank">{x["Processo"]}</a>',
                    axis=1
                )
                df = df.drop(columns=["Link"])

            # 📊 ORDEM DAS COLUNAS
            colunas = ["Tribunal", "Processo", "Autor", "Réu", "Classe", "Data", "Risco"]
            df = df[[c for c in colunas if c in df.columns]]

            st.subheader("Resultados encontrados")

            st.write(
                df.to_html(escape=False, index=False),
                unsafe_allow_html=True
            )

        else:
            st.warning("Nenhum processo encontrado")
