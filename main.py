import streamlit as st

st.set_page_config(page_title="Monitor de Oportunidades Jurídicas", layout="centered")

st.title("Monitor de Oportunidades Jurídicas")
st.write("Busca em Diários de Justiça (DJE) para identificar ações relevantes")

nome = st.text_input("Nome da parte")
banco = st.text_input("Banco (ex: Bradesco)")

if st.button("Buscar no DJE"):

    termo = f"{nome} {banco}".strip().replace(" ", "+")

    st.success("Buscar nos Diários de Justiça:")

    # TJSP DJE
    st.markdown("### 📘 TJSP - Diário da Justiça")
    st.markdown(
        f"👉 https://www.dje.tjsp.jus.br/cdje/index.do?buscaLivre={termo}"
    )

    # TJRJ DJE
    st.markdown("### 📘 TJRJ - Diário da Justiça")
    st.markdown(
        f"👉 https://www4.tjrj.jus.br/ejud/ConsultaDiario.aspx?busca={termo}"
    )

    # TJMG DJE
    st.markdown("### 📘 TJMG - Diário da Justiça")
    st.markdown(
        f"👉 https://www.tjmg.jus.br/portal-tjmg/servicos/diario-do-judiciario/?q={termo}"
    )

    st.markdown("---")

    st.markdown("### 🎯 O que procurar:")
    st.markdown("""
    - Ação Anulatória de Consolidação de Propriedade 🔴
    - Ação de Anulação de Leilão Extrajudicial 🔴
    - Ação Declaratória de Nulidade de Ato Jurídico 🔴
    - Ausência de Intimação Pessoal 🔴
    - Vício na Consolidação da Propriedade 🔴
    - Preço Vil 🔴
    - Teoria do Adimplemento Substancial 🔴
    - Irregularidade no Edital 🔴
    - Tutela de Urgência Antecipada 🔴
    - Perigo da Demora 🔴
    - Probabilidade do Direito 🔴
    - Direito de Preferência 🔴
    - Purgação da Mora (ou Purga da Mora) 🔴
    - Consignação em Pagamento 🔴
    - Vício de Edital (Ausência de Publicidade) 🔴
    - Agravo de Instrumento com Pedido de Efeito Suspensivo 🔴
    - Averbação Premonitória (Art. 828 do CPC) 🔴
    - Teoria do Desvio Produtivo do Consumidor
    - Sustação de leilão 🔴  
    - Revisional 🔴  
    - Alienação fiduciária 🔴  
    - Busca e apreensão 🟡  
    """)
