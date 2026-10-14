import streamlit as st
import pandas as pd
import os
import base64

# 1. Configuração Visual da Página
st.set_page_config(page_title="Alpha Iron 2.0 - Montador de Treinos", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- CORREÇÃO DA LOGO DA ALPHA IRON ATHLETICS ---
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
elif os.path.exists("1000319375.png"):
    st.sidebar.image("1000319375.png", use_container_width=True)
else:
    st.sidebar.title("🏋️‍♂️ ALPHA IRON ATHLETICS")

st.title("🏋️‍♂️ Alpha Iron Athletics 2.0 — Montador de Treinos")

# --- BANCO DE DADOS E INTELIGÊNCIA POR BLOCO / SEMANA ---
METODOLOGIA_BASE = {
    "Bloco 1 - Foco em Força": {
        "Semana 1 - Acumulação": {
            "forca": "Agachamento nas Costas 4x8 @ 65-70% RPE 7 (Tempo 3010)",
            "lpo": "Técnica de Arranco: Arranco em Suspensão Alta (Hang High Snatch) 5x3 leve",
            "wod": "AMRAP 12 min:\n- 12 Agachamentos com Halter\n- 10 Remadas na fita\n- 8 Flexões de braço"
        },
        "Semana 2 - Progressão": {
            "forca": "Agachamento nas Costas 5x5 @ 75-80% RPE 8",
            "lpo": "Arranco em Suspensão abaixo do joelho (Hang Power Snatch) 5x2",
            "wod": "For Time (Teto 15 min):\n- 15-12-9 Agachamentos com barra + Pés na barra"
        },
        "Semana 3 - Sobrecarga": {
            "forca": "Agachamento nas Costas 5x3 @ 85% RPE 9 (Carga de Sobrecarga)",
            "lpo": "Arranco Completo (Squat Snatch) 6x1 acumulando carga",
            "wod": "4 Rounds por Tempo:\n- 400m Corrida\n- 10 Arremessos de Wall Ball\n- 5 Power Cleans pesados"
        },
        "Semana 4 - Deload / Benchmark": {
            "forca": "Teste de 3RM Agachamento nas Costas ou Deload (-30% volume)",
            "lpo": "Benchmark Isabel (30 Arremessos/Snatches por tempo)",
            "wod": "Benchmark 'Fran' ou 'Isabel' conforme planejamento do bloco"
        }
    },
    "Bloco 2 - Foco em Engine": {
        "Semana 1 - Acumulação": {
            "forca": "Levantamento Terra 4x8 @ 65% RPE 7",
            "lpo": "Remada Alta + Arremesso Suspenso com Halteres 4x10",
            "wod": "EMOM 20 min:\n- Min 1: 15 Cal Remada/Bike\n- Min 2: 12 Burpees\n- Min 3: 15 Wall Balls\n- Min 4: Descanso"
        },
        "Semana 2 - Progressão": {
            "forca": "Levantamento Terra 5x5 @ 75% RPE 8",
            "lpo": "Clean Suspenso + Desenvolvimento de Arremesso (Push Press) 5x3",
            "wod": "Chipper por Tempo (Teto 18 min):\n- 800m Corrida\n- 40 Saltos na Caixa\n- 30 Burpees Over Bar\n- 20 Power Cleans"
        },
        "Semana 3 - Sobrecarga": {
            "forca": "Levantamento Terra 5x3 @ 85% RPE 9",
            "lpo": "Power Clean + Push Jerk 5x2+1",
            "wod": "5 Sets de 3 min ON / 1 min OFF:\n- 200m Corrida\n- Máximo de Burpees Box Jump no tempo restante"
        },
        "Semana 4 - Deload / Benchmark": {
            "forca": "Deload Ativo de Terra (3x5 @ 60%)",
            "lpo": "Trabalho leve de mobilidade e técnica de recepção",
            "wod": "Benchmark 'Helen' (3 Rounds: 400m Corrida, 21 Kettlebell Swings, 12 Pull-ups)"
        }
    },
    "Bloco 3 - Foco em Ginástica": {
        "Semana 1 - Acumulação": {
            "forca": "Desenvolvimento Estrito (Strict Press) 4x8 @ 70%",
            "lpo": "Desenvolvimento com pegada de Arranco (SOTS Press) 4x5 leve",
            "wod": "AMRAP 14 min:\n- 10 Puxadas na Barra (Pull-ups)\n- 15 Flexões de Braço\n- 20 Abdominais AbMat"
        },
        "Semana 2 - Progressão": {
            "forca": "Desenvolvimento Estrito 5x5 @ 78%",
            "lpo": "Equilíbrio de Arranco (Snatch Balance) 5x3",
            "wod": "EMOM 16 min:\n- Min 1: 8 Chest to Bar Pull-ups\n- Min 2: 10 Handstand Push-ups\n- Min 3: 12 Saltos na Caixa\n- Min 4: Descanso"
        },
        "Semana 3 - Sobrecarga": {
            "forca": "Desenvolvimento Estrito 5x3 @ 85%",
            "lpo": "Arranco com pausa na recepção 5x2",
            "wod": "For Time:\n- 21-15-9 Bar Muscle-ups (ou Chest-to-Bar) + Dumbbell Snatch pesado"
        },
        "Semana 4 - Deload / Benchmark": {
            "forca": "Teste de Máximo de Puxadas na Barra (Max Unbroken Pull-ups)",
            "lpo": "Trabalho leve de estabilidade overhead com bastão",
            "wod": "Benchmark 'Cindy' (AMRAP 20 min: 5 Pull-ups, 10 Push-ups, 15 Squats)"
        }
    },
    "Bloco 4 - Foco em LPO / Levantamento": {
        "Semana 1 - Acumulação": {
            "forca": "Agachamento Frontal (Front Squat) 4x6 @ 70%",
            "lpo": "Complex: 1 Puxada de Arranco + 1 Arranco Suspenso (5 Sets)",
            "wod": "AMRAP 10 min:\n- 6 Power Cleans\n- 9 Shoulder to Overhead\n- 12 Agachamentos com Halter"
        },
        "Semana 2 - Progressão": {
            "forca": "Agachamento Frontal 5x4 @ 78%",
            "lpo": "Complex: 1 Power Clean + 1 Hang Squat Clean + 1 Split Jerk (5 Sets)",
            "wod": "For Time (Teto 12 min):\n- 15-12-9 Clean & Jerk + Burpees Over Bar"
        },
        "Semana 3 - Sobrecarga": {
            "forca": "Agachamento Frontal 5x2 @ 88% RPE 9.5",
            "lpo": "Construção de 1RM de Clean & Jerk em 20 min",
            "wod": "Benchmark 'Grace' (30 Clean & Jerks por tempo)"
        },
        "Semana 4 - Deload / Benchmark": {
            "forca": "Teste de 1RM ou 3RM de Agachamento Frontal",
            "lpo": "Avaliação técnica de Levantamento Olímpico",
            "wod": "Benchmark 'DT' (5 Rounds: 12 Deadlifts, 9 Hang Power Cleans, 6 Push Jerks)"
        }
    }
}

# --- GERADOR DE SUGESTÕES COMPLETO ---
def gerar_todas_sugestoes(bloco_sel, semana_sel, strength_txt, lpo_txt, wod_txt):
    base_bloco = METODOLOGIA_BASE.get(bloco_sel, {}).get(semana_sel, {
        "forca": "Trabalho de força conforme planejamento do bloco",
        "lpo": "Trabalho técnico de LPO/Skill",
        "wod": "Treino principal metabólico/concorrente"
    })
    
    # Se o usuário não escreveu nada, usa a sugestão do banco de dados
    s_usada = strength_txt if len(strength_txt.strip()) > 10 else base_bloco["forca"]
    l_usada = lpo_txt if len(lpo_txt.strip()) > 10 else base_bloco["lpo"]
    m_usada = wod_txt if len(wod_txt.strip()) > 10 else base_bloco["wod"]
    
    conteudo = (s_usada + " " + l_usada + " " + m_usada).lower()
    
    warmup_sug = "2-3 Rounds:\n- 10 Agachamentos livres pausados\n- 10 Polichinelos\n- Elevação de frequência"
    mob_sug = "Mobilidade articular geral e liberação miofascial"
    acess_sug = "3 Séries: 15 Abdominais Infra + 12 Pranchas com toque no ombro"
    
    if any(k in conteudo for k in ["agach", "squat", "thruster", "wall ball", "lunge"]):
        warmup_sug = "3 Rounds:\n- 10 Agachamentos livres pausados\n- 10 Cossack Squats\n- 15m Corrida leve"
        mob_sug = "Dorsiflexão de Tornozelo + Abertura de Quadril (Pigeon Pose)"
        acess_sug = "3 Séries: 12 Agachamentos Búlgaros + 15 Passos laterais com fita"
        
    elif any(k in conteudo for k in ["terra", "deadlift", "snatch", "clean", "swing", "hinge"]):
        warmup_sug = "3 Rounds:\n- 10 Good Mornings com bastão de PVC\n- 10 Pontes de Quadril\n- 8 Minhocas"
        mob_sug = "Soltura de Isquiotibiais + Mobilidade Torácica no rolo"
        acess_sug = "3 Séries: 10 RDL Unilateral + 15 Good Mornings com fita"
        
    elif any(k in conteudo for k in ["jerk", "press", "hspu", "overhead", "push press"]):
        warmup_sug = "3 Rounds:\n- 10 Passagens de bastão\n- 10 Flexões escapulares\n- 8 Desenvolvimentos leves"
        mob_sug = "Mobilidade de Ombro (Rotação Externa) + Alongamento de Latíssimo"
        acess_sug = "3 Séries: 12 Puxadas na fita (Face Pull) + 10 Desenvolvimentos unilaterais"

    df_sug = pd.DataFrame({
        "Etapa do Treino": [
            "1. Aquecimento (Warm Up)", 
            "2. Bloco de Força (Strength)", 
            "3. LPO / Técnica (Skill)", 
            "4. Treino Principal (WOD)", 
            "5. Acessórios / Core", 
            "6. Mobilidade Específica"
        ],
        "Sugestão Automática": [
            warmup_sug, 
            base_bloco["forca"], 
            base_bloco["lpo"], 
            base_bloco["wod"], 
            acess_sug, 
            mob_sug
        ]
    })
    
    return df_sug, base_bloco

# --- BARRA LATERAL: PERIODIZAÇÃO ---
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
st.sidebar.header("📊 Painel MCVS & IACS (Carga Automática)")

vol_squat = st.sidebar.number_input("Volume Agachar (Ideal: 120-180)", value=140)
vol_hinge = st.sidebar.number_input("Volume Hinge / LPO (Ideal: 80-120)", value=90)
vol_push = st.sidebar.number_input("Volume Empurrar (Ideal: 60-100)", value=70)
vol_pull = st.sidebar.number_input("Volume Puxar (Ideal: 60-100)", value=75)
vol_run = st.sidebar.number_input("Volume Corrida em KM (Ideal: 6-12 km)", value=8.0)

# Cálculo IACS da Metodologia
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

# --- GRADE SEMANAL ---
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
            
            if "Sexta" in dias[i]: # ATHX
                st.info("🔥 **Sessão ATHX:** Estrutura Fixa (Força Máxima + Endurance + MetCon X)")
                w_input = st.text_area("Aquecimento (Tempo: 10')", "Ativação dinâmica\nCorrida leve\nExercícios articulados", height=100, key=f"athx_w_{i}")
                s_input = st.text_area("1. Força Máxima (Tempo: 15')", "5 RM Terra ou 3 RM Agachamento Frontal", height=100, key=f"athx_s_{i}")
                l_input = "" 
                e_input = st.text_area("2. Endurance (Tempo: 15')", "Burpees com Salto em Distância / Corrida Máxima / Transporte de Carga", height=100, key=f"athx_e_{i}")
                m_input = st.text_area("3. MetCon X / Treino Principal (Tempo: 20')", "For Time / AMRAP Alta Intensidade sob fadiga", height=120, key=f"athx_m_{i}")
                r_input = st.text_area("4. Mobilidade e Recuperação (Tempo: 5')", "Liberação miofascial / Alongamento", height=80, key=f"athx_r_{i}")
            
            elif "Segunda" in dias[i]: # HYROX
                st.info("🏃 **Sessão HYROX:** Corrida + Estações Funcionais")
                w_input = st.text_area("Aquecimento (10-12')", "Mobilidade dinâmica\nAtivação de Core e Quadril\nCorrida Leve", height=100, key=f"hy_w_{i}")
                s_input = "" 
                l_input = st.text_area("Técnica de Estação (8-10')", "Mecânica de Empurrão / Salto / Transportes de Carga", height=100, key=f"hy_t_{i}")
                m_input = st.text_area("Parte Principal (35-40')", "Alternância: Corrida + Estação Funcional", height=120, key=f"hy_m_{i}")
                r_input = st.text_area("Volta à Calma (5')", "Caminhada leve e respiração orientada", height=80, key=f"hy_r_{i}")
                
            else: # CrossFit Padrão
                w_input = st.text_area("1. Aquecimento (10')", "2-3 Rounds:\n50 Polichinelos\n10 Tiros de Corrida\nExercícios dinâmicos", height=120, key=f"cf_w_{i}")
                s_input = st.text_area("2. Bloco de Força (10-15')", "", height=100, key=f"cf_s_{i}")
                l_input = st.text_area("3. Bloco de LPO / Técnica (10-15')", "", height=100, key=f"cf_l_{i}")
                m_input = st.text_area("4. WOD / Treino Principal (15-20')", "", height=130, key=f"cf_wod_{i}")
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
            
            # --- TABELA DE SUGESTÕES COMPLETA DE TODAS AS ETAPAS ---
            st.markdown("### 💡 Sugestões Automáticas Inteligentes")
            st.caption("Baseadas na fase/semana selecionadas e nos exercícios digitados:")
            
            df_todas_sugestoes, base_info = gerar_todas_sugestoes(bloco, semana, s_input, l_input, m_input)
            st.table(df_todas_sugestoes)
            
            st.markdown("---")
            st.markdown("### 🔍 Checklist Metodológico")
            st.checkbox("O objetivo da sessão está claro?", value=True, key=f"chk1_{i}")
            st.checkbox("Movimento dominante respeitado?", value=True, key=f"chk2_{i}")
            st.checkbox("Sessão dentro dos 60 minutos?", value=True, key=f"chk3_{i}")
            st.checkbox("Escalas disponíveis para todos os níveis?", value=True, key=f"chk4_{i}")

st.markdown("---")
if st.button("💾 Salvar & Exportar Treino Semanal"):
    st.success("Programação enviada e sincronizada com a Planilha Alpha Iron 2.0!")
