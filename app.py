import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Alpha Iron - Workout System", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ Alpha Iron Athletics — Sistema de Montagem de Treinos")

# 2. Barra Lateral: Periodização do Bloco
st.sidebar.header("⚙️ Configuração do Bloco")
bloco = st.sidebar.selectbox("Bloco de Treinamento", ["Bloco 1 - Força", "Bloco 2 - Engine", "Bloco 3 - Ginástica", "Bloco 4 - LPO"])
semana = st.sidebar.selectbox("Semana do Bloco", [
    "Semana 1 - Acumulação (Volume Mod / Int Mod)",
    "Semana 2 - Progressão (Volume Alto / Int Crescente)",
    "Semana 3 - Sobrecarga (Volume Ajustado / Maior Intensidade)",
    "Semana 4 - Deload / Benchmark (-30% a -40% Volume)"
])

st.sidebar.markdown("---")
st.sidebar.header("📊 Painel MCVS & IACS (Tempo Real)")

# 3. Exemplo de Cálculo MCVS & IACS
vol_squat = st.sidebar.number_input("Volume Agachar (Ideal: 120-180)", value=140)
vol_pull = st.sidebar.number_input("Volume Puxar Vertical (Ideal: 60-100)", value=80)
vol_run = st.sidebar.number_input("Volume Corrida em KM (Ideal: 6-12km)", value=8.5)

# Cálculo IACS para demonstração
pontos_iacs = (vol_squat * 0.2) + (vol_pull * 0.3) + (vol_run * 2)

st.sidebar.metric("Índice Alpha de Carga (IACS)", f"{int(pontos_iacs)} pts")

if pontos_iacs <= 45:
    st.sidebar.success("Classificação: Semana Leve")
elif pontos_iacs <= 60:
    st.sidebar.info("Classificação: Semana Moderada")
elif pontos_iacs <= 75:
    st.sidebar.warning("Classificação: Semana Pesada")
else:
    st.sidebar.error("Classificação: Semana de Choque")

# 4. Abas dos Dias da Semana
dias = ["Segunda (HYROX)", "Terça (Força/LPO)", "Quarta (Ginástica)", "Quinta (Engine)", "Sexta (ATHX)", "Sábado (Community)", "Domingo (CrossFit)"]
tabs = st.tabs(dias)

for i, tab in enumerate(tabs):
    with tab:
        st.subheader(f"Programação — {dias[i]}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 📋 Estrutura da Sessão (60 Min)")
            st.text_input(f"1. Briefing (2-3 min)", "Apresentação dos objetivos e estímulo", key=f"b_{i}")
            st.text_area(f"2. Aquecimento / Mobilidade (8-10 min)", "Mobilidade de Quadril/Tornozelo + 2 rounds leve", key=f"a_{i}")
            st.text_area(f"3. Bloco Técnico / Força (15-20 min)", "Back Squat 5x5 @ 75-80% RPE 8", key=f"f_{i}")
            st.text_area(f"4. Main WOD (10-20 min)", "AMRAP 12 min:\n- 10 Wall Balls\n- 8 Burpees\n- 200m Corrida", key=f"w_{i}")
            st.text_area(f"5. Acessórios & Core (5-10 min)", "3 Sets: 15 Hollow Rocks + 10 Bulgarian Split Squat", key=f"c_{i}")
            
        with col2:
            st.markdown("### 🎯 Escalas Automáticas (RX / INT / BEG)")
            st.info("O sistema converte o WOD selecionado para os diferentes níveis de alunos do box.")
            
            escala_df = pd.DataFrame({
                "Nível": ["RX", "Intermediate", "Beginner", "Masters"],
                "Carga / Movimento": ["20lb / Pull-ups", "14lb / Ring Rows", "10lb / Jumping Pull-ups", "10-14lb / Adaptação Livre"],
                "Volume Target": ["100%", "80%", "60%", "60-70%"]
            })
            st.table(escala_df)
            
            st.markdown("### 🔍 Checklist Metodológico")
            st.checkbox("O objetivo da sessão está claro?", value=True, key=f"chk1_{i}")
            st.checkbox("Existe apenas um movimento dominante?", value=True, key=f"chk2_{i}")
            st.checkbox("O treino cabe no tempo total de 60 minutos?", value=True, key=f"chk3_{i}")

# 5. Exportação
st.markdown("---")
if st.button("📄 Gerar Relatório e Exportar Treinos da Semana"):
    st.success("Programação validada e exportada com sucesso!")
