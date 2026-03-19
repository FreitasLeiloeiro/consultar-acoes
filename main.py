import streamlit as st

st.set_page_config(page_title="Consulta Inteligente de Processos", layout="centered")

st.title("Consulta Inteligente de Processos")
st.write("Busca automatizada por devedor + banco")

nome = st.text_input("Nome do devedor")
banco = st.text_input("Banco (ex: Bradesco, Itaú, Santander)")

if st.button("Buscar processos"):

    if not nome:
        st.warning("Digite o nome")
    else:
        termo = f"{nome} {banco}".strip()
        termo_formatado = termo.replace(" ", "+")

        st.success("Buscas prontas:")

        st.markdown("### 🔎 Google (mais completo)")
        st.markdown(f"👉 [Buscar no Google](https://www.google.com/search?q={termo_formatado}+processo)")

        st.markdown("### ⚖️ Jusbrasil")
        st.markdown(f"👉 [Buscar no Jusbrasil](https://www.jusbrasil.com.br/busca?q={termo_formatado})")

        st.markdown("### 🧾 Escavador")
        st.markdown(f"👉 [Buscar no Escavador](https://www.escavador.com/busca?termo={termo_formatado})")
