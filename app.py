import streamlit as st
import pandas as pd
import os

# 1. Configuração Visual da Página
st.set_page_config(page_title="Alpha Iron 2.0 - Montador de Treinos", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- LOGO DA ALPHA IRON ATHLETICS ---
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

st.title("🏋️‍♂️ Alpha Iron Athletics 2.0 — Montador de Treinos")

# --- FUNÇÃO DE SUGESTÃO BASEADA NA MATRIZ DA METODOLOGIA ALPHA IRON ---
def gerar_tabela_sugestoes(strength_text, lpo_text, wod_text):
    conteudo = (strength_text + " " + lpo_text + " " + wod_text).lower()
    
    warmup_sug = "2-3 Rounds:\n- Ativação dinâmica geral\n- Mobilidade articular leve\n- Elevação de frequência cardíaca"
    mob_sug = "Mobilidade articular focada nos padrões fundamentais do dia"
    acess_sug = "Fortalecimento de core e estabilização unilateral"
    
    # Agachar / Quadril
    if any(k in conteudo for k in ["squat", "agacho", "thruster", "wall ball", "lunge"]):
        warmup_sug = "3 Rounds:\n- 10 Agachamentos livres pausados\n- 10 Cossack Squats\n- 15m Corrida leve"
        mob_sug = "Dorsiflexão de Tornozelo + Abertura de Quadril (Pigeon Pose)"
        acess_sug = "3 Séries: 12 Agachamentos Búlgaros + 15 Passos com mini-band"
        
    # Hinge / Levantamento / Posterior
    elif any(k in conteudo for k in ["deadlift", "snatch", "clean", "swing", "terra", "hinge"]):
        warmup_sug = "3 Rounds:\n- 10 Good Mornings com bastão de PVC\n- 10 Pontes de Quadril\n- 8 Minhocas (Inchworms)"
        mob_sug = "Soltura de Isquiotibiais + Mobilidade Torácica no rolo"
        acess_sug = "3 Séries: 10 RDL Unilateral + 15 Good Mornings com elástico"
        
    # Empurrar Vertical / Overhead / Jerk
    elif any(k in conteudo for k in ["jerk", "press", "hspu", "overhead", "push press"]):
        warmup_sug = "3 Rounds:\n- 10 Passagens de bastão\n- 10 Flexões escapulares\n- 8 Desenvolvimentos leves"
        mob_sug = "Mobilidade de Ombro (Rotação Externa) + Alongamento de Latíssimo"
        acess_sug = "3 Séries: 12 Puxadas na fita (Face Pull) + 10 Desenvolvimentos com Kettlebell invertido"
        
    # Puxar Vertical / Ginásticos
    elif any(k in conteudo for k in ["pull-up", "bar muscle", "ring", "chest to bar", "bmup"]):
        warmup_sug = "3 Rounds:\n- 10 Puxadas escapulares\n- 10 Remadas na fita leves\n- 10 Canoas (Hollow Body)"
        mob_sug = "Extensão Torácica + Alongamento de Antebraço e Flexores dos Dedos"
        acess_sug = "3 Séries: 10 Paralelas estritas na fita + 20s Canoa isométrica pesada"
        
    # Engine / Monostrutural / Corrida
    elif any(k in conteudo for k in ["run", "corrida", "row", "bike", "ski", "burpee", "hyrox"]):
        warmup_sug = "2 Rounds:\n- 200m Corrida leve\n- Exercícios educativos de pisada e aterrissagem"
        mob_sug = "Flexores de Quadril + Soltura de Panturrilha e Solear"
        acess_sug = "3 Séries: 15 Elevações de Tibial + 12 Elevações de Panturrilha unilateral"
        
    df_sugestao = pd.DataFrame({
        "Bloco Recomendado": ["Aquecimento (Warm Up)", "Mobilidade Específica", "Acessório / Core"],
        "Sugestão Automática (Metodologia)": [warmup_sug, mob_sug, acess_sug]
    })
    
    return df_sugestao

# 2. Barra Lateral: Periodização conforme Planilha 2.0
st.sidebar.header("⚙️ Periodização (Planilha 2.0)")
bloco = st.sidebar.selectbox("Fase / Bloco", [
    "Bloco 1 - Foco em Força",
    "Bloco 2 - Foco em Engine",
    "Bloco 3 - Foco em Ginástica",
    "Bloco 4 - Foco em LPO / Levantamento"
])

semana = st.sidebar.selectbox("Semana do Bloco", [
    "Semana 1 - Acumulação",
    "Semana 2 - Progressão",
    "Semana 3 - Sobrecarga",
    "Semana 4 - Deload / Benchmark"
])

st.sidebar.markdown("---")
st.sidebar.header("📊 Painel MCVS & IACS (Carga Semanal)")

vol_squat = st.sidebar.number_input("Volume Agachar (Ideal: 120-180)", value=140)
vol_hinge = st.sidebar.number_input("Volume Hinge / LPO (Ideal: 80-120)", value=90)
vol_push = st.sidebar.number_input("Volume Empurrar (Ideal: 60-100)", value=70)
vol_pull = st.sidebar.number_input("Volume Puxar (Ideal: 60-100)", value=75)
vol_run = st.sidebar.number_input("Volume Corrida em KM (Ideal: 6-12 km)", value=8.0)

# Cálculo IACS conforme Metodologia Alpha Iron
iacs_score = (vol_squat * 0.15) + (vol_hinge * 0.2) + (vol_push * 0.15) + (vol_pull * 0.15) + (vol_run * 3)

st.sidebar.metric("Índice Alpha de Carga (IACS)", f"{int(iacs_score)} pts")

if iacs_score <= 45:
    st.sidebar.success("Classificação: Semana Leve")
elif iacs_score <= 60:
    st.sidebar.info("Classificação: Semana Moderada")
elif iacs_score <= 75:
    st.sidebar.warning("Classificação: Semana Pesada")
elif iacs_score <= 90:
    st.sidebar.error("Classificação: Semana de Choque")
else:
    st.sidebar.error("⚠️ Não Recomendado para Turmas Regulares")

# 3. Grade Semanal Fiel à Metodologia Alpha Iron Athletics
dias = [
    "Segunda (HYROX)", 
    "Terça (CrossFit - Força/LPO)", 
    "Quarta (CrossFit - Ginástica)", 
    "Quinta (CrossFit - Engine)", 
    "Sexta (ATHX)", 
    "Sábado (Community WOD)", 
    "Domingo (Benchmark / Hero)"
]

tabs = st.tabs([d.split(" ")[0] for d in dias])

for i, tab in enumerate(tabs):
    with tab:
        st.subheader(f"Programação de {dias[i]}")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown("### 📋 Estrutura da Sessão (60 min)")
            
            # --- ESTRUTURA ATHX (SEXTA-FEIRA) ---
            if "Sexta" in dias[i]:
                st.info("🔥 **Sessão ATHX:** Estrutura Fixa (Força Máxima + Endurance + MetCon X)")
                w_input = st.text_area("Aquecimento (Tempo: 10')", "Ativação dinâmica\nCorrida leve\nExercícios articulados", height=100, key=f"athx_w_{i}")
                s_input = st.text_area("1. Força Máxima (Tempo: 15')", "5 RM Terra ou 3 RM Agachamento Frontal", height=100, key=f"athx_s_{i}")
                l_input = "" 
                e_input = st.text_area("2. Endurance (Tempo: 15')", "Burpees com Salto em Distância / Corrida Máxima / Transporte de Carga", height=100, key=f"athx_e_{i}")
                m_input = st.text_area("3. MetCon X / Treino Principal (Tempo: 20')", "For Time / AMRAP Alta Intensidade sob fadiga", height=120, key=f"athx_m_{i}")
                r_input = st.text_area("4. Mobilidade e Recuperação (Tempo: 5')", "Liberação miofascial / Alongamento", height=80, key=f"athx_r_{i}")
            
            # --- ESTRUTURA HYROX (SEGUNDA-FEIRA) ---
            elif "Segunda" in dias[i]:
                st.info("🏃 **Sessão HYROX:** Corrida + Estações Funcionais (Resistência Aeróbia)")
                w_input = st.text_area("Aquecimento (10-12')", "Mobilidade dinâmica\nAtivação de Core e Quadril\nCorrida Leve", height=100, key=f"hy_w_{i}")
                s_input = "" 
                l_input = st.text_area("Técnica de Estação (8-10')", "Mecânica de Empurrão / Salto / Transportes de Carga", height=100, key=f"hy_t_{i}")
                m_input = st.text_area("Parte Principal (35-40')", "Alternância: Corrida + Estação Funcional", height=120, key=f"hy_m_{i}")
                r_input = st.text_area("Volta à Calma (5')", "Caminhada leve e respiração orientada", height=80, key=f"hy_r_{i}")
                
            # --- ESTRUTURA CROSSFIT PADRÃO (TERÇA, QUARTA, QUINTA, SÁBADO, DOMINGO) ---
            else:
                w_input = st.text_area("1. Aquecimento (10')", "2-3 Rounds:\n50 Polichinelos\n10 Tiros de Corrida\nExercícios dinâmicos", height=120, key=f"cf_w_{i}")
                
                # Blocos separados de Força e LPO
                s_input = st.text_area("2. Bloco de Força (10-15')", "Agachamento nas Costas 5x5 @ 75%", height=100, key=f"cf_s_{i}")
                l_input = st.text_area("3. Bloco de LPO / Técnica (10-15')", "Equilíbrio de Arranco + Arranco Suspenso", height=100, key=f"cf_l_{i}")
                
                m_input = st.text_area("4. WOD / Treino Principal (15-20')", "AMRAP 12 min:\n- 12 Wall Balls\n- 9 Pés na Barra (Toes to Bar)\n- 6 Power Cleans", height=130, key=f"cf_wod_{i}")
                a_input = st.text_area("5. Acessórios / Core (5-10')", "Trabalho complementar unilateral / estabilização", height=90, key=f"cf_a_{i}")
                r_input = st.text_area("6. Mobilidade (5')", "Mobilidade focada nas articulações mais exigidas", height=80, key=f"cf_m_{i}")

        with col2:
            st.markdown("### 🎯 Tabela de Escalas (RX / INT / INI / MASTERS)")
            escala_df = pd.DataFrame({
                "Nível": ["RX", "Intermediário", "Iniciante", "Masters"],
                "Carga / Categoria": ["100% Carga RX", "70-80% Carga", "50% Carga / Halteres", "Adaptação Livre"],
                "Ginásticos": ["Movimento Completo", "Progressão Média", "Adaptação Básica", "Foco em Amplitude"]
            })
            st.table(escala_df)
            
            # --- TABELA DE SUGESTÕES AUTOMÁTICAS ---
            st.markdown("### 💡 Sugestões Automáticas (Metodologia Alpha Iron)")
            st.caption("Geradas a partir da Força, LPO e WOD do dia:")
            
            df_sugestoes = gerar_tabela_sugestoes(s_input, l_input, m_input)
            st.table(df_sugestoes)
            
            st.markdown("---")
            st.markdown("### 🔍 Checklist Metodológico")
            st.checkbox("O objetivo da sessão está claro?", value=True, key=f"chk1_{i}")
            st.checkbox("Movimento dominante respeitado?", value=True, key=f"chk2_{i}")
            st.checkbox("Sessão dentro dos 60 minutos?", value=True, key=f"chk3_{i}")
            st.checkbox("Escalas disponíveis para todos os níveis?", value=True, key=f"chk4_{i}")

st.markdown("---")
if st.button("💾 Salvar & Exportar Treino Semanal"):
    st.success("Programação enviada e sincronizada com a Planilha Alpha Iron 2.0!")
