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
    page_title="Alpha Iron Athletics 2.0 — Sistema de Gestão", 
    layout="wide"
)

# --- DESIGN SYSTEM / CSS CUSTOMIZADO (ALPHA IRON ATHLETICS - AZUL ELÉTRICO) ---
st.markdown("""
    <style>
    /* Remove a barra/cabeçalho branco padrão do Streamlit no topo */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* Fundo principal da aplicação */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #121418;
        border-right: 1px solid #22262d;
    }

    /* OCULTAR OS CÍRCULOS (BOLINHAS) DO MENU LATERAL (RADIO) */
    [data-testid="stSidebar"] input[type="radio"] {
        display: none !important;
    }
    
    /* Estilização limpa para os itens do menu lateral sem os botões padrão */
    [data-testid="stSidebar"] div.row-widget.stRadio > div {
        gap: 4px;
    }
    [data-testid="stSidebar"] div.row-widget.stRadio label {
        background-color: transparent;
        padding: 6px 10px;
        border-radius: 6px;
        color: #9ca3af;
        font-weight: 500;
        cursor: pointer;
        width: 100%;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] div.row-widget.stRadio label:hover {
        background-color: #1a1d24;
        color: #00E5FF;
    }

    /* Títulos e Cabeçalhos com Azul Elétrico */
    h1, h2, h3, h4 {
        color: #00E5FF !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Estilização das abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #121418;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #22262d;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1d24;
        color: #9ca3af;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00E5FF !important;
        color: #0e1117 !important;
    }

    /* Inputs de texto e áreas de texto */
    .stTextInput input, .stTextArea textarea {
        background-color: #161920 !important;
        color: #ffffff !important;
        border: 1px solid #2a2f3a !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 5px rgba(0, 229, 255, 0.3) !important;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 24px !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
    }

    /* Tabelas */
    table {
        background-color: #161920 !important;
        border-radius: 8px;
        color: #e5e7eb !important;
    }
    
    th {
        background-color: #1f242d !important;
        color: #00E5FF !important;
    }

    /* Botões personalizados com Azul Elétrico */
    .stButton button {
        background: linear-gradient(135deg, #0051ff 0%, #00e5ff 100%);
        color: #0e1117;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 229, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #0066ff 0%, #33edff 100%);
        box-shadow: 0 6px 16px rgba(0, 229, 255, 0.5);
        transform: translateY(-1px);
    }
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
                <div style="text-align: center; padding-bottom: 15px;">
                    <img src="data:image/png;base64,{encoded_string}" style="max-width: 90%; height: auto; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception:
            st.sidebar.markdown("<h2 style='text-align: center; color: #00E5FF;'>ALPHA IRON</h2>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<h2 style='text-align: center; color: #00E5FF;'>ALPHA IRON</h2>", unsafe_allow_html=True)

carregar_logo_sidebar()

# --- CONTROLE DE ESTADO DA NAVEGAÇÃO ---
if "menu_escolhido" not in st.session_state:
    st.session_state.menu_escolhido = "Início (Dashboard)"

opcoes_menu = [
    "Início (Dashboard)",
    "Programação Semanal",
    "Montagem de Treinos",
    "Biblioteca de WODs",
    "Biblioteca de Exercícios",
    "Treinos Salvos",
    "Configurações"
]

# --- MENU LATERAL DE NAVEGAÇÃO PROFISSIONAL ---
st.sidebar.markdown("### Menu Principal")

# O rádio atualiza diretamente o st.session_state.menu_escolhido de forma fluida
indice_atual = opcoes_menu.index(st.session_state.menu_escolhido) if st.session_state.menu_escolhido in opcoes_menu else 0
st.session_state.menu_escolhido = st.sidebar.radio(
    "Navegação",
    opcoes_menu,
    index=indice_atual,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# --- BARRA LATERAL: PERIODIZAÇÃO ---
st.sidebar.header("Periodização (Planilha 2.0)")
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

metas = obter_metas_volume(bloco, semana)

# --- CÁLCULO DE VOLUME UNIVERSAL (LPO + 4X12) ---
def extrair_volume_acumulado_estruturado(lista_blocos_dados):
    vol = {"Squat": 0, "Hinge": 0, "Push": 0, "Pull": 0, "Core": 0, "Snatch": 0, "Clean & Jerk": 0, "Run": 0.0}
    ultimo_exercicio_contexto = ""
    
    for item in lista_blocos_dados:
        texto = item.get("texto", "").strip()
        tempo_minutos = item.get("tempo", 0)
        
        if not texto:
            continue
            
        linhas = [l.strip() for l in texto.split("\n") if l.strip()]
        texto_low = texto.lower()
        is_emom = "emom" in texto_low or "e90s" in texto_low or "e90" in texto_low
        
        num_rounds = 1
        for l in linhas:
            m_rnds = re.search(r'(\d+)\s*(?:rounds|rnds|sets|series|séries|rodadas)', l.lower())
            if m_rnds:
                num_rounds = int(m_rnds.group(1))
                break

        if is_emom and num_rounds == 1 and tempo_minutos > 0:
            if "e90" in texto_low or "90s" in texto_low:
                num_rounds = max(1, (tempo_minutos * 60) >> 1)
            else:
                num_rounds = tempo_minutos

        for linha in linhas:
            linha_limpa = linha.lower().strip()
            if not linha_limpa or any(k in linha_limpa for k in ["rx:", "scaled:", "emom", "amrap", "for time", "cap ", "e90"]):
                continue

            reps_calculadas = 0
            m_perc_reps = re.search(r'(\d+)%\s*-\s*(\d+)(?:\((\d+)\))?', linha_limpa)
            if m_perc_reps:
                reps_por_serie = int(m_perc_reps.group(2))
                multiplicador_series = int(m_perc_reps.group(3)) if m_perc_reps.group(3) else 1
                reps_calculadas = reps_por_serie * multiplicador_series
            else:
                m_mult = re.findall(r'(\d+)\s*x\s*(\d+)', linha_limpa)
                if m_mult:
                    for s, r in m_mult:
                        reps_calculadas += int(s) * int(r)
                else:
                    esquema_hifen = re.findall(r'(\d+)-(\d+)-(\d+)', linha_limpa)
                    if esquema_hifen:
                        for a, b, c in esquema_hifen:
                            reps_calculadas += int(a) + int(b) + int(c)
                    else:
                        nums = re.findall(r'\b(\d+)\b', linha_limpa)
                        if nums:
                            reps_encontradas = [int(n) for n in nums if int(n) <= 300]
                            if reps_encontradas:
                                reps_calculadas = reps_encontradas[0]

            if reps_calculadas == 0:
                ultimo_exercicio_contexto = linha_limpa
                continue

            alvo_texto = f"{ultimo_exercicio_contexto} {linha_limpa}"
            is_bmu = any(k in alvo_texto for k in ["bmu", "bar muscle up", "bar muscle-up", "muscle up", "rmu"])
            reps_totais = reps_calculadas * num_rounds if not is_emom else reps_calculadas

            if any(k in alvo_texto for k in ["squat", "agacho", "agachamento", "thruster", "wall ball", "wallball", "lunge", "lunges", "passada", "pistol", "squat clean", "squat snatch", "front squat", "back squat", "ohs", "balance"]):
                vol["Squat"] += reps_totais
            if any(k in alvo_texto for k in ["deadlift", "terra", "rdl", "snatch", "clean", "swing", "good morning", "hip thrust", "extensora", "flexora"]):
                vol["Hinge"] += reps_totais
            if any(k in alvo_texto for k in ["push", "press", "jerk", "thruster", "hspu", "dip", "dips", "bench", "flexao", "flexão", "supino", "wall ball", "wallball", "desenvolvimento"]):
                vol["Push"] += reps_totais
            if is_bmu or any(k in alvo_texto for k in ["pull", "pullup", "pull-up", "c2b", "chest to bar", "row", "remada", "rope climb", "puxada", "pulldown"]):
                vol["Pull"] += reps_totais
            if any(k in alvo_texto for k in ["toes to bar", "ttb", "knees to elbow", "kte", "sit up", "situp", "v-up", "hollow", "plank", "prancha", "l-sit", "abmat", "ghd", "abdominal"]):
                vol["Core"] += reps_totais
            if any(k in alvo_texto for k in ["snatch", "arranco", "snatch balance"]):
                vol["Snatch"] += reps_totais
            if any(k in alvo_texto for k in ["clean", "jerk", "arremesso", "clean & jerk", "clean and jerk"]):
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

def calcular_alpha_wod_load(texto_wod, tempo_wod):
    if not texto_wod or not texto_wod.strip():
        return 0
    txt_low = texto_wod.lower()
    vol_wod = extrair_volume_acumulado_estruturado([{"texto": texto_wod, "tempo": tempo_wod}])
    volume_total_reps = sum(vol_wod.values()) - vol_wod["Run"]
    quilometragem_run = vol_wod["Run"]
    
    fator_modalidade = 1.0
    if "for time" in txt_low:
        fator_modalidade = 1.35
    elif "amrap" in txt_low:
        fator_modalidade = 1.25
    elif "emom" in txt_low or "e90" in txt_low:
        fator_modalidade = 1.10
    
    score_wod = (volume_total_reps * 0.15 + quilometragem_run * 4.0) * fator_modalidade
    if any(k in txt_low for k in ["muscle-up", "bmu", "hspu", "snatch", "clean & jerk", "rope climb"]):
        score_wod *= 1.2
    return int(max(score_wod, 5 if len(txt_low) > 5 else 0))

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
    
    df_sug = pd.DataFrame({
        "Session Block": ["1. Warm-Up", "2. Strength", "3. Skill", "4. WOD", "5. Accessory", "6. Mobility"],
        "Recommended Programming": ["2-3 Rounds: Air Squats", base_bloco["strength"], base_bloco["skill"], base_bloco["wod"], "Core Accessory", "Mobility"]
    })
    return df_sug

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

# ==========================================
# ROTEAMENTO DE TELAS COM BASE NO SESSION STATE
# ==========================================
if st.session_state.menu_escolhido == "Início (Dashboard)":
    st.title("Alpha Iron Athletics — Painel Principal")
    st.markdown("Bem-vindo ao centro de comando da periodização e montagem de treinos da metodologia Alpha.")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.metric("Fase Atual", bloco.split(" - ")[1])
    with col_d2:
        st.metric("Ciclo Semanal", semana.split(" - ")[1])
    with col_d3:
        st.metric("Status da Base", "Sincronizado")

    st.markdown("---")
    st.subheader("Atalhos Rápidos")
    
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        if st.button("Programação Semanal"):
            st.session_state.menu_escolhido = "Programação Semanal"
            st.rerun()
    with col_a2:
        if st.button("Montar / Editar Treinos"):
            st.session_state.menu_escolhido = "Montagem de Treinos"
            st.rerun()
    with col_a3:
        if st.button("Treinos Salvos"):
            st.session_state.menu_escolhido = "Treinos Salvos"
            st.rerun()

    st.markdown("---")
    st.subheader("Resumo de Volume da Semana")
    
    lista_temp = []
    for d_info in dias_semana:
        d_n = d_info["day"]
        w_t = treinos_salvos.get(f"{d_n}_t_w", 10)
        w_txt = treinos_salvos.get(f"{d_n}_w", "")
        m_t = treinos_salvos.get(f"{d_n}_t_m", 15)
        m_txt = treinos_salvos.get(f"{d_n}_m", "")
        lista_temp.append({"texto": w_txt, "tempo": w_t})
        lista_temp.append({"texto": m_txt, "tempo": m_t})
        
    vol_resumo = extrair_volume_acumulado_estruturado(lista_temp)
    df_dash_vol = pd.DataFrame({
        "Padrão de Movimento": ["Squat", "Hinge", "Push", "Pull", "Core", "Snatch", "Clean & Jerk", "Run"],
        "Meta": [metas["Squat"], metas["Hinge"], metas["Push"], metas["Pull"], metas["Core"], metas["Snatch"], metas["Clean & Jerk"], f"{metas['Run']} km"],
        "Programado": [vol_resumo["Squat"], vol_resumo["Hinge"], vol_resumo["Push"], vol_resumo["Pull"], vol_resumo["Core"], vol_resumo["Snatch"], vol_resumo["Clean & Jerk"], f"{round(vol_resumo['Run'], 2)} km"]
    })
    st.table(df_dash_vol)

elif st.session_state.menu_escolhido == "Programação Semanal":
    st.title("Programação Semanal Alpha Iron")
    st.markdown("Consulte de forma limpa e objetiva o planejamento completo dos treinos de toda a semana.")
    
    dia_selecionado = st.selectbox("Selecione o Dia para Consulta Rápida", [d["day"] + " — " + d["focus"] for d in dias_semana])
    dia_idx = [d["day"] + " — " + d["focus"] for d in dias_semana].index(dia_selecionado)
    d_info = dias_semana[dia_idx]
    d_name = d_info["day"]
    
    st.markdown(f"### Ficha Técnica: {d_name} ({d_info['focus']})")
    
    w_t = treinos_salvos.get(f"{d_name}_t_w", 10)
    w_txt = treinos_salvos.get(f"{d_name}_w", "Não cadastrado")
    m_t = treinos_salvos.get(f"{d_name}_t_m", 15)
    m_txt = treinos_salvos.get(f"{d_name}_m", "Não cadastrado")
    
    st.markdown(f"**1. Warm-Up ({w_t} min):**")
    st.code(w_txt, language="text")
    
    if d_name not in ["Monday", "Friday"]:
        s_t = treinos_salvos.get(f"{d_name}_t_s", 15)
        s_txt = treinos_salvos.get(f"{d_name}_s", "Não cadastrado")
        l_t = treinos_salvos.get(f"{d_name}_t_l", 10)
        l_txt = treinos_salvos.get(f"{d_name}_l", "Não cadastrado")
        a_t = treinos_salvos.get(f"{d_name}_t_a", 5)
        a_txt = treinos_salvos.get(f"{d_name}_a", "Não cadastrado")
        r_t = treinos_salvos.get(f"{d_name}_t_r", 5)
        r_txt = treinos_salvos.get(f"{d_name}_r", "Não cadast
