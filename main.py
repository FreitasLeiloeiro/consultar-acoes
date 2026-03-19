import streamlit as st
import pandas as pd
import unicodedata
from datetime import datetime
import time

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

nome = st.text_input("Nome (obrigatório para busca)")
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
# BANCOS
# -------------------------------

bancos = [
    "bradesco","itau","santander","caixa","banco do brasil",
    "bb","inter","nubank","pan","votorantim"
]

# -------------------------------
# FUNÇÕES
# -------------------------------

def normalizar_nome(nome):
    nome = nome.lower()
    nome = unicodedata.normalize('NFKD', nome)
    nome = "".join([c for c in nome if not unicodedata.combining(c)])
    return nome.strip()

def nome_simples(nome):
    partes = nome.split()
    if len(partes) >= 2:
        return partes[0] + " " + partes[-1]
    return nome

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
# BOTÃO
# -------------------------------

if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite o nome (obrigatório)")
    else:

        nome_normalizado = normalizar_nome(nome)
        nome_reduzido = nome_simples(nome_normalizado)

        st.write("Tentativa 1 (nome completo):")
        st.write(nome_normalizado)

        resultados = buscar_tjsp(nome_normalizado)

        # 🔥 FALLBACK AUTOMÁTICO
        if not resultados:
            st.write("Tentativa 2 (nome simplificado):")
            st.write(nome_reduzido)

            time.sleep(2)
            resultados = buscar_tjsp(nome_reduzido)

        # -------------------------------

        if resultados:

            df = pd.DataFrame(resultados)

            df = df.drop_duplicates(subset=["Processo"])

            df["Banco"] = df.apply(
                lambda row: identificar_banco(
                    str(row.get("Autor", "")) + " " + str(row.get("Réu", ""))
                ),
                axis=1
            )

            df["Risco"] = df.apply(classificar_risco, axis=1)

            st.subheader("Resultados encontrados")

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
