import streamlit as st

st.set_page_config(page_title="Consulta Inteligente", layout="centered")

st.title("Consulta Inteligente de Processos")
st.write("Busca automática focada em ações contra bancos")

nome = st.text_input("Nome do devedor")
banco = st.text_input("Banco (ex: Bradesco, Itaú, Santander)")

if st.button("Buscar processos"):

    if not nome:
        st.warning("Digite o nome")
    else:
        termo = f'"{nome}" "{banco}" processo'
        termo_formatado = termo.replace(" ", "+")

        st.success("Busca otimizada pronta")

        st.markdown("### 🔎 Resultado principal (Google)")
        st.markdown(
            f"👉 [Buscar processos no Google](https://www.google.com/search?q={termo_formatado})"
        )

        st.markdown("---")

        st.markdown("### 🎯 Dica profissional:")
        st.markdown("""
        - Clique nos primeiros resultados  
        - Priorize links com:
            - **Jusbrasil**
            - **Tribunais (TJSP, TJRJ, etc)**
        - Procure termos como:
            - Sustação de leilão  
            - Revisional  
            - Alienação fiduciária  
        """)
