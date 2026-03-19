import streamlit as st

st.title("Consulta Inteligente de Processos")

nome = st.text_input("Nome da parte")

if st.button("Buscar"):

    if nome:
        nome_formatado = nome.replace(" ", "+")

        st.markdown("### 🔎 Buscar em plataformas:")

        st.markdown(f"👉 [Escavador](https://www.escavador.com/busca?termo={nome_formatado})")
        st.markdown(f"👉 [Jusbrasil](https://www.jusbrasil.com.br/busca?q={nome_formatado})")

        st.markdown("---")
        st.markdown("### ⚖️ Tribunais:")

        st.markdown(f"👉 [TJSP](https://esaj.tjsp.jus.br/cpopg/search.do?dadosConsulta.valorConsulta={nome_formatado})")
        st.markdown(f"👉 [TJRJ](https://www4.tjrj.jus.br/consultaProcessoWebV2/consulta.do?nomeParte={nome_formatado})")
