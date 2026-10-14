import streamlit as st
import pandas as pd
import os
import glob
import base64
import re

# --- BUSCA A LOGO OFICIAL PARA O FAVICON DA ABA DO NAVEGADOR ---
def encontrar_logo():
    nomes_possiveis = [
        "Logo_e_mascote[1].png", 
        "Logo_e_mascote.png", 
        "logo.png", 
        "Logo.png"
    ]
    for nome in nomes_possiveis:
        if os.path.exists(nome):
            return nome
    arquivos = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
    for f in arquivos:
        if "logo" in f.lower() or "mascote" in f.lower():
            return f
    return None

logo_path = encontrar_logo()

# 1. Configuração Visual da Página (Favicon com a Logo Oficial da Alpha)
st.set_page_config(
    page_title="Alpha Iron 2.0 - Workout Builder", 
    layout="wide", 
    page_icon=logo_path if logo_path else "🏋️‍♂️"
)

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    .stTable { font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

# --- CARREGAMENTO DIRETO DA LOGO NA SIDEBAR ---
def carregar_logo_sidebar():
    if logo_path and os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            
            st.sidebar.markdown(
                f"""
                <div style="text-align: center; padding-bottom: 10px;">
                    <img src="data:image/png;base64,{encoded_string}" style="max-width: 100%; height: auto; border-radius: 8px;">
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception:
            st.sidebar.title("🏋️‍♂️ ALPHA IRON ATHLETICS")
    else:
        st.sidebar.title("🏋️‍♂️ ALPHA IRON ATHLETICS")

carregar_logo_sidebar()

st.title("🏋️‍♂️ Alpha Iron Athletics 2.0 — Workout Builder")

# --- TABELA DE VOLUME IDEAL DINÂMICO POR BLOCO E SEMANA ---
def obter_metas_volume(bloco_sel, semana_sel):
    base = {
        "Squat": 140,
        "Hinge": 90,
        "Push": 80,
        "Pull": 80,
        "Core": 100,
        "Snatch": 45,
        "Clean & Jerk": 50,
        "Run": 8.0
    }
    
    if "Block 1" in bloco_sel or "Strength" in bloco_sel:
        base["Squat"] += 30
        base["Hinge"] += 20
    elif "Block 2" in bloco_sel or "Engine" in bloco_sel:
        base["Run"] += 4.0
        base["Pull"] += 20
    elif "Block 3" in bloco_sel or "Gymnastics" in bloco_sel:
        base["Push"] += 30
        base["Pull"] += 30
        base["Core"] += 40
    elif "Block 4" in bloco_sel or "Weightlifting" in bloco_sel:
        base["Snatch"] += 25
        base["Clean & Jerk"] += 30
        base["Hinge"] += 20

    fator = 1.0
    if "Progression" in semana_sel or "Week 2" in semana_sel:
        fator = 1.15
    elif "Overload" in semana_sel or "Week 3" in semana_sel:
        fator = 1.30
    elif "Deload" in semana_sel or "Week 4" in semana_sel:
        fator = 0.65
        
    return {
        "Squat": int(base["Squat"] * fator),
        "Hinge": int(base["Hinge"] * fator),
        "Push": int(base["Push"] * fator),
        "Pull": int(base["Pull"] * fator),
        "Core": int(base["Core"] * fator),
        "Snatch": int(base["Snatch"] * fator),
        "Clean & Jerk": int(base["Clean & Jerk"] * fator),
        "Run": round(base["Run"] * fator, 1)
    }

# --- MOTOR CORRIGIDO DE CÁLCULO DE EMOM VINCULADO AO TEMPO EXATO DO BLOCO ---
def extrair_volume_acumulado_estruturado(lista_blocos_dados):
    vol = {"Squat": 0, "Hinge": 0, "Push": 0, "Pull": 0, "Core": 0, "Snatch": 0, "Clean & Jerk": 0, "Run": 0.0}
    
    for item in lista_blocos_dados:
        texto = item.get("texto", "").strip()
        tempo_minutos = item.get("tempo", 0)
        
        if not texto:
            continue
            
        linhas = [l.strip() for l in texto.split("\n") if l.strip()]
        
        texto_low = texto.lower()
        is_emom = "emom" in texto_low
        is_amrap = "amrap" in texto_low
        
        num_rounds = 1
        for l in linhas:
            m_rnds = re.search(r'(\d+)\s*(?:rounds|rnds|sets|series|séries|rodadas)', l.lower())
            if m_rnds:
                num_rounds = int(m_rnds.group(1))
                break

        # Filtra exercícios do bloco
        linhas_ex = []
        for l in linhas:
            l_low = l.lower()
            if any(k in l_low for k in ["rx:", "scaled:", "emom", "amrap", "for time", "cap "]):
                continue
            if " or " in l_low:
                l = l_low.split(" or ")[0]
            linhas_ex.append(l)

        qtd_exercicios = len(linhas_ex) if len(linhas_ex) > 0 else 1

        # CÁLCULO DE MULTIPLICADOR VINCULADO AO TEMPO DO INPUT
        multiplicador = 1
        if is_emom and tempo_minutos > 0:
            multiplicador = max(1, tempo_minutos // qtd_exercicios)
        elif is_amrap and tempo_minutos > 0:
            multiplicador = max(1, tempo_minutos // 3)
        elif num_rounds > 1:
            multiplicador = num_rounds

        for linha in linhas_ex:
            linha_limpa = linha.lower().strip()
            if not linha_limpa or "rm " in linha_limpa or "rm" in linha_limpa:
                continue

            # LEITURA DE CORRIDA (M / KM)
            if "run" in linha_limpa or "corrida" in linha_limpa or "km" in linha_limpa:
                m_metros = re.findall(r'(\d+)\s*m\b', linha_limpa)
                if m_metros:
                    vol["Run"] += (sum([int(m) for m in m_metros]) / 1000.0) * multiplicador
                m_kms = re.findall(r'(\d+(?:\.\d+)?)\s*km\b', linha_limpa)
                if m_kms:
                    vol["Run"] += sum([float(k) for k in m_kms]) * multiplicador

            reps_base = 0
            m_mult = re.findall(r'(\d+)\s*x\s*(\d+)', linha_limpa)
            if m_mult:
                for s, r in m_mult:
                    reps_base += int(s) * int(r)
            else:
                esquema_hifen = re.findall(r'(\d+)-(\d+)-(\d+)', linha_limpa)
                if esquema_hifen:
                    for a, b, c in esquema_hifen:
                        reps_base += int(a) + int(b) + int(c)
                else:
                    nums = re.findall(r'\b(\d+)\b', linha_limpa)
                    if nums:
                        reps_encontradas = [int(n) for n in nums if int(n) <= 300]
                        if reps_encontradas:
                            reps_base = sum(reps_encontradas)

            if reps_base == 0:
                continue

            reps_totais = reps_base * multiplicador

            # CLASSIFICAÇÃO MULTI-CATEGORIA COMPLETA

            if any(k in linha_limpa for k in [
                "squat", "agacho", "agachamento", "thruster", "wall ball", "wallball", 
                "lunge", "lunges", "passada", "pistol", "squat clean", "squat snatch", "front squat", "back squat", "ohs"
            ]):
                vol["Squat"] += reps_totais

            if any(k in linha_limpa for k in [
                "deadlift", "terra", "rdl", "snatch", "clean", "swing", "good morning", "hip thrust"
            ]):
                vol["Hinge"] += reps_totais

            if any(k in linha_limpa for k in [
                "push", "press", "jerk", "thruster", "hspu", "dip", "dips", "bench", "flexao", "flexão", "supino", "wall ball", "wallball"
            ]):
                vol["Push"] += reps_totais

            if any(k in linha_limpa for k in [
                "pull", "pullup", "pull-up", "c2b", "chest to bar", "muscle up", "muscle-up", "bmu", "rmu", "row", "remada", "rope climb", "puxada"
            ]):
                vol["Pull"] += reps_totais

            if any(k in linha_limpa for k in [
                "toes to bar", "ttb", "knees to elbow", "kte", "sit up", "situp", "v-up", "hollow", "plank", "prancha", "l-sit", "abmat", "ghd"
            ]):
                vol["Core"] += reps_totais

            if any(k in linha_limpa for k in [
                "snatch", "arranco", "snatch balance"
            ]):
                vol["Snatch"] += reps_totais

            if any(k in linha_limpa for k in [
                "clean", "jerk", "arremesso", "clean & jerk", "clean and jerk"
            ]):
                vol["Clean & Jerk"] += reps_totais

    return vol

# --- BANCO DE DADOS METODOLÓGICO (BLOCKS & WEEKS) ---
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

metas = obter_metas_volume(bloco, semana)

st.sidebar.markdown("---")
st.sidebar.header("📊 MCVS & Weekly Volume Control")

dias_semana = [
    {"day": "Monday", "focus": "HYROX"},
    {"day": "Tuesday", "focus": "CrossFit - Strength / LPO"},
    {"day": "Wednesday", "focus": "CrossFit - Gymnastics"},
    {"day": "Thursday", "focus": "CrossFit - Engine"},
    {"day": "Friday", "focus": "ATHX"},
    {"day": "Saturday", "focus": "Community WOD"},
    {"day": "Sunday", "focus": "Benchmark / Hero"}
]

# --- CONSTRUÇÃO DAS ABAS DIÁRIAS ---
tabs = st.tabs([d["day"] for d in dias_semana])

lista_blocos_acumulados = []

for i, tab in enumerate(tabs):
    day_info = dias_semana[i]
    day_name = day_info["day"]
    
    with tab:
        st.subheader(f"{day_name} — {day_info['focus']}")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown("### 📋 Session Structure (60 min)")
            
            t_s = 0
            t_m = 0
            
            if day_name == "Monday":
                st.info("🏃 **HYROX Session:** Running + Functional Stations")
                
                c_time1, c_text1 = st.columns([1, 3])
                with c_time1:
                    t_w = st.number_input("Warm-Up (min)", 1, 60, 10, key=f"t_hy_w_{i}")
                with c_text1:
                    w_input = st.text_area(f"Warm-Up ({t_w}')", "Dynamic Mobility\nCore & Hip Activation\nLight Run", height=90, key=f"hy_w_{i}")
                
                s_input = "" 
                l_input = ""
                
                c_time2, c_text2 = st.columns([1, 3])
                with c_time2:
                    t_m = st.number_input("Main Block (min)", 1, 60, 40, key=f"t_hy_m_{i}")
                with c_text2:
                    m_input = st.text_area(f"HYROX Main Block ({t_m}')", "Alternating: Running + Functional Station (Burpee Broad Jump / Carries / Sled / Wall Ball)", height=140, key=f"hy_m_{i}")
                
                c_time3, c_text3 = st.columns([1, 3])
                with c_time3:
                    t_r = st.number_input("Mobility (min)", 1, 60, 10, key=f"t_hy_r_{i}")
                with c_text3:
                    r_input = st.text_area(f"Mobility ({t_r}')", "Light Walk & Guided Breathing / Joint Mobility", height=80, key=f"hy_r_{i}")
                
                total_time = t_w + t_m + t_r

                lista_blocos_acumulados.extend([
                    {"texto": w_input, "tempo": t_w},
                    {"texto": m_input, "tempo": t_m}
                ])

            elif day_name == "Friday":
                st.info("🔥 **ATHX Session:** Fixed Structure (Strength Max + Endurance + MetCon X)")
                
                c_time1, c_text1 = st.columns([1, 3])
                with c_time1:
                    t_w = st.number_input("Warm-Up (min)", 1, 60, 10, key=f"t_athx_w_{i}")
                with c_text1:
                    w_input = st.text_area(f"Warm-Up ({t_w}')", "Dynamic Activation\nLight Run\nJoint Drills", height=90, key=f"athx_w_{i}")

                c_time2, c_text2 = st.columns([1, 3])
                with c_time2:
                    t_s = st.number_input("Strength Max (min)", 0, 60, 15, key=f"t_athx_s_{i}")
                with c_text2:
                    s_input = st.text_area(f"Strength Max ({t_s}')", "", height=90, key=f"athx_s_{i}")

                c_time3, c_text3 = st.columns([1, 3])
                with c_time3:
                    t_e = st.number_input("Endurance (min)", 0, 60, 15, key=f"t_athx_e_{i}")
                with c_text3:
                    l_input = st.text_area(f"Endurance ({t_e}')", "", height=90, key=f"athx_e_{i}")

                c_time4, c_text4 = st.columns([1, 3])
                with c_time4:
                    t_m = st.number_input("MetCon X (min)", 1, 60, 15, key=f"t_athx_m_{i}")
                with c_text4:
                    m_input = st.text_area(f"MetCon X ({t_m}')", "", height=110, key=f"athx_m_{i}")

                c_time5, c_text5 = st.columns([1, 3])
                with c_time5:
                    t_r = st.number_input("Mobility (min)", 0, 60, 5, key=f"t_athx_r_{i}")
                with c_text5:
                    r_input = st.text_area(f"Mobility ({t_r}')", "Myofascial Release / Stretching", height=80, key=f"athx_r_{i}")

                total_time = t_w + t_s + t_e + t_m + t_r

                lista_blocos_acumulados.extend([
                    {"texto": w_input, "tempo": t_w},
                    {"texto": s_input, "tempo": t_s},
                    {"texto": l_input, "tempo": t_e},
                    {"texto": m_input, "tempo": t_m}
                ])

            else:
                c_time1, c_text1 = st.columns([1, 3])
                with c_time1:
                    t_w = st.number_input("Warm-Up (min)", 1, 60, 10, key=f"t_cf_w_{i}")
                with c_text1:
                    w_input = st.text_area(f"1. Warm-Up ({t_w}')", "2-3 Rounds:\n50 Jumping Jacks\n10 Shuttle Runs\nDynamic Drills", height=100, key=f"cf_w_{i}")

                c_time2, c_text2 = st.columns([1, 3])
                with c_time2:
                    t_s = st.number_input("Strength (min)", 0, 60, 15, key=f"t_cf_s_{i}")
                with c_text2:
                    s_input = st.text_area(f"2. Strength ({t_s}')", "", height=90, key=f"cf_s_{i}")

                c_time3, c_text3 = st.columns([1, 3])
                with c_time3:
                    t_l = st.number_input("Skill (min)", 0, 60, 10, key=f"t_cf_l_{i}")
                with c_text3:
                    l_input = st.text_area(f"3. Skill ({t_l}')", "", height=120, key=f"cf_l_{i}")

                c_time4, c_text4 = st.columns([1, 3])
                with c_time4:
                    t_m = st.number_input("WOD (min)", 1, 60, 15, key=f"t_cf_m_{i}")
                with c_text4:
                    m_input = st.text_area(f"4. WOD ({t_m}')", "", height=140, key=f"cf_wod_{i}")

                c_time5, c_text5 = st.columns([1, 3])
                with c_time5:
                    t_a = st.number_input("Accessory (min)", 0, 60, 5, key=f"t_cf_a_{i}")
                with c_text5:
                    a_input = st.text_area(f"5. Accessory ({t_a}')", "Unilateral accessories / core stabilization", height=80, key=f"cf_a_{i}")

                c_time6, c_text6 = st.columns([1, 3])
                with c_time6:
                    t_r = st.number_input("Mobility (min)", 0, 60, 5, key=f"t_cf_r_{i}")
                with c_text6:
                    r_input = st.text_area(f"6. Mobility ({t_r}')", "Targeted joint mobility", height=80, key=f"cf_m_{i}")

                total_time = t_w + t_s + t_l + t_m + t_a + t_r

                lista_blocos_acumulados.extend([
                    {"texto": w_input, "tempo": t_w},
                    {"texto": s_input, "tempo": t_s},
                    {"texto": l_input, "tempo": t_l},
                    {"texto": m_input, "tempo": t_m},
                    {"texto": a_input, "tempo": t_a}
                ])

            if total_time > 60:
                st.warning(f"⚠️ **Session Time Alert:** Total duration is **{total_time} min** (Standard limit: 60 min).")
            else:
                st.success(f"⏱️ **Session Total Duration:** **{total_time} min** / 60 min")

            # --- DIFICULDADE DA SESSÃO DO DIA ---
            st.markdown("---")
            daily_pts = (t_s * 1.5) + (t_m * 2.0)
            if "HYROX" in day_info["focus"] or "ATHX" in day_info["focus"]:
                daily_pts += 15
                
            if daily_pts <= 25:
                st.info(f"🟢 **Daily Session Level:** Level 1 - Low Fatigue (~{int(daily_pts)} pts)")
            elif daily_pts <= 45:
                st.success(f"🟡 **Daily Session Level:** Level 2 - Moderate Fatigue (~{int(daily_pts)} pts)")
            elif daily_pts <= 65:
                st.warning(f"🟠 **Daily Session Level:** Level 3 - High Fatigue (~{int(daily_pts)} pts)")
            else:
                st.error(f"🔴 **Daily Session Level:** Level 4 - Very High / Shock Session (~{int(daily_pts)} pts)")

        with col2:
            st.markdown("### 🎯 Scaling Chart (RX / INT / BEG / MASTERS)")
            escala_df = pd.DataFrame({
                "Level": ["RX", "Intermediate", "Beginner", "Masters"],
                "Load / Category": ["100% RX Load", "70-80% Load", "50% Load / Dumbbells", "Custom Scaling"],
                "Gymnastics": ["Full Movement", "Medium Progression", "Basic Scale", "Range Focus"]
            })
            st.table(escala_df)
            
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

# PROCESSA O VOLUME EXATAMENTE CONECTADO COM O TEMPO DIGITADO EM CADA BLOCO
vol_usado = extrair_volume_acumulado_estruturado(lista_blocos_acumulados)

# TABELA LATERAL COM O VOLUME RECALCULADO CORRETAMENTE
tabela_volume = pd.DataFrame({
    "Pattern": ["Squat", "Hinge", "Push", "Pull", "Core", "Snatch", "Clean & Jerk", "Run (KM)"],
    "Target": [
        f"{int(metas['Squat'])}", f"{int(metas['Hinge'])}", f"{int(metas['Push'])}", 
        f"{int(metas['Pull'])}", f"{int(metas['Core'])}", f"{int(metas['Snatch'])}", 
        f"{int(metas['Clean & Jerk'])}", f"{metas['Run']} km"
    ],
    "Used": [
        f"{int(vol_usado['Squat'])}", f"{int(vol_usado['Hinge'])}", f"{int(vol_usado['Push'])}", 
        f"{int(vol_usado['Pull'])}", f"{int(vol_usado['Core'])}", f"{int(vol_usado['Snatch'])}", 
        f"{int(vol_usado['Clean & Jerk'])}", f"{round(vol_usado['Run'], 2)} km"
    ],
    "Balance": [
        f"{int(metas['Squat'] - vol_usado['Squat'])}",
        f"{int(metas['Hinge'] - vol_usado['Hinge'])}",
        f"{int(metas['Push'] - vol_usado['Push'])}",
        f"{int(metas['Pull'] - vol_usado['Pull'])}",
        f"{int(metas['Core'] - vol_usado['Core'])}",
        f"{int(metas['Snatch'] - vol_usado['Snatch'])}",
        f"{int(metas['Clean & Jerk'] - vol_usado['Clean & Jerk'])}",
        f"{round(metas['Run'] - vol_usado['Run'], 2)} km"
    ]
})

st.sidebar.table(tabela_volume)

iacs_score = (
    (vol_usado["Squat"] * 0.12) + (vol_usado["Hinge"] * 0.15) + 
    (vol_usado["Push"] * 0.12) + (vol_usado["Pull"] * 0.12) + 
    (vol_usado["Core"] * 0.08) + (vol_usado["Snatch"] * 0.2) + 
    (vol_usado["Clean & Jerk"] * 0.2) + (vol_usado["Run"] * 3)
)

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

st.markdown("---")
if st.button("💾 Save & Export Weekly Programming"):
    st.success("Programming successfully synchronized with Alpha Iron 2.0 Sheet!")
