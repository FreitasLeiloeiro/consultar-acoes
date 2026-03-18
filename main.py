import streamlit as st
import pandas as pd
import unicodedata
from datetime import datetime

# 🔥 CORREÇÃO DE IMPORT (ESSENCIAL PARA STREAMLIT CLOUD)
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from tribunais.tjsp import buscar_tjsp


st.title("Consultar Ações")

st.write("Busca de processos que possam suspender leilões de imóveis")


# INPUTS
nome = st.text_input("Nome do Devedor (ou avalista / garantidor / fiador / emitente / cônjuge)")
cpf = st.text_input("CPF ou CNPJ somente números")
matricula = st.text_input("Matrícula do imóvel")
data_leilao = st.date_input("Data do leilão")


# PALAVRAS DE RISCO
palavras_risco = [
    "revisional",
    "revisão contratual",
    "taxas abusivas",
    "juros abusivos",
    "embargos",
    "anulatória",
    "nulidade",
    "alienação fiduciária",
    "sustação de leilão",
    "falta de notificação",
    "ausência de notificação",
    "liminar",
    "tutela antecipada",
    "ação anulatória de consolidação de propriedade",
    "ação de anulação de leilão extrajudicial",
    "ação declaratória de nulidade de ato jurídico",
    "ausência de intimação pessoal",
    "vício na consolidação da propriedade",
    "preço vil",
    "teoria do adimplemento substancial",
    "irregularidade no edital",
    "tutela de urgência antecipada",
    "perigo da demora",
    "probabilidade do direito",
    "direito de preferência",
    "purgação da mora",
    "consignação em pagamento",
    "vício de edital",
    "agravo de instrumento com pedido de efeito suspensivo",
    "averbação premonitória",
    "teoria do desvio produtivo do consumidor",
]


# NORMALIZAÇÃO
def normalizar_nome(nome):
    nome = nome.lower()
    nome = unicodedata.normalize('NFKD', nome)
    nome = "".join([c for c in nome if not unicodedata.combining(c)])
    remover = [" de ", " da ", " dos ", " das "]
    for r in remover:
        nome = nome.replace(r, " ")
    return nome.strip()


def gerar_variacoes(nome):
    nome = normalizar_nome(nome)
    partes = nome.split()
    variacoes = []

    variacoes.append(nome)

    if len(partes) > 1:
        variacoes.append(partes[0] + " " + partes[-1])

    if len(partes) > 2:
        variacoes.append(partes[-1] + " " + partes[0])

    return list(set(variacoes))


# CLASSIFICAÇÃO DE RISCO
def classificar_risco(classe):
    classe_lower = classe.lower()

    for palavra in palavras_risco:
        if palavra in classe_lower:
            return "⚠ ALTO"

    return "🟢 BAIXO"


# BOTÃO
if st.button("Pesquisar processos"):

    if not nome:
        st.warning("Digite um nome para buscar")

    else:
        variacoes = gerar_variacoes(nome)

        st.write("Variações do nome utilizadas na busca:")
        st.write(variacoes)

        resultados = []

        for nome_busca in variacoes:
            try:
                dados = buscar_tjsp(nome_busca)
                resultados.extend(dados)
            except Exception as e:
                st.error(f"Erro ao consultar TJSP: {e}")

        if resultados:

            # FORMATA DATA + CLASSIFICA RISCO
            for item in resultados:
                try:
                    data_obj = datetime.strptime(item["Data"], "%d/%m/%Y")
                    item["Data"] = data_obj.strftime("%d/%m/%Y")
                except:
                    pass

                item["Risco"] = classificar_risco(item["Classe"])

            df = pd.DataFrame(resultados)

            st.subheader("Resultados encontrados")
            st.dataframe(df)

        else:
            st.warning("Nenhum processo encontrado")
