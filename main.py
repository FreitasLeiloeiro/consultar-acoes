import streamlit as st

st.set_page_config(page_title="Consulta Inteligente de Processos", layout="centered")

st.title("Consulta Inteligente de Processos")
st.write("Busca estruturada de processos com identificação de banco")

nome = st.text_input("Nome do devedor (obrigatório)")
banco = st.text_input("Banco (opcional - ex: Bradesco)")

if st.button("Buscar processos"):

    if not nome:
        st.warning("Digite o nome")
    else:
        termo = f"{nome} {banco}".strip()
        termo_formatado = termo.replace(" ", "%20")

        st.success("Busca estruturada pronta")

        # 🔥 JUSDADOS (principal)
        st.markdown("### 🧠 JusDados (recomendado)")
        st.markdown(
            f"👉 [Buscar no JusDados](https://jusdados.com/busca?q={termo_formatado})"
        )

        # 🔎 Google (backup forte)
        st.markdown("### 🔎 Google (backup)")
        st.markdown(
            f"👉 [Buscar no Google](https://www.google.com/search?q={termo_formatado}+processo)"
        )

        st.markdown("---")

        st.markdown("### 🎯 O que procurar:")
        st.markdown("""
        - Nome do banco (Bradesco, Itaú, etc)
        - Tipo da ação:
            - Sustação de leilão 🔴
            - Revisional 🔴
            - Alienação fiduciária 🔴
        - Número do processo (clicável)
        """)
