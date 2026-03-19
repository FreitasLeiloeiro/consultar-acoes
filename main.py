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
# BOTÃO
# -------------------------------

if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite o nome para busca")
    else:

        # 🔥 BUSCA SIMPLES (FUNCIONA)
        resultados = buscar_tjsp(nome)

        if resultados:

            df = pd.DataFrame(resultados)

            # remover duplicados
            df = df.drop_duplicates(subset=["Processo"])

            st.subheader("Resultados encontrados")

            # 🔗 EXIBIÇÃO SIMPLES E FUNCIONAL
            for _, row in df.iterrows():

                st.markdown(f"""
                **Tribunal:** {row.get('Tribunal', '')}  
                **Processo:** [{row.get('Processo', '')}]({row.get('Link', '')})  
                **Classe:** {row.get('Classe', '')}  
                **Data:** {row.get('Data', '')}  
                ---
                """)

        else:
            st.warning("Nenhum processo encontrado")
