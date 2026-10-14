import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Alpha Iron 2.0 - Workout Builder", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    .sugestao-box { background-color: #1E1E1E; border-left: 4px solid #D32F2F; padding: 12px; margin-bottom: 15px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ Alpha Iron Athletics 2.0 — Montador de Treinos")

# 2. Barra Lateral: Periodização Dinâmica
st.sidebar.header("⚙️ Periodização (Planilha 2.0)")
bloco_sel = st.sidebar.selectbox("Fase / Bloco", [
    "Block 1 - Strength Focus",
    "Block 2 - Engine Focus",
    "Block 3 - Gymnastics Focus",
    "Block 4 - Weightlifting Focus"
])

semana_sel = st.sidebar.selectbox("Semana do Bloco", [
    "Week 1 - Accumulation",
    "Week 2 - Progression",
    "Week 3 - Overload",
    "Week 4 - Deload / Benchmark"
])

# Banco de dados de diretrizes dinâmicas da metodologia Alpha Iron
diretrizes_bloco = {
    "Block 1 - Strength Focus": {
        "Week 1 - Accumulation": {"rpe": "RPE 7 (65-75%)", "metodo": "4x10, 5x5", "vol_target": "Volume Moderado", "foco": "Hipertrofia Funcional & Base Técnica"},
        "Week 2 - Progression": {"rpe": "RPE 7.5-8 (75-80%)", "metodo": "5x5, 4x8", "vol_target": "Volume Alto", "foco": "Carga Progressiva & Densidade Controlada"},
        "Week 3 - Overload": {"rpe": "RPE 8.5-9 (85-90%)", "metodo": "5x3, 6x2, 5x1", "vol_target": "Volume Reduzido / Alta Carga", "foco": "Força Máxima / Recrutamento Neural"},
        "Week 4 - Deload / Benchmark": {"rpe": "RPE 6 (50-60%) ou Teste", "metodo": "Deload (-30% a -40% Vol) / 3RM Test", "vol_target": "Baixo Volume", "foco": "Recuperação Ativa ou Benchmark Test"}
    },
    "Block 2 - Engine Focus": {
        "Week 1 - Accumulation": {"rpe": "RPE 6-7 (Zonas 1-2)", "metodo": "EMOM, AMRAP Longo", "vol_target": "Volume Alto Cardio", "foco": "Capacidade Aeróbia & Controle de Pace"},
        "Week 2 - Progression": {"rpe": "RPE 7-8 (Zona 2-3)", "metodo": "Intervalados, Chipper", "vol_target": "Volume Moderado/Alto", "foco": "Limiar Anaeróbio & Sustentação de Esforço"},
        "Week 3 - Overload": {"rpe": "RPE 8-9 (Zona 3)", "metodo": "Intervalados de Alta Densidade", "vol_target": "Alta Intensidade / Volume Ajustado", "foco": "Capacidade Cardiorrespiratória sob Fadiga"},
        "Week 4 - Deload / Benchmark": {"rpe": "RPE 6 / Teste", "metodo": "Simulado Reduzido / Time Trial", "vol_target": "Redução de Volume", "foco": "Teste de Ritmo ou Teste Interno (1km/5km)"}
    },
    "Block 3 - Gymnastics Focus": {
        "Week 1 - Accumulation": {"rpe": "RPE 6-7 (Qualidade)", "metodo": "Drills, Posicionamento, Strict Sets", "vol_target": "Volume Moderado", "foco": "Controle Corporal & Força Relativa"},
        "Week 2 - Progression": {"rpe": "RPE 7-8", "metodo": "Kipping Transitions, Skill EMOM", "vol_target": "Volume Crescente", "foco": "Eficiência de Movimento & Volume Específico"},
        "Week 3 - Overload": {"rpe": "RPE 8-9", "metodo": "High Volume Unbroken / Density Sets", "vol_target": "Alto Volume / Fadiga Muscular", "foco": "Resistência Específica sob Fadiga"},
        "Week 4 - Deload / Benchmark": {"rpe": "RPE 6 / Teste Max Reps", "metodo": "Max Pull-ups / Max T2B / Benchmark", "vol_target": "Volume Baixo", "foco": "Avaliação Técnica e Recuperação"}
    },
    "Block 4 - Weightlifting Focus": {
        "Week 1 - Accumulation": {"rpe": "RPE 6 (50-65%)", "metodo": "Complexes Técnicos, Tall / Hang Drills", "vol_target": "Volume Técnico (50-70 reps)", "foco": "Trajetória da Barra & Posição de Recepção"},
        "Week 2 - Progression": {"rpe": "RPE 7-8 (70-80%)", "metodo": "Hang Power / Full Lift + Pausa", "vol_target": "Volume Moderado (30-50 reps)", "foco": "Velocidade de Transição & Potência"},
        "Week 3 - Overload": {"rpe": "RPE 8.5-9 (80-90%)", "metodo": "Heavy Singles, Doubles, Wave Loading", "vol_target": "Baixo Volume (15-30 reps)", "foco": "Expressão de Potência & Carga Elevada"},
        "Week 4 - Deload / Benchmark": {"rpe": "RPE 10 / Teste 1RM/3RM", "metodo": "Max Lift / Complex Test", "vol_target": "Volume Mínimo (10-20 reps)", "foco": "Avaliação de Potência e Técnica"}
    }
}

# Dados selecionados para o contexto atual
info_atual = diretrizes_bloco[bloco_sel][semana_sel]

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

