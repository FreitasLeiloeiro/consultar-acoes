import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Consultar Ações", layout="centered")

st.title("Consultar Ações")
st.write("Busca de processos que possam suspender leilões de imóveis")

# INPUTS
nome = st.text_input("Nome do Devedor (obrigatório)")
cpf = st.text_input("CPF ou CNPJ (opcional)")
matricula = st.text_input("Matrícula do imóvel")
data_leilao = st.date_input("Data do leilão")

# DATA
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

# BOTÃO
if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite o nome")
    else:

        nome_formatado = nome.replace(" ", "+")

        url = f"https://esaj.tjsp.jus.br/cpopg/search.do?cbPesquisa=NMPARTE&dadosConsulta.valorConsulta={nome_formatado}"

        st.success("Consulta pronta")

        st.markdown(f"""
        🔎 **Clique abaixo para ver os processos no TJSP:**

        👉 [Abrir consulta no TJSP]({url})
        """)
