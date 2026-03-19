import streamlit as st

st.set_page_config(page_title="Consultar Ações", layout="centered")

st.title("Consultar Ações")
st.write("Busca de processos que possam impactar leilões de imóveis")

# INPUTS
nome = st.text_input("Nome da parte (obrigatório)")
cpf = st.text_input("CPF ou CNPJ (opcional)")

# BOTÃO
if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite o nome para realizar a busca")
    else:
        nome_formatado = nome.replace(" ", "+")

        # Se tiver CPF, inclui na URL
        if cpf:
            url = f"https://esaj.tjsp.jus.br/cpopg/search.do?cbPesquisa=NMPARTE&dadosConsulta.valorConsulta={nome_formatado}&dadosConsulta.valorConsultaCpfCnpj={cpf}"
        else:
            url = f"https://esaj.tjsp.jus.br/cpopg/search.do?cbPesquisa=NMPARTE&dadosConsulta.valorConsulta={nome_formatado}"

        st.success("Consulta pronta")

        st.markdown(f"""
        🔎 **Clique abaixo para consultar no TJSP:**

        👉 [Abrir processos no TJSP]({url})
        """)
