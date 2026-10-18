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

# --- INJEÇÃO FORÇADA DO FAVICON NA ABA DO NAVEGADOR VIA HTML ---
def injetar_favicon_html():
    if os.path.exists("favicon.png"):
        try:
            with open("favicon.png", "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            
            st.markdown(
                f"""
                <script>
                const doc = window.parent.document;
                let link = doc.querySelector("link[rel*='icon']") || doc.createElement('link');
                link.type = 'image/png';
                link.rel = 'icon';
                link.href = 'data:image/png;base64,{encoded}';
                doc.getElementsByTagName('head')[0].appendChild(link);
                </script>
                """,
                unsafe_allow_html=True
            )
        except Exception:
            pass

injetar_favicon_html()

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

# --- IA: ESTIMATIVA DE TEMPO DO WOD ---
def estimar_tempo_wod(texto_wod):
    """Estima o tempo de conclusão (em minutos) com base nos movimentos e volume."""
    if not texto_wod or len(texto_wod.strip()) < 3:
        return "Insira o WOD para calcular"
        
    texto_low = texto_wod.lower()
    
    m_cap = re.search(r'(?:cap|time cap)\D*(\d+)', texto_low)
    if m_cap:
        return f"⏱️ Time Cap Definido: {m_cap.group(1)} min"

    linhas = [l.strip() for l in texto_wod.split("\n") if l.strip()]
    
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

    if num_rounds > 1 and not esquema_21_15_9:
        total_reps_totais = total_reps_base * num_rounds
    else:
        total_reps_totais = total_reps_base if total_reps_base > 0 else 50

    fator_tempo_por_rep = 2.5 
    if any(k in texto_low for k in ["bmu", "bar muscle", "muscle-up", "hspu", "snatch", "clean & jerk"]):
        fator_tempo_por_rep = 4.0 

    segundos_estimados = total_reps_totais * fator_tempo_por_rep
    minutos_estimados = max(4, round(segundos_estimados / 60))

    return f"🤖 Estimativa da IA: ~{minutos_estimados} min (Volume aprox: {total_reps_totais} reps)"

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

# --- CÁLCULO DE VOLUME (USADO TANTO PARA O DIA QUANTO PARA A SEMANA) ---
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

            # Regra Pull / BMU separada
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

# --- BANCO DE DADOS METODOLÓGICO ---
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

def gerar_todas_sugestoes(bloco_sel, semana_sel, strength_txt, skill_txt, wod_txt):
    key_block = bloco_sel.split(" ")[0] + " " + bloco_sel
