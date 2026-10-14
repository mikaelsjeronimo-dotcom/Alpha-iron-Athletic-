import streamlit as st
import pandas as pd
import os
import glob
import base64

# 1. Configuração Visual da Página
st.set_page_config(page_title="Alpha Iron 2.0 - Workout Builder", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- CARREGAMENTO DIRETO DA LOGO DA SUA PASTA ---
def carregar_logo():
    # Lista de possíveis nomes da logo na pasta raiz
    nomes_possiveis = [
        "Logo_e_mascote[1].png", 
        "Logo_e_mascote.png", 
        "logo.png", 
        "Logo.png"
    ]
    
    logo_file = None
    for nome in nomes_possiveis:
        if os.path.exists(nome):
            logo_file = nome
            break
            
    # Se não achar pelos nomes exatos, busca qualquer imagem com 'logo' ou 'mascote'
    if not logo_file:
        arquivos = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
        for f in arquivos:
            if "logo" in f.lower() or "mascote" in f.lower():
                logo_file = f
                break

    if logo_file and os.path.exists(logo_file):
        try:
            with open(logo_file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            
            st.sidebar.markdown(
                f"""
                <div style="text-align: center; padding-bottom: 15px;">
                    <img src="data:image/png;base64,{encoded_string}" style="max-width: 100%; height: auto; border-radius: 8px;">
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception:
            st.sidebar.title("🏋️‍♂️ ALPHA IRON ATHLETICS")
    else:
        st.sidebar.title("🏋️‍♂️ ALPHA IRON ATHLETICS")

# Executa o carregamento da logo na barra lateral
carregar_logo()

st.title("🏋️‍♂️ Alpha Iron Athletics 2.0 — Workout Builder")

# --- BANCO DE DADOS OFICIAL DA PLANILHA (BLOCKS & WEEKS) ---
METODOLOGIA_BASE = {
    "Block 1": {
        "Week 1": {
            "strength": "Back Squat 4x8 @ 65-70% RPE 7 (Tempo 3010)",
            "skill": "Hang High Snatch 5x3 (Light Load)",
            "wod": "AMRAP 12 min:\n- 12 DB Goblet Squats\n- 10 Ring Rows\n- 8 Push-ups"
        },
        "Week 2": {
            "strength": "Back Squat 5x5 @ 75-80% RPE 8",
            "skill": "Hang Power Snatch 5x2",
            "wod": "For Time (Cap 15 min):\n- 15-12-9 Barbell Squats + Toes to Bar"
        },
        "Week 3": {
            "strength": "Back Squat 5x3 @ 85% RPE 9",
            "skill": "Squat Snatch 6x1 (Heavy Build)",
            "wod": "4 Rounds For Time:\n- 400m Run\n- 10 Wall Balls\n- 5 Heavy Power Cleans"
        },
        "Week 4": {
            "strength": "3RM Back Squat Test or Deload (-30% Volume)",
            "skill": "Benchmark Isabel (30 Snatches for time)",
            "wod": "Benchmark 'Fran' or 'Isabel'"
        }
    },
    "Block 2": {
        "Week 1": {
            "strength": "Deadlift 4x8 @ 65% RPE 7",
            "skill": "DB High Pull + DB Push Press 4x10",
            "wod": "EMOM 20 min:\n- Min 1: 15 Cal Row/Bike\n- Min 2: 12 Burpees\n- Min 3: 15 Wall Balls\n- Min 4: Rest"
        },
        "Week 2": {
            "strength": "Deadlift 5x5 @ 75% RPE 8",
            "skill": "Hang Clean + Push Press 5x3",
            "wod": "Chipper For Time (Cap 18 min):\n- 800m Run\n- 40 Box Jumps\n- 30 Burpees Over Bar\n- 20 Power Cleans"
        },
        "Week 3": {
            "strength": "Deadlift 5x3 @ 85% RPE 9",
            "skill": "Power Clean + Push Jerk 5x2+1",
            "wod": "5 Sets of 3 min ON / 1 min OFF:\n- 200m Run\n- Max Burpee Box Jump Overs"
        },
        "Week 4": {
            "strength": "Active Deload Deadlift (3x5 @ 60%)",
            "skill": "Light Mobility & Catch Technique",
            "wod": "Benchmark 'Helen' (3 Rounds: 400m Run, 21 KB Swings, 12 Pull-ups)"
        }
    },
    "Block 3": {
        "Week 1": {
            "strength": "Strict Press 4x8 @ 70%",
            "skill": "SOTS Press (PVC / Light Barbell) 4x5",
            "wod": "AMRAP 14 min:\n- 10 Pull-ups\n- 15 Push-ups\n- 20 AbMat Sit-ups"
        },
        "Week 2": {
            "strength": "Strict Press 5x5 @ 78%",
            "skill": "Snatch Balance 5x3",
            "wod": "EMOM 16 min:\n- Min 1: 8 Chest to Bar Pull-ups\n- Min 2: 10 HSPU\n- Min 3: 12 Box Jumps\n- Min 4: Rest"
        },
        "Week 3": {
            "strength": "Strict Press 5x3 @ 85%",
            "skill": "Squat Snatch w/ Pause in Catch 5x2",
            "wod": "For Time:\n- 21-15-9 Bar Muscle-ups + Heavy DB Snatches"
        },
        "Week 4": {
            "strength": "Max Unbroken Pull-ups Test",
            "skill": "Overhead Stability & Mobility",
            "wod": "Benchmark 'Cindy' (AMRAP 20 min: 5 Pull-ups, 10 Push-ups, 15 Squats)"
        }
    },
    "Block 4": {
        "Week 1": {
            "strength": "Front Squat 4x6 @ 70%",
            "skill": "Complex: 1 Snatch Pull + 1 Hang Snatch (5 Sets)",
            "wod": "AMRAP 10 min:\n- 6 Power Cleans\n- 9 Shoulder to Overhead\n- 12 Goblet Squats"
        },
        "Week 2": {
            "strength": "Front Squat 5x4 @ 78%",
            "skill": "Complex: 1 Power Clean + 1 Hang Squat Clean + 1 Split Jerk (5 Sets)",
            "wod": "For Time (Cap 12 min):\n- 15-12-9 Clean & Jerks + Burpees Over Bar"
        },
        "Week 3": {
            "strength": "Front Squat 5x2 @ 88% RPE 9.5",
            "skill": "Build to Heavy Clean & Jerk Single (20 min)",
            "wod": "Benchmark 'Grace' (30 Clean & Jerks for time)"
        },
        "Week 4": {
            "strength": "1RM or 3RM Front Squat Test",
            "skill": "Weightlifting Technical Assessment",
            "wod": "Benchmark 'DT' (5 Rounds: 12 Deadlifts, 9 Hang Power Cleans, 6 Push Jerks)"
        }
    }
}

# --- GERADOR DE SUGESTÕES AUTOMÁTICAS ---
def gerar_todas_sugestoes(bloco_sel, semana_sel, strength_txt, skill_txt, wod_txt):
    key_block = bloco_sel.split(" ")[0] + " " + bloco_sel.split(" ")[1]
    key_week = semana_sel.split(" ")[0] + " " + semana_sel.split(" ")[1]
    
    base_bloco = METODOLOGIA_BASE.get(key_block, {}).get(key_week, {
        "strength": "Strength progression based on block focus",
        "skill": "LPO / Skill technical progression",
        "wod": "Main WOD"
    })
    
    s_usada = strength_txt if len(strength_txt.strip()) > 5 else base_bloco["strength"]
    l_usada = skill_txt if len(skill_txt.strip()) > 5 else base_bloco["skill"]
    m_usada = wod_txt if len(wod_txt.strip()) > 5 else base_bloco["wod"]
    
    conteudo = (s_usada + " " + l_usada + " " + m_usada).lower()
    
    warmup_sug = "2-3 Rounds:\n- 10 Air Squats\n-
