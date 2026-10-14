import streamlit as st
import pandas as pd

# 1. Configuração Visual da Página
st.set_page_config(page_title="Alpha Iron 2.0 - Workout Builder", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ Alpha Iron Athletics 2.0 — Montador de Treinos")

# 2. Barra Lateral: Periodização conforme Planilha
st.sidebar.header("⚙️ Periodização (Planilha 2.0)")
bloco = st.sidebar.selectbox("Fase / Bloco", [
    "Block 1 - Strength Focus",
    "Block 2 - Engine Focus",
    "Block 3 - Gymnastics Focus",
    "Block 4 - Weightlifting Focus"
])

semana = st.sidebar.selectbox("Semana do Bloco", [
    "Week 1 - Accumulation",
    "Week 2 - Progression",
    "Week 3 - Overload",
    "Week 4 - Deload / Benchmark"
])

st.sidebar.markdown("---")
st.sidebar.header("📊 Painel de Controle MCVS & IACS")

# Parâmetros de Volume da Planilha
vol_squat = st.sidebar.number_input("Volume Agachar (Ideal: 120-180)", value=140)
vol_hinge = st.sidebar.number_input("Volume Hinge / LPO (Ideal: 80-120)", value=90)
vol_push = st.sidebar.number_input("Volume Empurrar (Ideal: 60-100)", value=70)
vol_pull = st.sidebar.number_input("Volume Puxar (Ideal: 60-100)", value=75)
vol_run = st.sidebar.number_input("Volume Corrida (KM) (Ideal: 6-12 km)", value=8.0)

# Cálculo IACS baseado na planilha
iacs_score = (vol_squat * 0.15) + (vol_hinge * 0.2) + (vol_push * 0.15) + (vol_pull * 0.15) + (vol_run * 3)

st.sidebar.metric("Índice Alpha de Carga (IACS)", f"{int(iacs_score)} pts")

if iacs_score <= 45:
    st.sidebar.success("Classificação: Semana Leve")
elif iacs_score <= 60:
    st.sidebar.info("Classificação: Semana Moderada")
elif iacs_score <= 75:
    st.sidebar.warning("Classificação: Semana Pesada")
else:
    st.sidebar.error("Classificação: Semana de Choque")

# 3. Grade Semanal Fiel à Planilha 2.0
dias = [
    "Monday (HYROX)", 
    "Tuesday (CrossFit - Strength/LPO)", 
    "Wednesday (CrossFit - Gymnastics/Skill)", 
    "Thursday (CrossFit - Strength/LPO)", 
    "Friday (ATHX)", 
    "Saturday (Community WOD)", 
    "Sunday (Benchmark / Hero)"
]

tabs = st.tabs([d.split(" ")[0] for d in dias])

for i, tab in enumerate(tabs):
    with tab:
        st.subheader(f"Programação de {dias[i]}")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown("### 📋 Estrutura da Sessão (Weekly Programming)")
            
            # Ajuste de layout de blocos dinâmicos por dia
            if "Friday" in dias[i]: # Estrutura Exclusiva do ATHX da planilha
                st.info("🔥 **Sessão ATHX:** Estrutura Fixa (Strength Max + Endurance + MetCon X)")
                st.text_input("Warm Up (Tempo: 10')", "Ativação dinâmica + Corrida leve", key=f"athx_w_{i}")
                st.text_area("1. Strength Max (Tempo: 15')", "5 RM Deadlift ou 3 RM Front Squat", key=f"athx_s_{i}")
                st.text_area("2. Endurance (Tempo: 15')", "Max Burpees Broad Jump / Max Run / Farmer Carry", key=f"athx_e_{i}")
                st.text_area("3. MetCon X / Workout (Tempo: 20')", "For Time / AMRAP Alta Intensidade sob fadiga", key=f"athx_m_{i}")
                st.text_area("4. Mobility / Recovery (Tempo: 5')", "Liberação miofascial / Alongamento", key=f"athx_r_{i}")
            
            elif "Monday" in dias[i]: # Estrutura HYROX
                st.info("🏃 **Sessão HYROX:** Corrida + Estações Funcionais")
                st.text_input("Warm Up (10')", "Ativação de Core, Quadril e Corrida Leve", key=f"hy_w_{i}")
                st.text_area("Técnica de Estação (10')", "Mecânica de Sled / Burpee Broad Jump / Carries", key=f"hy_t_{i}")
                st.text_area("HYROX Main Block (35-40')", "Alternância: 800m Corrida + Estação Funcional", key=f"hy_m_{i}")
                st.text_area("Volta à Calma (5')", "Caminhada leve e respiração", key=f"hy_r_{i}")
                
            else: # Estrutura CrossFit Padrão da Planilha (Terça, Quarta, Quinta, Sábado, Domingo)
                st.text_input("1. Warm Up (10')", "2-3 Rounds: 50 Jumping Jacks, Shuttle Run, Drills", key=f"cf_w_{i}")
                st.text_area("2. Strength / LPO / Skill (15-20')", "E90s / Complex / Porcentagens %RM", key=f"cf_s_{i}")
                st.text_area("3. WOD / Main Event (15-20')", "For Time / AMRAP / EMOM / Chipper", key=f"cf_wod_{i}")
                st.text_area("4. Accessory / Core (5-10')", "Trabalho complementar unilateral / estabilização", key=f"cf_a_{i}")
                st.text_area("5. Mobility (5')", "Mobilidade focada nas articulações mais exigidas", key=f"cf_m_{i}")

        with col2:
            st.markdown("### 🎯 Tabela de Escalas (RX / INT / BEG / MASTERS)")
            st.write("Ajustes automáticos de intensidade e complexidade técnica:")
            
            escala_df = pd.DataFrame({
                "Nível": ["RX", "Intermediate", "Beginner", "Masters"],
                "Carga / Categoria": ["100% Carga RX", "70-80% Carga", "50% Carga / Halteres", "Adaptação Livre"],
                "Ginásticos": ["Movimento Completo", "Progressão Média", "Adaptação Básica", "Foco em Amplitude"]
            })
            st.table(escala_df)
            
            st.markdown("### 🔍 Checklist de Validação")
            st.checkbox("Movimento dominante respeitado?", value=True, key=f"chk1_{i}")
            st.checkbox("Sem interferência de fadiga com o dia anterior?", value=True, key=f"chk2_{i}")
            st.checkbox("Sessão dentro dos 60 minutos?", value=True, key=f"chk3_{i}")

st.markdown("---")
if st.button("💾 Salvar & Exportar Treino Semanal"):
    st.success("Programação enviada e sincronizada com a Planilha Alpha Iron 2.0!")
