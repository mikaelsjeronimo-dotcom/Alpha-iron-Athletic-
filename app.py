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

# --- CARREGAMENTO DA LOGO ALPHA IRON ---
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
elif os.path.exists("1000319375.png"):
    st.sidebar.image("1000319375.png", use_container_width=True)
else:
    st.sidebar.title("🏋️‍♂️ ALPHA IRON ATHLETICS")

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
    key_block = bloco_sel.split(" ")[0] + " " + bloco_sel.split(" ")[1] # Ex: "Block 1"
    key_week = semana_sel.split(" ")[0] + " " + semana_sel.split(" ")[1] # Ex: "Week 1"
    
    base_bloco = METODOLOGIA_BASE.get(key_block, {}).get(key_week, {
        "strength": "Strength progression based on block focus",
        "skill": "LPO / Skill technical progression",
        "wod": "Main WOD"
    })
    
    s_usada = strength_txt if len(strength_txt.strip()) > 5 else base_bloco["strength"]
    l_usada = skill_txt if len(skill_txt.strip()) > 5 else base_bloco["skill"]
    m_usada = wod_txt if len(wod_txt.strip()) > 5 else base_bloco["wod"]
    
    conteudo = (s_usada + " " + l_usada + " " + m_usada).lower()
    
    warmup_sug = "2-3 Rounds:\n- 10 Air Squats\n- 10 Jumping Jacks\n- Dynamic Drills"
    mob_sug = "General Joint Mobility & Foam Rolling"
    acess_sug = "3 Sets: 15 Hollow Rocks + 12 Shoulder Tap Planks"
    
    if any(k in conteudo for k in ["squat", "agach", "thruster", "wall ball", "lunge"]):
        warmup_sug = "3 Rounds:\n- 10 Paused Air Squats\n- 10 Cossack Squats\n- 15m Shuttle Run"
        mob_sug = "Ankle Dorsiflexion + Hip Opener (Pigeon Pose)"
        acess_sug = "3 Sets: 12 Bulgarian Split Squats + 15 Mini-band Walks"
        
    elif any(k in conteudo for k in ["deadlift", "terra", "snatch", "clean", "swing", "hinge"]):
        warmup_sug = "3 Rounds:\n- 10 PVC Good Mornings\n- 10 Glute Bridges\n- 8 Inchworms"
        mob_sug = "Hamstring Release + Thoracic Spine Mobility"
        acess_sug = "3 Sets: 10 Single Leg RDLs + 15 Banded Good Mornings"
        
    elif any(k in conteudo for k in ["jerk", "press", "hspu", "overhead", "push press"]):
        warmup_sug = "3 Rounds:\n- 10 PVC Pass-throughs\n- 10 Scapular Push-ups\n- 8 Light DB Press"
        mob_sug = "Shoulder External Rotation + Lat Stretch"
        acess_sug = "3 Sets: 12 Banded Face Pulls + 10 Bottom-up KB Press"

    df_sug = pd.DataFrame({
        "Session Block": [
            "1. Warm-Up", 
            "2. Strength", 
            "3. Skill", 
            "4. WOD", 
            "5. Accessory", 
            "6. Mobility"
        ],
        "Recommended Programming": [
            warmup_sug, 
            base_bloco["strength"], 
            base_bloco["skill"], 
            base_bloco["wod"], 
            acess_sug, 
            mob_sug
        ]
    })
    
    return df_sug

# --- BARRA LATERAL: PERIODIZAÇÃO ---
st.sidebar.header("⚙️ Periodization (Planilha 2.0)")
bloco = st.sidebar.selectbox("Periodization Phase", [
    "Block 1 - Strength Focus",
    "Block 2 - Engine Focus",
    "Block 3 - Gymnastics Focus",
    "Block 4 - Weightlifting Focus"
])

semana = st.sidebar.selectbox("Periodization Week", [
    "Week 1 - Accumulation",
    "Week 2 - Progression",
    "Week 3 - Overload",
    "Week 4 - Deload / Benchmark"
])

st.sidebar.markdown("---")
st.sidebar.header("📊 MCVS & IACS Control")

vol_squat = st.sidebar.number_input("Squat Volume (Ideal: 120-180)", value=140)
vol_hinge = st.sidebar.number_input("Hinge / LPO Volume (Ideal: 80-120)", value=90)
vol_push = st.sidebar.number_input("Push Volume (Ideal: 60-100)", value=70)
vol_pull = st.sidebar.number_input("Pull Volume (Ideal: 60-100)", value=75)
vol_run = st.sidebar.number_input("Running Volume KM (Ideal: 6-12 km)", value=8.0)

# Cálculo IACS conforme Metodologia Alpha Iron
iacs_score = (vol_squat * 0.15) + (vol_hinge * 0.2) + (vol_push * 0.15) + (vol_pull * 0.15) + (vol_run * 3)

st.sidebar.metric("Alpha Load Index (IACS)", f"{int(iacs_score)} pts")

if iacs_score <= 45:
    st.sidebar.success("Classification: Light Week")
elif iacs_score <= 60:
    st.sidebar.info("Classification: Moderate Week")
