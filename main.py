import streamlit as st
import pandas as pd
import unicodedata
from datetime import datetime

# 🔗 IMPORTAÇÃO DO TJSP
from tribunais.tjsp import buscar_tjsp

# -------------------------------
# CONFIG INICIAL
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
# DATA NO PADRÃO BR
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
# LISTA DE BANCOS
# -------------------------------

bancos = [
    "bradesco",
    "itau",
    "santander",
    "caixa economica",
    "caixa econômica",
    "banco do brasil",
    "bb",
    "hsbc",
    "inter",
    "nubank",
    "pan",
    "votorantim",
    "original",
    "daycoval",
    "mercantil",
]

# -------------------------------
# FUNÇÕES AUXILIARES
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


def identificar_banco(texto):
    if not texto:
        return ""

    texto = texto.lower()

    for banco in bancos:
        if banco in texto:
            return banco.upper()

    return ""


def classificar_risco(row):
    if row["Banco"]:
        return "🔴 ALTO"
    return "🟢 BAIXO"

# -------------------------------
# BOTÃO DE BUSCA
# -------------------------------

if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite um nome para busca")
    else:

        variacoes = gerar_variacoes(nome)

        st.write("Variações do nome utilizadas na busca:")
        st.write(variacoes)

        resultados = []

        # 🔎 CONSULTA TJSP
        for v in variacoes:
            dados_tjsp = buscar_tjsp(v)
            resultados.extend(dados_tjsp)

        if resultados:

            df = pd.DataFrame(resultados)

            # 🔥 REMOVER DUPLICADOS
            df = df.drop_duplicates(subset=["Processo"])

            # 🏦 DETECTAR BANCO
            df["Banco"] = df.apply(
                lambda row: identificar_banco(
                    str(row.get("Autor", "")) + " " + str(row.get("Réu", ""))
                ),
                axis=1
            )

            # ⚠️ CLASSIFICAR RISCO
            df["Risco"] = df.apply(classificar_risco, axis=1)

            st.subheader("Resultados encontrados")

            # 🔗 EXIBIÇÃO COM LINK
            for _, row in df.iterrows():

                st.markdown(f"""
                **Tribunal:** {row['Tribunal']}  
                **Processo:** [{row['Processo']}]({row['Link']})  
                **Classe:** {row['Classe']}  
                **Banco:** {row['Banco'] if row['Banco'] else 'Não identificado'}  
                **Risco:** {row['Risco']}  
                ---
                """)

        else:
            st.warning("Nenhum processo encontrado")
