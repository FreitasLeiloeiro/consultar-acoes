import streamlit as st

st.set_page_config(page_title="Consulta Inteligente de Processos", layout="centered")

st.title("Consulta Inteligente de Processos")
st.write("Busca otimizada por nome + banco para identificar ações relevantes")

nome = st.text_input("Nome do devedor")
banco = st.text_input("Banco (ex: Bradesco, Itaú, Santander)")

if st.button("Buscar processos"):

    if not nome:
        st.warning("Digite o nome")
    else:
        termo = f'"{nome}" "{banco}" processo'
        termo_formatado = termo.replace(" ", "+")

        st.success("Busca pronta")

        # 🔎 GOOGLE
        st.markdown("### 🔎 Buscar processos (Google)")
        st.markdown(
            f"👉 [Abrir busca no Google](https://www.google.com/search?q={termo_formatado})"
        )

        st.markdown("---")

        # ⚖️ TRIBUNAIS
        nome_formatado = nome.replace(" ", "+")

        st.markdown("### ⚖️ Consulta direta nos tribunais:")

        st.markdown(f"👉 [TJSP](https://esaj.tjsp.jus.br/cpopg/search.do?dadosConsulta.valorConsulta={nome_formatado})")
        st.markdown(f"👉 [TJRJ](https://www4.tjrj.jus.br/consultaProcessoWebV2/consulta.do?nomeParte={nome_formatado})")
        st.markdown(f"👉 [TJMG](https://www4.tjmg.jus.br/juridico/sf/proc_resultado2.jsp?nomeParte={nome_formatado})")

        st.markdown("---")

        st.markdown("### 🎯 Dica prática:")
        st.markdown("""
        - Use o Google como principal fonte  
        - Procure:
            - Sustação de leilão  
            - Revisional  
            - Alienação fiduciária  
        - Clique no número do processo  
        - Valide no tribunal  
        """)
