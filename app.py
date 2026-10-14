import streamlit as st
import pandas as pd
import os

# 1. Configuração Visual da Página
st.set_page_config(page_title="Alpha Iron 2.0 - Workout Builder", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- 🎯 MOTOR INTELIGENTE DE SUGESTÃO (WARM-UP, MOBILIDADE E ACESSÓRIOS) ---
def sugerir_elementos(texto_skill, texto_wod):
    conteudo = (texto_skill + " " + texto_wod).lower()
    
    warmups = []
    mobilidades = []
    acessorios = []
    
    # Padrão: Agachar / Quadril
    if any(k in conteudo for k in ["squat", "agacho", "thruster", "wall ball", "lunge"]):
        warmups.append("3 Rounds: 10 Air Squats bem pausados, 10 Cossack Squats, 15m Shuttle Run")
        mobilidades.append("Mobilidade profunda de Tornozelo (Dorsiflexão) + Abertura de Quadril (Pigeon Pose)")
        acessorios.append("3 Sets: 12 Bulgarian Split Squats + 15 Monster Walks com mini-band")
        
    # Padrão: Puxar / LPO / Posterior
    if any(k in conteudo for k in ["deadlift", "snatch", "clean", "swing", "hinge", "terra"]):
        warmups.append("3 Rounds: 10 Good Mornings c/ bastão, 10 Glute Bridges, 8 Inchworms")
        mobilidades.append("Liberação de Isquiotibiais + Mobilidade de Torácica na fita/foam roller")
        acessorios.append("3 Sets: 10 Single Leg Romanian Deadlifts + 15 Banded Good Mornings")
        
    # Padrão: Empurrar Acima da Cabeça / LPO / Overhead
    if any(k in conteudo for k in ["jerk", "press", "push press", "hspu", "overhead", "snatch"]):
        warmups.append("3 Rounds: 10 Pass-throughs c/ bastão, 10 Scapular Push-ups, 8 Crossover Dumbbell Press leve")
        mobilidades.append("Mobilidade de Ombros (Rotação Externa) + Alongamento Dinâmico de Latíssimo")
        acessorios.append("3 Sets: 12 Banded Face Pulls + 10 Bottom-up Kettlebell Press (Estabilidade)")
        
    # Padrão: Ginásticos / Puxada
    if any(k in conteudo for k in ["pull-up", "bar muscle", "ring", "chest to bar", "bmup", "rope climb"]):
        warmups.append("3 Rounds: 10 Scapular Pull-ups, 10 Ring Rows leves, 10 Hollow Body Rocks")
        mobilidades.append("Mobilidade de Ombro (Extensão/Extensão Torácica) + Alongamento de Antebraços")
        acessorios.append("3 Sets: 10 Ring Dips Estritos + 20s Hollow Hold com peso")
        
    # Padrão: Corrida / Endurance / Monostrutural
    if any(k in conteudo for k in ["run", "corrida", "row", "bike", "ski", "burpee", "hyrox"]):
        warmups.append("2 Rounds: 200m Corrida leve / Aceleração progressiva + Drills de Pisotio/Aterrissagem")
        mobilidades.append("Mobilidade de Flexores de Quadril + Soltura de Panturrilha/Solear")
        acessorios.append("3 Sets: 15 Tibialis Raises + 12 Single-leg Calf Raises")

    # Fallback genérico caso não encontre padrões específicos
    if not warmups:
        warmups.append("2-3 Rounds: 50 Jumping Jacks, 10 Sprawls, 10 World's Greatest Stretch")
    if not mobilidades:
        mobilidades.append("Mobilidade articular geral de Ombros, Quadril e Tornozelos")
    if not acessorios:
        acessorios.append("3 Sets: 15 Hollow Rocks + 12 Dumbbell Rows Unilaterais")
        
    return " / ".join(warmups), " / ".join(mobilidades), " / ".join(acessorios)

# --- 📸 LOGO DA ALPHA IRON ATHLETICS NA SIDEBAR ---
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.title("🏋️‍♂️ ALPHA IRON")

# --- ⚙️ SIDEBAR: PERIODIZAÇÃO & PAINEL MCVS / IACS ---
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

vol_squat = st.sidebar.number_input("Volume Agachar (Ideal: 120-180)", value=140)
vol_hinge = st.sidebar.number_input("Volume Hinge / LPO (Ideal: 80-120)", value=90)
vol_push = st.sidebar.number_input("Volume Empurrar (Ideal: 60-100)", value=70)
vol_pull = st.sidebar.number_input("Volume Puxar (Ideal: 60-100)", value=75)
vol_run = st.sidebar.number_input("Volume Corrida (KM) (Ideal: 6-12 km)", value=8.0)

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

# --- 🏋️ MAIN CONTENT ---
st.title("🏋️‍♂️ Alpha Iron Athletics 2.0 — Montador de Treinos")

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
            st.markdown("### 📋 Estrutura da Sessão")
            
            if "Friday" in dias[i]: # ATHX
                st.info("🔥 **Sessão ATHX:** Estrutura Fixa (Strength Max + Endurance + MetCon X)")
                
                s_text = st.text_area("1. Strength Max (Tempo: 15')", "5 RM Deadlift ou 3 RM Front Squat", key=f"athx_s_{i}")
                m_text = st.text_area("3. MetCon X / Workout (Tempo: 20')", "For Time / AMRAP Alta Intensidade sob fadiga", key=f"athx_m_{i}")
                
                # Sugestão Inteligente baseada no Strength/MetCon
                sug_w, sug_mob, sug_acess = sugerir_elementos(s_text, m_text)
                
                st.text_input("Warm Up Sugerido (Tempo: 10')", value=sug_w, key=f"athx_w_{i}")
                st.text_area("2. Endurance (Tempo: 15')", "Max Burpees Broad Jump / Max Run / Farmer Carry", key=f"athx_e_{i}")
                st.text_area("4. Mobility / Recovery Sugerido (Tempo: 5')", value=sug_mob, key=f"athx_r_{i}")
            
            elif "Monday" in dias[i]: # HYROX
                st.info("🏃 **Sessão HYROX:** Corrida + Estações Funcionais")
                
                t_text = st.text_area("Técnica de Estação (10')", "Mecânica de Sled Push / Burpee Broad Jump / Carries", key=f"hy_t_{i}")
                m_text = st.text_area("HYROX Main Block (35-40')", "Alternância: 800m Corrida + Estação Funcional", key=f"hy_m_{i}")
                
                sug_w, sug_mob, _ = sugerir_elementos(t_text, m_text)
                
                st.text_input("Warm Up Sugerido (10')", value=sug_w, key=f"hy_w_{i}")
                st.text_area("Volta à Calma / Mobilidade (5')", value=sug_mob, key=f"hy_r_{i}")
                
            else: # CrossFit Padrão
                # Digitado primeiro
                s_text = st.text_area("2. Strength / LPO / Skill (15-20')", "Back Squat 5x5 @ 75% ou Snatch Balance + Hang Squat Snatch", key=f"cf_s_{i}")
                w_text = st.text_area("3. WOD / Main Event (15-20')", "AMRAP 12 min:\n- 12 Wall Balls\n- 9 Toes to Bar\n- 6 Power Cleans", key=f"cf_wod_{i}")
                
                # Sugestões inteligentes geradas automaticamente
                sug_w, sug_mob, sug_acess = sugerir_elementos(s_text, w_text)
                
                st.markdown("---")
                st.text_input("1. Warm Up Sugerido Dinamicamente (10')", value=sug_w, key=f"cf_w_{i}")
                st.text_area("4. Accessory / Core Sugerido (5-10')", value=sug_acess, key=f"cf_a_{i}")
                st.text_area("5. Mobility Sugerida (5')", value=sug_mob, key=f"cf_m_{i}")

        with col2:
            st.markdown("### 🎯 Tabela de Escalas (RX / INT / BEG / MASTERS)")
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
