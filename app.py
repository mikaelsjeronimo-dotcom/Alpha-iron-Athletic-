import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Alpha Iron Athletics 2.0 — Sistema de Gestão", 
    layout="wide",
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
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    </style>
""", unsafe_allow_html=True)

# Barra Lateral (Sidebar)
st.sidebar.markdown("👤 **Logado como:** Mikael Santos")
if st.sidebar.button("Sair / Logout"):
    st.sidebar.info("Sessão encerrada.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Menu Principal")
menu = st.sidebar.radio(
    "Navegação",
    [
        "Início (Dashboard)", 
        "Programação Semanal", 
        "Montagem de Treinos", 
        "Biblioteca de WODs", 
        "Biblioteca de Exercícios", 
        "Treinos Salvos"
    ],
    label_visibility="collapsed"
)

# Conteúdo das Páginas
if menu == "Início (Dashboard)":
    st.title("Alpha Iron Athletics 2.0")
    st.subheader("Painel de Controle e Gestão da Academia")
    st.markdown("---")

    st.markdown("### 🚀 Atalhos Rápidos")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("Programação Semanal", use_container_width=True):
            pass
    with col_b:
        if st.button("Montar / Editar Treinos", use_container_width=True):
            pass
    with col_c:
        if st.button("Treinos Salvos", use_container_width=True):
            pass

    st.markdown("---")
    st.markdown("### 📊 Resumo de Volume da Semana")
    
    data_volume = {
        "Padrão de Movimento": ["Squat", "Bench Press", "Deadlift", "Pull-up", "Conditioning"],
        "Meta": [170, 140, 120, 150, 180],
        "Programado": [0, 0, 0, 0, 0],
        "Realizado": [0, 0, 0, 0, 0]
    }
    df_volume = pd.DataFrame(data_volume)
    st.dataframe(df_volume, use_container_width=True)

elif menu == "Programação Semanal":
    st.title("📅 Programação Semanal")
    st.markdown("Gerencie e visualize a programação de treinos por dia da semana.")
    
    dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_selecionado = st.selectbox("Selecione o Dia:", dias)
    
    st.info(f"Programação atual para: **{dia_selecionado}**")
    st.text_area("WOD / Treino do Dia:", "Ex: Aquecimento + Força + WOD Metcon")

elif menu == "Montagem de Treinos":
    st.title("🏋️ Montagem de Treinos")
    st.markdown("Crie novas estruturas de treinos e defina cargas, séries e repetições.")
    
    with st.form("form_treino"):
        nome_treino = st.text_input("Nome do Treino / WOD")
        tipo = st.selectbox("Tipo de Treino", ["Força (Strength)", "Conditioning (WOD)", "Gymnastics", "Endurance"])
        detalhes = st.text_area("Descrição detalhada dos blocos de exercício")
        submit = st.form_submit_button("Salvar Treino")
        if submit:
            st.success(f"Treino '{nome_treino}' salvo com sucesso!")

elif menu == "Biblioteca de WODs":
    st.title("📚 Biblioteca de WODs")
    st.markdown("Consulte wods clássicos e treinos cadastrados no sistema.")
    
    wods_exemplo = {
        "Nome do WOD": ["Fran", "Cindy", "Murph", "Grace"],
        "Tipo": ["AMRAP / Metcon", "AMRAP 20 min", "Hero WOD", "For Time (30 Lifts)"],
        "Foco": ["Thrusters & Pull-ups", "Pull, Push, Squat", "Run, Pull, Push, Squat", "Clean and Jerk"]
    }
    st.dataframe(pd.DataFrame(wods_exemplo), use_container_width=True)

elif menu == "Biblioteca de Exercícios":
    st.title("💪 Biblioteca de Exercícios")
    st.markdown("Lista completa de movimentos e padrões de movimento disponíveis.")
    
    exercicios = {
        "Exercício": ["Back Squat", "Front Squat", "Deadlift", "Clean & Jerk", "Snatch", "Pull-up", "Muscle-up"],
        "Grupo Muscular": ["Pernas", "Pernas", "Cadeia Posterior", "Full Body", "Full Body", "Costas / Braços", "Upper Body"],
        "Padrão": ["Squat", "Squat", "Hinge", "Olympic", "Olympic", "Pull", "Pull"]
    }
    st.dataframe(pd.DataFrame(exercicios), use_container_width=True)

elif menu == "Treinos Salvos":
    st.title("💾 Treinos Salvos")
    st.markdown("Histórico de treinos criados e salvos no sistema.")
    st.info("Nenhum treino personalizado salvo recentemente. Utilize a aba 'Montagem de Treinos' para criar novos.")
