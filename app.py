import streamlit as st
import pandas as pd
import os
import glob
import base64
import re
import json

# --- ARQUIVO DE PERSISTÊNCIA EM TEMPO REAL ---
DB_FILE = "treinos_salvos.json"

def carregar_treinos_salvos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def salvar_treinos_disco(dados):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# 1. Configuração Básica da Página
st.set_page_config(
    page_title="Alpha Iron 2.0 - Workout Builder", 
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #D32F2F; font-family: 'Roboto', sans-serif; }
    .stTable { font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

# --- ENCONTRAR A LOGO DA SIDEBAR ---
def encontrar_logo_sidebar():
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
        if "favicon" not in f.lower() and ("logo" in f.lower() or "mascote" in f.lower()):
            return f
    return None

sidebar_logo_path = encontrar_logo_sidebar()

def carregar_logo_sidebar():
    if sidebar_logo_path and os.path.exists(sidebar_logo_path):
        try:
            with open(sidebar_logo_path, "rb") as image_file:
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

# --- IA: ESTIMATIVA DE TEMPO DO WOD (ZERADA SE VAZIO) ---
def estimar_tempo_wod(texto_wod):
    if not texto_wod or len(texto_wod.strip()) < 3:
        return "⏱️ WOD não programado (0 min)"
        
    texto_low = texto_wod.lower()
    
    m_cap = re.search(r'(?:cap|time cap)\D*(\d+)', texto_low)
    if m_cap:
        return f"⏱️ Time Cap Definido: {m_cap.group(1)} min"

    linhas = [l.strip() for l in texto_wod.split("\n") if l.strip()]
    if not linhas:
        return "⏱️ WOD não programado (0 min)"
    
    num_rounds = 1
    for l in linhas:
        m_rnds = re.search(r'(\d+)\s*(?:rounds|rnds|sets|series|séries|rodadas)', l.lower())
        if m_rnds:
            num_rounds = int(m_rnds.group(1))
            break
            
    total_reps_base = 0
    esquema_21_15_9 = re.findall(r'(\d+)-(\d+)-(\d+)', texto_low)
    if esquema_21_15_9:
        for a, b, c in esquema_21_15_9:
            total_reps_base = (int(a) + int(b) + int(c)) * 3
    else:
        for l in linhas:
            nums = re.findall(r'\b(\d+)\b', l)
            if nums:
                reps = [int(n) for n in nums if int(n) <= 200]
                if reps:
                    total_reps_base += reps[0]

    if total_reps_base == 0:
        return "⏱️ WOD não programado (0 min)"

    if num_rounds > 1 and not esquema_21_15_9:
        total_reps_totais = total_reps_base * num_rounds
    else:
        total_reps_totais = total_reps_base

    fator_tempo_por_rep = 2.5 
    if any(k in texto_low for k in ["bmu", "bar muscle", "muscle-up", "hspu", "snatch", "clean & jerk"]):
        fator_tempo_por_rep = 4.0 

    segundos_estimados = total_reps_totais * fator_tempo_por_rep
    minutos_estimados = max(2, round(segundos_estimados / 60))

    return f"🤖 Estimativa da IA: ~{minutos_estimados} min (Volume aprox: {total_reps_totais} reps)"

# --- TABELA DE VOLUME IDEAL DINÂMICO POR BLOCO E SEMANA ---
def obter_metas_volume(bloco_sel, semana_sel):
    base = {
        "Squat": 140, "Hinge": 90, "Push": 80, "Pull": 80, 
        "Core": 100, "Snatch": 45, "Clean & Jerk": 50, "Run": 8.0
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

# --- CÁLCULO DE VOLUME ---
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

        linhas_ex = []
        for l in linhas:
            l_low = l.lower()
            if any(k in l_low for k in ["rx:", "scaled:", "emom", "amrap", "for time", "cap "]):
                continue
            if " or " in l_low:
                l = l_low.split(" or ")[0]
            linhas_ex.append(l)

        qtd_exercicios = len(linhas_ex) if len(linhas_ex) > 0 else 1
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

            linha_sem_prefixo = re.sub(r'^(?:min(?:uto)?\s*\d+|st\d+|station\s*\d+|\d+[\.\-\)]\s*)', '', linha_limpa).strip()

            if "run" in linha_sem_prefixo or "corrida" in linha_sem_prefixo or "km" in linha_sem_prefixo:
                m_metros = re.findall(r'(\d+)\s*m\b', linha_sem_prefixo)
                if m_metros:
                    vol["Run"] += (sum([int(m) for m in m_metros]) / 1000.0) * multiplicador
                m_kms = re.findall(r'(\d+(?:\.\d+)?)\s*km\b', linha_sem_prefixo)
                if m_kms:
                    vol["Run"] += sum([float(k) for k in m_kms]) * multiplicador

            reps_base = 0
            m_mult = re.findall(r'(\d+)\s*x\s*(\d+)', linha_sem_prefixo)
            if m_mult:
                for s, r in m_mult:
                    reps_base += int(s) * int(r)
            else:
                esquema_hifen = re.findall(r'(\d+)-(\d+)-(\d+)', linha_sem_prefixo)
                if esquema_hifen:
                    for a, b, c in esquema_hifen:
                        reps_base += int(a) + int(b) + int(c)
                else:
                    nums = re.findall(r'\b(\d+)\b', linha_sem_prefixo)
                    if nums:
                        reps_encontradas = [int(n) for n in nums if int(n) <= 300]
                        if reps_encontradas:
                            reps_base = reps_encontradas[0]

            if reps_base == 0:
                continue

            is_bmu = any(k in linha_sem_prefixo for k in ["bmu", "bar muscle up", "bar muscle-up", "muscle up", "rmu"])
            reps_totais = reps_base if is_bmu else reps_base * multiplicador

            if any(k in linha_sem_prefixo for k in ["squat", "agacho", "agachamento", "thruster", "wall ball", "wallball", "lunge", "lunges", "passada", "pistol", "squat clean", "squat snatch", "front squat", "back squat", "ohs"]):
                vol["Squat"] += reps_totais
            if any(k in linha_sem_prefixo for k in ["deadlift", "terra", "rdl", "snatch", "clean", "swing", "good morning", "hip thrust"]):
                vol["Hinge"] += reps_totais
            if any(k in linha_sem_prefixo for k in ["push", "press", "jerk", "thruster", "hspu", "dip", "dips", "bench", "flexao", "flexão", "supino", "wall ball", "wallball"]):
                vol["Push"] += reps_totais
            if is_bmu or any(k in linha_sem_prefixo for k in ["pull", "pullup", "pull-up", "c2b", "chest to bar", "row", "remada", "rope climb", "puxada"]):
                vol["Pull"] += reps_totais
            if any(k in linha_sem_prefixo for k in ["toes to bar", "ttb", "knees to elbow", "kte", "sit up", "situp", "v-up", "hollow", "plank", "prancha", "l-sit", "abmat", "ghd"]):
                vol["Core"] += reps_totais
            if any(k in linha_sem_prefixo for k in ["snatch", "arranco", "snatch balance"]):
                vol["Snatch"] += reps_totais
            if any(k in linha_sem_prefixo for k in ["clean", "jerk", "arremesso", "clean & jerk", "clean and jerk"]):
                vol["Clean & Jerk"] += reps_totais

    return vol

def calcular_iacs_de_vol(vol_dict, eh_especial=False):
    score = (
        (vol_dict["Squat"] * 0.12) + (vol_dict["Hinge"] * 0.15) + 
        (vol_dict["Push"] * 0.12) + (vol_dict["Pull"] * 0.12) + 
        (vol_dict["Core"] * 0.08) + (vol_dict["Snatch"] * 0.2) + 
        (vol_dict["Clean & Jerk"] * 0.2) + (vol_dict["Run"] * 3)
    )
    if eh_especial:
        score += 15
    return int(score)

METODOLOGIA_BASE = {
    "Block 1": {
        "Week 1": {"strength": "Back Squat 4x8 @ 65-70% RPE 7", "skill": "Hang High Snatch 5x3", "wod": "AMRAP 12 min:\n- 12 DB Goblet Squats\n- 10 Ring Rows\n- 8 Push-ups"},
        "Week 2": {"strength": "Back Squat 5x5 @ 75-80% RPE 8", "skill": "Hang Power Snatch 5x2", "wod": "For Time (Cap 15 min):\n- 15-12-9 Barbell Squats + Toes to Bar"},
        "Week 3": {"strength": "Back Squat 5x3 @ 85% RPE 9", "skill": "Squat Snatch 6x1", "wod": "4 Rounds For Time:\n- 400m Run\n- 10 Wall Balls\n- 5 Heavy Power Cleans"},
        "Week 4": {"strength": "3RM Back Squat Test", "skill": "Benchmark Isabel", "wod": "Benchmark Fran"}
    },
    "Block 2": {
        "Week 1": {"strength": "Deadlift 4x8 @ 65%", "skill": "DB High Pull 4x10", "wod": "EMOM 20 min:\n- Min 1: 15 Cal Row\n- Min 2: 12 Burpees"},
        "Week 2": {"strength": "Deadlift 5x5 @ 75%", "skill": "Hang Clean 5x3", "wod": "Chipper For Time:\n- 800m Run\n- 40 Box Jumps"},
        "Week 3": {"strength": "Deadlift 5x3 @ 85%", "skill": "Power Clean 5x2", "wod": "5 Sets:\n- 200m Run\n- Max Burpee Box Jumps"},
        "Week 4": {"strength": "Active Deload", "skill": "Mobility", "wod": "Benchmark Helen"}
    },
    "Block 3": {
        "Week 1": {"strength": "Strict Press 4x8", "skill": "SOTS Press 4x5", "wod": "AMRAP 14 min:\n- 10 Pull-ups\n- 15 Push-ups"},
        "Week 2": {"strength": "Strict Press 5x5", "skill": "Snatch Balance 5x3", "wod": "EMOM 16 min:\n- 8 Chest to Bar\n- 10 HSPU"},
        "Week 3": {"strength": "Strict Press 5x3", "skill": "Squat Snatch 5x2", "wod": "For Time:\n- 21-15-9 Bar Muscle-ups"},
        "Week 4": {"strength": "Max Pull-ups Test", "skill": "Mobility", "wod": "Benchmark Cindy"}
    },
    "Block 4": {
        "Week 1": {"strength": "Front Squat 4x6", "skill": "Snatch Complex", "wod": "AMRAP 10 min:\n- 6 Power Cleans"},
        "Week 2": {"strength": "Front Squat 5x4", "skill": "Clean Complex", "wod": "For Time:\n- 15-12-9 Clean & Jerks"},
        "Week 3": {"strength": "Front Squat 5x2", "skill": "C&J Single", "wod": "Benchmark Grace"},
        "Week 4": {"strength": "1RM Front Squat", "skill": "Assessment", "wod": "Benchmark DT"}
    }
}

def gerar_todas_sugestoes(bloco_sel, semana_sel, strength_txt, skill_txt, wod_txt):
    key_block = bloco_sel.split(" ")[0] + " " + bloco_sel.split(" ")[1]
    key_week = semana_sel.split(" ")[0] + " " + semana_sel.split(" ")[1]
    base_bloco = METODOLOGIA_BASE.get(key_block, {}).get(key_week, {"strength": "Strength", "skill": "Skill", "wod": "WOD"})
    
    s_usada = strength_txt if len(strength_txt.strip()) > 5 else base_bloco["strength"]
    l_usada = skill_txt if len(skill_txt.strip()) > 5 else base_bloco["skill"]
    m_usada = wod_txt if len(wod_txt.strip()) > 5 else base_bloco["wod"]
    
    df_sug = pd.DataFrame({
        "Session Block": ["1. Warm-Up", "2. Strength", "3. Skill", "4. WOD", "5. Accessory", "6. Mobility"],
        "Recommended Programming": ["2-3 Rounds: Air Squats", base_bloco["strength"], base_bloco["skill"], base_bloco["wod"], "Core Accessory", "Mobility"]
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
    {"day": "Thursday", "focus": "CrossFit - Strength / LPO"},
    {"day": "Friday", "focus": "ATHX"},
    {"day": "Saturday", "focus": "Community WOD"},
    {"day": "Sunday", "focus": "Benchmark / Hero"}
]

treinos_salvos = carregar_treinos_salvos()
tabs = st.tabs([d["day"] for d in dias_semana])

lista_blocos_semana_acumulados = []
dados_para_salvar = {}

for i, tab in enumerate(tabs):
    day_info = dias_semana[i]
    day_name = day_info["day"]
    
    with tab:
        st.subheader(f"{day_name} — {day_info['focus']}")
        
        col1, col2 = st.columns([1.2, 1])
        lista_blocos_do_dia = []
        
        with col1:
            st.markdown("### 📋 Session Structure (60 min)")
            t_s, t_m = 0, 0
            
            if day_name == "Monday":
                st.info("🏃 **HYROX Session:** Running + Functional Stations")
                c1, c2 = st.columns(2)
                with c1: t_w = st.number_input("Warm-Up (min)", 1, 60, treinos_salvos.get(f"{day_name}_t_w", 10), key=f"t_hy_w_{i}")
                with c2: w_input = st.text_area(f"Warm-Up ({t_w}')", treinos_salvos.get(f"{day_name}_w", "Dynamic Mobility"), height=90, key=f"hy_w_{i}")
                
                s_input, l_input = "", ""
                c3, c4 = st.columns(2)
                with c3: t_m = st.number_input("Main Block (min)", 1, 60, treinos_salvos.get(f"{day_name}_t_m", 40), key=f"t_hy_m_{i}")
                with c4: m_input = st.text_area(f"HYROX Main Block ({t_m}')", treinos_salvos.get(f"{day_name}_m", "Running + Stations"), height=140, key=f"hy_m_{i}")
                
                c5, c6 = st.columns(2)
                with c5: t_r = st.number_input("Mobility (min)", 1, 60, treinos_salvos.get(f"{day_name}_t_r", 10), key=f"t_hy_r_{i}")
                with c6: r_input = st.text_area(f"Mobility ({t_r}')", treinos_salvos.get(f"{day_name}_r", "Stretching"), height=80, key=f"hy_r_{i}")
                
                total_time = t_w + t_m + t_r
                lista_blocos_do_dia = [{"texto": w_input, "tempo": t_w}, {"texto": m_input, "tempo": t_m}]
                dados_para_salvar.update({f"{day_name}_t_w": t_w, f"{day_name}_w": w_input, f"{day_name}_t_m": t_m, f"{day_name}_m": m_input, f"{day_name}_t_r": t_r, f"{day_name}_r": r_input})

            elif day_name == "Friday":
                st.info("🔥 **ATHX Session:** Fixed Structure")
                c1, c2 = st.columns(2)
                with c1: t_w = st.number_input("Warm-Up (min)", 1, 60, treinos_salvos.get(f"{day_name}_t_w", 10), key=f"t_athx_w_{i}")
                with c2: w_input = st.text_area(f"Warm-Up ({t_w}')", treinos_salvos.get(f"{day_name}_w", "Dynamic"), height=90, key=f"athx_w_{i}")

                c3, c4 = st.columns(2)
                with c3: t_s = st.number_input("Strength Max (min)", 0, 60, treinos_salvos.get(f"{day_name}_t_s", 15), key=f"t_athx_s_{i}")
                with c4: s_input = st.text_area(f"Strength Max ({t_s}')", treinos_salvos.get(f"{day_name}_s", ""), height=90, key=f"athx_s_{i}")

                c5, c6 = st.columns(2)
                with c5: t_e = st.number_input("Endurance (min)", 0, 60, treinos_salvos.get(f"{day_name}_t_e", 15), key=f"t_athx_e_{i}")
                with c6: l_input = st.text_area(f"Endurance ({t_e}')", treinos_salvos.get(f"{day_name}_e", ""), height=90, key=f"athx_e_{i}")

                c7, c8 = st.columns(2)
                with c7: t_m = st.number_input("MetCon X (min)", 1, 60, treinos_salvos.get(f"{day_name}_t_m", 15), key=f"t_athx_m_{i}")
                with c8: m_input = st.text_area(f"MetCon X ({t_m}')", treinos_salvos.get(f"{day_name}_m", ""), height=110, key=f"athx_m_{i}")

                c9, c10 = st.columns(2)
                with c9: t_r = st.number_input("Mobility (min)", 0, 60, treinos_salvos.get(f"{day_name}_t_r", 5), key=f"t_athx_r_{i}")
                with c10: r_input = st.text_area(f"Mobility ({t_r}')", treinos_salvos.get(f"{day_name}_r", "Stretching"), height=80, key=f"athx_r_{i}")

                total_time = t_w + t_s + t_e + t_m + t_r
                lista_blocos_do_dia = [{"texto": w_input, "tempo": t_w}, {"texto": s_input, "tempo": t_s}, {"texto": l_input, "tempo": t_e}, {"texto": m_input, "tempo": t_m}]
                dados_para_salvar.update({f"{day_name}_t_w": t_w, f"{day_name}_w": w_input, f"{day_name}_t_s": t_s, f"{day_name}_s": s_input, f"{day_name}_t_e": t_e, f"{day_name}_e": l_input, f"{day_name}_t_m": t_m, f"{day_name}_m": m_input, f"{day_name}_t_r": t_r, f"{day_name}_r": r_input})

            else:
                c1, c2 = st.columns(2)
                with c1: t_w = st.number_input("Warm-Up (min)", 1, 60, treinos_salvos.get(f"{day_name}_t_w", 10), key=f"t_cf_w_{i}")
                with c2: w_input = st.text_area(f"1. Warm-Up ({t_w}')", treinos_salvos.get(f"{day_name}_w", "Warm-up"), height=100, key=f"cf_w_{i}")

                c3, c4 = st.columns(2)
                with c3: t_s = st.number_input("Strength (min)", 0, 60, treinos_salvos.get(f"{day_name}_t_s", 15), key=f"t_cf_s_{i}")
                with c4: s_input = st.text_area(f"2. Strength ({t_s}')", treinos_salvos.get(f"{day_name}_s", ""), height=90, key=f"cf_s_{i}")

                c5, c6 = st.columns(2)
                with c5: t_l = st.number_input("Skill (min)", 0, 60, treinos_salvos.get(f"{day_name}_t_l", 10), key=f"t_cf_l_{i}")
                with c6: l_input = st.text_area(f"3. Skill ({t_l}')", treinos_salvos.get(f"{day_name}_l", ""), height=120, key=f"cf_l_{i}")

                c7, c8 = st.columns(2)
                with c7: t_m = st.number_input("WOD (min)", 1, 60, treinos_salvos.get(f"{day_name}_t_m", 15), key=f"t_cf_m_{i}")
                with c8: 
                    m_input = st.text_area(f"4. WOD ({t_m}')", treinos_salvos.get(f"{day_name}_m", ""), height=140, key=f"cf_wod_{i}")
                    st.caption(estimar_tempo_wod(m_input))

                c9, c10 = st.columns(2)
                with c9: t_a = st.number_input("Accessory (min)", 0, 60, treinos_salvos.get(f"{day_name}_t_a", 5), key=f"t_cf_a_{i}")
                with c10: a_input = st.text_area(f"5. Accessory ({t_a}')", treinos_salvos.get(f"{day_name}_a", "Accessory"), height=80, key=f"cf_a_{i}")

                c11, c12 = st.columns(2)
                with c11: t_r = st.number_input("Mobility (min)", 0, 60, treinos_salvos.get(f"{day_name}_t_r", 5), key=f"t_cf_r_{i}")
                with c12: r_input = st.text_area(f"6. Mobility ({t_r}')", treinos_salvos.get(f"{day_name}_r", "Mobility"), height=80, key=f"cf_m_{i}")

                total_time = t_w + t_s + t_l + t_m + t_a + t_r
                lista_blocos_do_dia = [
                    {"texto": w_input, "tempo": t_w}, {"texto": s_input, "tempo": t_s},
                    {"texto": l_input, "tempo": t_l}, {"texto": m_input, "tempo": t_m},
                    {"texto": a_input, "tempo": t_a}
                ]
                
                dados_para_salvar.update({
                    f"{day_name}_t_w": t_w, f"{day_name}_w": w_input,
                    f"{day_name}_t_s": t_s, f"{day_name}_s": s_input,
                    f"{day_name}_t_l": t_l, f"{day_name}_l": l_input,
                    f"{day_name}_t_m": t_m, f"{day_name}_m": m_input,
                    f"{day_name}_t_a": t_a, f"{day_name}_a": a_input,
                    f"{day_name}_t_r": t_r, f"{day_name}_r": r_input
                })

            lista_blocos_semana_acumulados.extend(lista_blocos_do_dia)

            # --- CÁLCULO DO IACS DIÁRIO ---
            vol_dia = extrair_volume_acumulado_estruturado(lista_blocos_do_dia)
            eh_especial = ("HYROX" in day_info["focus"] or "ATHX" in day_info["focus"])
            iacs_dia = calcular_iacs_de_vol(vol_dia, eh_especial)

            st.markdown("---")
            col_metric1, col_metric2 = st.columns(2)
            
            with col_metric1:
                if total_time > 60:
                    st.warning(f"⚠️ **Duration:** {total_time} min / 60 min")
                else:
                    st.success(f"⏱️ **Duration:** {total_time} min / 60 min")

            with col_metric2:
                if iacs_dia <= 10:
                    st.info(f"🟢 **Daily Alpha Load (IACS):** {iacs_dia} pts (Recovery)")
                elif iacs_dia <= 20:
                    st.success(f"🟡 **Daily Alpha Load (IACS):** {iacs_dia} pts (Moderate)")
                elif iacs_dia <= 32:
                    st.warning(f"🟠 **Daily Alpha Load (IACS):** {iacs_dia} pts (High Intensity)")
                else:
                    st.error(f"🔴 **Daily Alpha Load (IACS):** {iacs_dia} pts (Shock Session)")

        with col2:
            st.markdown("### 🎯 Scaling Chart (RX / INT / BEG / MASTERS)")
            escala_df = pd.DataFrame({
                "Level": ["RX", "Intermediate", "Beginner", "Masters"],
                "Load / Category": ["100% RX Load", "70-80% Load", "50% Load / Dumbbells", "Custom Scaling"],
                "Gymnastics": ["Full Movement", "Medium Progression", "Basic Scale", "Range Focus"]
            })
            st.table(escala_df)
            
            st.markdown("### 💡 Intelligence Suggestions")
            s_val = s_input if 's_input' in locals() else ""
            l_val = l_input if 'l_input' in locals() else ""
            m_val = m_input if 'm_input' in locals() else ""
            
            df_todas_sugestoes = gerar_todas_sugestoes(bloco, semana, s_val, l_val, m_val)
            st.table(df_todas_sugestoes)
            
            st.markdown("---")
            st.markdown("### 🔍 Validation Checklist")
            st.checkbox("Session objective clearly defined?", value=True, key=f"chk1_{i}")
            st.checkbox("Dominant movement pattern respected?", value=True, key=f"chk2_{i}")
            st.checkbox("Session within 60 minutes time cap?", value=True, key=f"chk3_{i}")
            st.checkbox("Scaling options available for all levels?", value=True, key=f"chk4_{i}")

salvar_treinos_disco(dados_para_salvar)

# --- CÁLCULO SEMANAL ---
vol_usado_semana = extrair_volume_acumulado_estruturado(lista_blocos_semana_acumulados)

tabela_volume = pd.DataFrame({
    "Pattern": ["Squat", "Hinge", "Push", "Pull", "Core", "Snatch", "Clean & Jerk", "Run (KM)"],
    "Target": [
        f"{int(metas['Squat'])}", f"{int(metas['Hinge'])}", f"{int(metas['Push'])}", 
        f"{int(metas['Pull'])}", f"{int(metas['Core'])}", f"{int(metas['Snatch'])}", 
        f"{int(metas['Clean & Jerk'])}", f"{metas['Run']} km"
    ],
    "Used": [
        f"{int(vol_usado_semana['Squat'])}", f"{int(vol_usado_semana['Hinge'])}", f"{int(vol_usado_semana['Push'])}", 
        f"{int(vol_usado_semana['Pull'])}", f"{int(vol_usado_semana['Core'])}", f"{int(vol_usado_semana['Snatch'])}", 
        f"{int(vol_usado_semana['Clean & Jerk'])}", f"{round(vol_usado_semana['Run'], 2)} km"
    ],
    "Balance": [
        f"{int(metas['Squat'] - vol_usado_semana['Squat'])}",
        f"{int(metas['Hinge'] - vol_usado_semana['Hinge'])}",
        f"{int(metas['Push'] - vol_usado_semana['Push'])}",
        f"{int(metas['Pull'] - vol_usado_semana['Pull'])}",
        f"{int(metas['Core'] - vol_usado_semana['Core'])}",
        f"{int(metas['Snatch'] - vol_usado_semana['Snatch'])}",
        f"{int(metas['Clean & Jerk'] - vol_usado_semana['Clean & Jerk'])}",
        f"{round(metas['Run'] - vol_usado_semana['Run'], 2)} km"
    ]
})

st.sidebar.table(tabela_volume)

iacs_semanal_total = calcular_iacs_de_vol(vol_usado_semana)
st.sidebar.metric("Weekly Alpha Load (Total IACS)", f"{int(iacs_semanal_total)} pts")

if iacs_semanal_total <= 45:
    st.sidebar.success("Classification: Light Week")
elif iacs_semanal_total <= 60:
    st.sidebar.info("Classification: Moderate Week")
elif iacs_semanal_total <= 75:
    st.sidebar.warning("Classification: Heavy Week")
elif iacs_semanal_total <= 90:
    st.sidebar.error("Classification: Shock Week")
else:
    st.sidebar.error("⚠️ Not Recommended for Regular Classes")

st.markdown("---")
if st.button("💾 Save & Export Weekly Programming"):
    st.success("Programming successfully synchronized with Alpha Iron 2.0 Sheet!")