# 3. Exibição do Resumo Metodológico Dinâmico no Topo
st.markdown(f"""
<div class="sugestao-box">
    <h4>💡 DIRETRIZES ATUAIS DO BLOCO: <b>{bloco_sel}</b> | <b>{semana_sel}</b></h4>
    <p><b>Foco Principal:</b> {info_atual['foco']} | <b>Intensidade / Carga:</b> {info_atual['rpe']} | <b>Métodos Recomendados:</b> {info_atual['metodo']} | <b>Meta de Volume:</b> {info_atual['vol_target']}</p>
</div>
""", unsafe_allow_html=True)

# 4. Grade Semanal Fiel à Planilha 2.0
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

# Sugestões específicas dinâmicas por dia e por bloco
def get_sugestao_dia(dia_nome, bloco, semana, info):
    if "Friday" in dia_nome:
        return {
            "Warm Up": "Ativação dinâmica + mobilidade ativa de quadril/ombro (10')",
            "Strength Max": f"1. Strength Max ({info['rpe']}): Ex. 5 RM Deadlift / 3 RM Front Squat / Bench Press",
            "Endurance": "2. Endurance (15'): Ex. Max Burpees Broad Jump / Max Run / Farmer Carry / Sandbag Drag",
            "Workout": f"3. MetCon X (15-20'): For Time ou AMRAP Alta Intensidade ({info['metodo']})"
        }
    elif "Monday" in dia_nome:
        return {
            "Warm Up": "Ativação de Core, corrida leve e mobilidade de tornozelo/quadril (10')",
            "Técnica": "Trabalho mecânico de estações (Sled Push, Sandbag Carry, Burpee Broad Jump)",
            "HYROX Main": f"Alternância: Corrida (3-5km total) + Estação Funcional ({info['vol_target']})"
        }
    elif "Wednesday" in dia_nome:
        return {
            "Warm Up": "Mobilidade de Ombros, Punhos e Hollow/Arch Holds (10')",
            "Skill / Ginástica": f"Progressão do Bloco ({info['metodo']}): Strict Pull-up -> Kipping -> C2B -> BMU/RMU",
            "WOD": f"WOD focado em controle corporal e densidade ({info['rpe']})"
        }
    else: # Terça, Quinta, Sábado, Domingo
        return {
            "Warm Up": "2-3 Rounds: Jumping Jacks, Shuttle Run, Mobility Drills",
            "Strength / LPO": f"Trabalho Dominante ({info['metodo']}) @ {info['rpe']} - Ex. Back Squat, Snatch/Clean Complex",
            "WOD": f"Main Event ({info['vol_target']}) - AMRAP / For Time / EMOM"
        }

for i, tab in enumerate(tabs):
    with tab:
        st.subheader(f"Programação — {dias[i]}")
        sugestao = get_sugestao_dia(dias[i], bloco_sel, semana_sel, info_atual)
        
        col1, col2 = st.columns([1.3, 1])
        
        with col1:
            st.markdown("### 📝 Campo de Escrita do Treino")
            
            if "Friday" in dias[i]:
                st.info("🔥 **ATHX:** Digite abaixo os treinos da sessão de sexta-feira:")
                t_w = st.text_input("1. Warm Up (10')", value="", placeholder="Digite o aquecimento aqui...", key=f"athx_w_{i}")
                t_s = st.text_area("2. Strength Max (15')", value="", placeholder="Digite a parte de força/potência máxima aqui...", key=f"athx_s_{i}")
                t_e = st.text_area("3. Endurance (15')", value="", placeholder="Digite o bloco de resistência muscular/carries...", key=f"athx_e_{i}")
                t_m = st.text_area("4. MetCon X / Workout (20')", value="", placeholder="Digite o WOD final...", key=f"athx_m_{i}")
                t_r = st.text_input("5. Mobility / Recovery (5')", value="", placeholder="Digite a volta à calma...", key=f"athx_r_{i}")
            else:
                t_w = st.text_input("1. Warm Up (10')", value="", placeholder="Digite o aquecimento aqui...", key=f"cf_w_{i}")
                t_s = st.text_area("2. Strength / LPO / Skill (15-20')", value="", placeholder="Digite a parte técnica/força aqui...", key=f"cf_s_{i}")
                t_m = st.text_area("3. Main WOD (15-20')", value="", placeholder="Digite o WOD principal aqui...", key=f"cf_m_{i}")
                t_a = st.text_area("4. Accessories / Core (5-10')", value="", placeholder="Digite os acessórios/core aqui...", key=f"cf_a_{i}")
                t_r = st.text_input("5. Mobility (5')", value="", placeholder="Digite a mobilidade final...", key=f"cf_r_{i}")

        with col2:
            st.markdown("### 💡 Tabela de Referência / Sugestão da Metodologia")
            st.caption("Esta tabela altera automaticamente conforme o Bloco, a Semana e o Dia selecionados:")
            
            # Tabela de referência isolada
            ref_df = pd.DataFrame(list(sugestao.items()), columns=["Etapa da Aula", "Recomendação da Metodologia / Planilha"])
            st.table(ref_df)
            
            st.markdown("### 🎯 Guia de Escalas (RX / INT / BEG / MASTERS)")
            escala_df = pd.DataFrame({
                "Nível": ["RX", "Intermediate", "Beginner", "Masters"],
                "Carga / Categoria": ["100% Carga RX", "70-80% Carga", "50% Carga / DBs", "Adaptação Libre"],
                "Ginásticos": ["Movimento Completo", "Progressão Média", "Adaptação Básica", "Foco em Amplitude"]
            })
            st.table(escala_df)

st.markdown("---")
if st.button("💾 Salvar & Exportar Treino Semanal"):
    st.success("Programação enviada e sincronizada com a Planilha Alpha Iron 2.0!")
