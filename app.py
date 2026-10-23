import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Alpha Iron Athletics 2.0 — Sistema de Gestão", 
    page_layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c23 100%);
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Alpha Iron Athletics 2.0")
st.subheader("Painel de Controle e Gestão Integrada")
st.markdown("---")

st.sidebar.header("Menu Principal")
menu = st.sidebar.radio(
    "Selecione o Módulo:",
    ["Visão Geral", "Gestão de Alunos", "Controle Financeiro", "Acessos & Turnstile (ABC EVO)", "Configurações"]
)

if menu == "Visão Geral":
    st.markdown("### 📊 Indicadores Principais")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Alunos Ativos", value="342", delta="+12 este mês")
    with col2:
        st.metric(label="Faturamento Mensal", value="R$ 45.890", delta="+5.4%")
    with col3:
        st.metric(label="Check-ins Hoje", value="189", delta="Normal")
    with col4:
        st.metric(label="Inadimplência", value="3.2%", delta="-0.8%", delta_color="inverse")
        
    st.markdown("---")
    st.info("Sistema integrado ao ABC EVO com reconhecimento facial e catracas operando normalmente.")

elif menu == "Gestão de Alunos":
    st.markdown("### 👥 Cadastro e Consulta de Alunos")
    busca = st.text_input("Pesquisar aluno por nome ou CPF:")
    dados_alunos = {
        "Nome": ["Carlos Silva", "Ana Souza", "Marcos Lima", "Beatriz Costa"],
        "Plano": ["Anual VIP", "Mensal", "Trimestral", "Anual VIP"],
        "Status": ["Ativo", "Ativo", "Pendente", "Ativo"],
        "Vencimento": ["15/11/2026", "20/10/2026", "05/09/2026", "10/12/2026"]
    }
    df_alunos = pd.DataFrame(dados_alunos)
    st.dataframe(df_alunos, use_container_width=True)

elif menu == "Controle Financeiro":
    st.markdown("### 💰 Fluxo de Caixa e Despesas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Receitas (Outubro)", "R$ 45.890,00")
    with col2:
        st.metric("Despesas Fixas", "R$ 18.500,00")
        
    st.markdown("#### Despesas Recorrentes Cadastradas:")
    st.markdown("- Aluguel (R. P. Zillig Negócios Imobiliários)")
    st.markdown("- Energia (Enel SP)")
    st.markdown("- Água (Sabesp)")
    st.markdown("- Manutenção Hidráulica (V M Da Silva Hidráulica)")

elif menu == "Acessos & Turnstile (ABC EVO)":
    st.markdown("### 🔐 Controle de Acesso e Reconhecimento Facial")
    st.success("Catracas sincronizadas com sucesso via ABC EVO.")
    st.code("[13:45:12] Carlos Silva - Reconhecimento Facial OK - Catraca 01\n[13:44:50] Ana Souza - Reconhecimento Facial OK - Catraca 02")

elif menu == "Configurações":
    st.markdown("### ⚙️ Configurações do Sistema")
    st.write("Versão do Sistema: Alpha Iron Athletics 2.0 (Build 2026.10)")
    st.checkbox("Modo de Manutenção", value=False)
    st.checkbox("Notificações Automáticas de Vencimento via WhatsApp", value=True)