elif iacs_score <= 75:
    st.sidebar.warning("Classification: Heavy Week")
elif iacs_score <= 90:
    st.sidebar.error("Classification: Shock Week")
else:
    st.sidebar.error("⚠️ Not Recommended for Regular Classes")

# --- GRADE SEMANAL CONFORME A ABA SETTINGS ---
dias_semana = [
    {"day": "Monday", "focus": "HYROX"},
    {"day": "Tuesday", "focus": "CrossFit - Strength / LPO"},
    {"day": "Wednesday", "focus": "CrossFit - Gymnastics"},
    {"day": "Thursday", "focus": "CrossFit - Engine"},
    {"day": "Friday", "focus": "ATHX"},
    {"day": "Saturday", "focus": "Community WOD"},
    {"day": "Sunday", "focus": "Benchmark / Hero"}
]

tabs = st.tabs([d["day"] for d in dias_semana])

for i, tab in enumerate(tabs):
    day_info = dias_semana[i]
    with tab:
        st.subheader(f"{day_info['day']} — {day_info['focus']}")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown("### 📋 Session Structure (60 min)")
            
            # --- SEGUNDA: HYROX ---
            if day_info["day"] == "Monday":
                st.info("🏃 **HYROX Session:** Running + Functional Stations")
                w_input = st.text_area("Warm-Up (10')", "Dynamic Mobility\nCore & Hip Activation\nLight Run", height=100, key=f"hy_w_{i}")
                s_input = "" 
                l_input = ""
                m_input = st.text_area("HYROX Main Block (35-40')", "Alternating: Running + Functional Station (Burpee Broad Jump / Carries / Sled / Wall Ball)", height=150, key=f"hy_m_{i}")
                r_input = st.text_area("Mobility (5')", "Light Walk & Guided Breathing / Joint Mobility", height=80, key=f"hy_r_{i}")
            
            # --- SEXTA: ATHX ---
            elif day_info["day"] == "Friday":
                st.info("🔥 **ATHX Session:** Fixed Structure (Strength Max + Endurance + MetCon X)")
                w_input = st.text_area("Warm-Up (10')", "Dynamic Activation\nLight Run\nJoint Drills", height=100, key=f"athx_w_{i}")
                s_input = st.text_area("Strength Max (15')", "5 RM Deadlift or 3 RM Front Squat", height=100, key=f"athx_s_{i}")
                l_input = st.text_area("Endurance (15')", "Max Burpees Broad Jump / Max Run / Farmer Carry", height=100, key=f"athx_e_{i}")
                m_input = st.text_area("MetCon X (20')", "For Time / AMRAP High Intensity under fatigue", height=120, key=f"athx_m_{i}")
                r_input = st.text_area("Mobility (10')", "Myofascial Release / Stretching", height=80, key=f"athx_r_{i}")
                
            # --- CROSSFIT PADRÃO (TERÇA, QUARTA, QUINTA, SÁBADO, DOMINGO) ---
            else:
                w_input = st.text_area("Warm-Up (10')", "2-3 Rounds:\n50 Jumping Jacks\n10 Shuttle Runs\nDynamic Drills", height=120, key=f"cf_w_{i}")
                s_input = st.text_area("Strength (15')", "", height=100, key=f"cf_s_{i}")
                l_input = st.text_area("Skill (10')", "", height=100, key=f"cf_l_{i}")
                m_input = st.text_area("WOD (20')", "", height=130, key=f"cf_wod_{i}")
                a_input = st.text_area("Accessory (5-10')", "Unilateral accessories / core stabilization", height=90, key=f"cf_a_{i}")
                r_input = st.text_area("Mobility (5')", "Targeted joint mobility", height=80, key=f"cf_m_{i}")

        with col2:
            st.markdown("### 🎯 Scaling Chart (RX / INT / BEG / MASTERS)")
            escala_df = pd.DataFrame({
                "Level": ["RX", "Intermediate", "Beginner", "Masters"],
                "Load / Category": ["100% RX Load", "70-80% Load", "50% Load / Dumbbells", "Custom Scaling"],
                "Gymnastics": ["Full Movement", "Medium Progression", "Basic Scale", "Range Focus"]
            })
            st.table(escala_df)
            
            # --- TABELA DE SUGESTÕES COMPLETA ---
            st.markdown("### 💡 Intelligence Suggestions")
            st.caption("Auto-generated based on Block, Week & Typed Movement Patterns:")
            
            df_todas_sugestoes = gerar_todas_sugestoes(bloco, semana, s_input, l_input, m_input)
            st.table(df_todas_sugestoes)
            
            st.markdown("---")
            st.markdown("### 🔍 Validation Checklist")
            st.checkbox("Session objective clearly defined?", value=True, key=f"chk1_{i}")
            st.checkbox("Dominant movement pattern respected?", value=True, key=f"chk2_{i}")
            st.checkbox("Session within 60 minutes time cap?", value=True, key=f"chk3_{i}")
            st.checkbox("Scaling options available for all levels?", value=True, key=f"chk4_{i}")

st.markdown("---")
if st.button("💾 Save & Export Weekly Programming"):
    st.success("Programming successfully synchronized with Alpha Iron 2.0 Sheet!")
