import streamlit as st
import pandas as pd
import os
import glob
import base64
import re
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

st.set_page_config(
    page_title="Alpha Iron Athletics 2.0 — Sistema de Gestão", 
    layout="wide"
)

# ==========================================
# MODO WOD TV (Exibição em Tela Cheia na TV)
# ==========================================
query_params = st.query_params
if query_params.get("modo") == "tv":
    st.markdown("""
        <style>
        [data-testid="stHeader"], [data-testid="stSidebar"], footer {display: none !important;}
        body, .stApp { background-color: #0e1117 !important; color: #f0f2f6 !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #00E5FF; font-size: 38px;'>ALPHA IRON ATHLETICS — WOD TV</h1>", unsafe_allow_html=True)
    
    fuso_br = timezone(timedelta(hours=-3))
    agora_br = datetime.now(fuso_br)
    dias_ingles = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dia_atual_str = dias_ingles[agora_br.weekday()]
    
    dias_traducao_pt = {
        "Monday": "Segunda-feira — HYROX",
        "Tuesday": "Terça-feira — CrossFit (Strength / LPO)",
        "Wednesday": "Quarta-feira — CrossFit (Gymnastics)",
        "Thursday": "Quinta-feira — CrossFit (Strength / LPO)",
        "Friday": "Sexta-feira — ATHX",
        "Saturday": "Sábado — Community WOD",
        "Sunday": "Domingo — Benchmark / Hero WOD"
    }

    auth_file_tv = "usuarios_credenciais.json"
    db_alvo = "treinos_salvos_mikael.json"
    if os.path.exists(auth_file_tv):
        try:
            with open(auth_file_tv, "r", encoding="utf-8") as f_cred:
                creds_tv = json.load(f_cred)
                nomes_users = list(creds_tv.keys())
                if nomes_users:
                    col_sel_tv1, col_sel_tv2, col_sel_tv3 = st.columns([1, 2, 1])
                    with col_sel_tv2:
                        user_escolhido_tv = st.selectbox("Selecione o Coach / Unidade para Exibição:", nomes_users, key="sel_user_tv")
                        db_alvo = creds_tv[user_escolhido_tv].get("db", "treinos_salvos_mikael.json")
        except Exception:
            pass

    dados_treinos = {}
    if os.path.exists(db_alvo):
        try:
            with open(db_alvo, "r", encoding="utf-8") as f_db:
                dados_treinos = json.load(f_db)
        except Exception:
            pass

    nome_dia_exibicao = dias_traducao_pt.get(dia_atual_str, dia_atual_str)
    st.markdown(f"<p style='text-align: center; color: #9ca3af; font-size: 22px;'>📅 Hoje: <strong>{nome_dia_exibicao}</strong> (Atualização Automática)</p>", unsafe_allow_html=True)
    st.markdown("---")

    w_t = dados_treinos.get(f"{dia_atual_str}_t_w", 10)
    w_txt = dados_treinos.get(f"{dia_atual_str}_w", "")
    s_t = dados_treinos.get(f"{dia_atual_str}_t_s", 15)
    s_txt = dados_treinos.get(f"{dia_atual_str}_s", "")
    l_t = dados_treinos.get(f"{dia_atual_str}_t_l", 10)
    l_txt = dados_treinos.get(f"{dia_atual_str}_l", "")
    m_t = dados_treinos.get(f"{dia_atual_str}_t_m", 15)
    m_txt = dados_treinos.get(f"{dia_atual_str}_m", "")
    a_t = dados_treinos.get(f"{dia_atual_str}_t_a", 5)
    a_txt = dados_treinos.get(f"{dia_atual_str}_a", "")
    r_t = dados_treinos.get(f"{dia_atual_str}_t_r", 5)
    r_txt = dados_treinos.get(f"{dia_atual_str}_r", "")
    e_t = dados_treinos.get(f"{dia_atual_str}_t_e", 15)
    e_txt = dados_treinos.get(f"{dia_atual_str}_e", "")

    col_tv_1, col_tv_2 = st.columns([1, 1])
    with col_tv_1:
        st.markdown(f"### ⚡ Warm-Up & Prep ({w_t} min)")
        if w_txt:
            st.code(w_txt, language="text")
        else:
            st.info("Nenhum aquecimento cadastrado para hoje.")
            
        if s_txt:
            st.markdown(f"### 🏋️ Strength / Força ({s_t} min)")
            st.code(s_txt, language="text")
            
        if l_txt:
            st.markdown(f"### 🎯 Skill / Técnica ({l_t} min)")
            st.code(l_txt, language="text")

    with col_tv_2:
        if m_txt:
            st.markdown(f"### 🔥 WOD / Main Block ({m_t} min)")
            st.code(m_txt, language="text")
        else:
            st.info("Nenhum WOD principal cadastrado para hoje.")

        if a_txt:
            st.markdown(f"### 🛡️ Accessory ({a_t} min)")
            st.code(a_txt, language="text")

        if r_txt:
            st.markdown(f"### 🧘 Mobility ({r_t} min)")
            st.code(r_txt, language="text")

    st.stop()


# ==========================================
# SISTEMA PRINCIPAL
# ==========================================

def obter_fundo_base64():
    nomes_possiveis = ["alpha_iron.jpg", "alpha_iron.png", "Alpha_Iron.jpg", "Alpha_Iron.png"]
    for nome in nomes_possiveis:
        if os.path.exists(nome):
            with open(nome, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    arquivos = glob.glob("*.jpg") + glob.glob("*.png") + glob.glob("*.jpeg")
    for f in arquivos:
        if "alpha" in f.lower() or "iron" in f.lower():
            with open(f, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    return None

img_bg_base64 = obter_fundo_base64()

if img_bg_base64:
    css_bg = f'.stApp {{ background: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.92)), url("data:image/jpeg;base64,{img_bg_base64}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; color: #f0f2f6; }}' if img_bg_base64 else '.stApp { background-color: #0e1117; color: #f0f2f6; }'

st.markdown("""
    <style>
    """ + css_bg + """
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(14, 17, 23, 0.45) !important;
        backdrop-filter: blur(8px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3, h4 {
        color: #00E5FF !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(18, 20, 24, 0.85);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #22262d;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(26, 29, 36, 0.9);
        color: #9ca3af;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        border: none !important;
        outline: none !important;
    }
    .stTabs [data-baseweb="tab"]:focus {
        background-color: rgba(35, 39, 48, 0.95) !important;
        color: #00E5FF !important;
        box-shadow: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0051ff 0%, #00e5ff 100%) !important;
        color: #0e1117 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 229, 255, 0.3) !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
        background-color: transparent !important;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(22, 25, 32, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid #2a2f3a !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 5px rgba(0, 229, 255, 0.3) !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 24px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
    }
    table {
        background-color: rgba(22, 25, 32, 0.88) !important;
        border-radius: 8px;
        color: #e5e7eb !important;
    }
    th {
        background-color: rgba(31, 36, 45, 0.95) !important;
        color: #00E5FF !important;
    }
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

def encontrar_logo_sidebar():
    nomes_possiveis = ["Logo_e_mascote[1].png", "Logo_e_mascote.png", "logo.png", "Logo.png"]
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

AUTH_FILE = "usuarios_credenciais.json"

def carregar_credenciais():
    if os.path.exists(AUTH_FILE):
        try:
            with open(AUTH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"mikael": {"senha": "alpha2026", "nome": "Mikael Santos", "tipo": "admin", "db": "treinos_salvos_mikael.json"}}
    return {"mikael": {"senha": "alpha2026", "nome": "Mikael Santos", "tipo": "admin", "db": "treinos_salvos_mikael.json"}}

def salvar_credenciais(cred):
    try:
        with open(AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(cred, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

credenciais_sistema = carregar_credenciais()

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = ""

if not st.session_state.autenticado:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        carregar_logo_sidebar()
        st.markdown("<h2 style='text-align: center; color: #00E5FF;'>Alpha Iron Athletics</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af;'>Faça login para acessar o sistema</p>", unsafe_allow_html=True)
        
        with st.form("form_login"):
            username_input = st.text_input("Usuário")
            password_input = st.text_input("Senha", type="password")
            btn_login = st.form_submit_button("Entrar no Sistema", use_container_width=True)
            
            if btn_login:
                user_lower = username_input.strip().lower()
                if user_lower in credenciais_sistema and credenciais_sistema[user_lower]["senha"] == password_input:
                    st.session_state.autenticado = True
                    st.session_state.usuario_logado = user_lower
                    st.session_state.usuario_atual = credenciais_sistema[user_lower]["nome"]
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
    st.stop()

info_user = credenciais_sistema.get(st.session_state.usuario_logado, {"db": "treinos_salvos_mikael.json"})
DB_FILE = info_user.get("db", "treinos_salvos_mikael.json")

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

carregar_logo_sidebar()

st.sidebar.markdown("---")
st.sidebar.markdown(f"👤 Logado como: **{credenciais_sistema.get(st.session_state.usuario_logado, {}).get('nome', st.session_state.usuario_logado)}**")
if st.sidebar.button("Sair / Logout", key="btn_logout", use_container_width=True):
    st.session_state.autenticado = False
    st.session_state.usuario_logado = ""
    st.rerun()

if "menu_escolhido" not in st.session_state:
    st.session_state.menu_escolhido = "Início (Dashboard)"

opcoes_menu = [
    "Início (Dashboard)",
    "Programação Semanal",
    "🖥️ WOD TV (Para a TV)",
    "🧠 Coach Intelligence",
    "Montagem de Treinos",
    "Biblioteca de WODs",
    "Biblioteca de Exercícios",
    "Treinos Salvos",
    "🤖 Teste de Diagnóstico da IA",
    "Configurações"
]

st.sidebar.markdown("### Menu Principal")
for op in opcoes_menu:
    is_ativo = (st.session_state.menu_escolhido == op)
    if st.sidebar.button(op, key=f"menu_btn_{op}", use_container_width=True):
        st.session_state.menu_escolhido = op
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Periodização (Planilha 2.0)")
bloco = st.sidebar.selectbox("Periodization Phase", [
    "Block 1 - Strength Focus",
    "Block 2 - Engine Focus",
    "Block 3 - Gymnastics Focus",
    "Block 4 - Weightlifting Focus"
], key="sel_bloco_per")

semana = st.sidebar.selectbox("Periodization Week", [
    "Week 1 - Accumulation",
    "Week 2 - Progression",
    "Week 3 - Overload",
    "Week 4 - Deload / Benchmark"
], key="sel_semana_per")

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

def chamar_gemini_direto(prompt_texto):
    api_key = st.session_state.get("gemini_api_key", "")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            api_key = ""

    if not api_key:
        raise Exception("Chave da API do Gemini não configurada.")

    base_url = "https://generativelanguage.googleapis.com/v1beta"
    headers = {"Content-Type": "application/json"}

    list_url = f"{base_url}/models?key={api_key}"
    list_req = urllib.request.Request(list_url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(list_req, timeout=20) as response:
            modelos_json = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", errors="replace")
        raise Exception(f"Não foi possível listar modelos Gemini (HTTP {e.code}): {detalhe}")
    except Exception as e:
        raise Exception(f"Falha ao consultar modelos Gemini: {e}")

    modelos = [
        item.get("name", "")
        for item in modelos_json.get("models", [])
        if "generateContent" in item.get("supportedGenerationMethods", [])
        and item.get("name")
    ]
    if not modelos:
        raise Exception("A API não retornou modelos compatíveis com generateContent para esta chave.")

    def prioridade(nome):
        n = nome.lower()
        if "gemini-2.5-flash" in n:
            return (0, n)
        if "gemini-2.0-flash" in n:
            return (1, n)
        if "flash" in n:
            return (2, n)
        return (3, n)

    payload = {"contents": [{"parts": [{"text": prompt_texto}]}]}
    data = json.dumps(payload).encode("utf-8")
    erros = []

    for modelo in sorted(modelos, key=prioridade):
        url = f"{base_url}/{modelo}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                resultado = json.loads(response.read().decode("utf-8"))
            candidatos = resultado.get("candidates", [])
            if candidatos:
                partes = candidatos[0].get("content", {}).get("parts", [])
                texto = "".join(parte.get("text", "") for parte in partes if parte.get("text"))
                if texto:
                    return texto
            erros.append(f"{modelo}: resposta sem texto.")
        except urllib.error.HTTPError as e:
            detalhe = e.read().decode("utf-8", errors="replace")
            erros.append(f"{modelo}: HTTP {e.code}: {detalhe}")
        except Exception as e:
            erros.append(f"{modelo}: {e}")

    raise Exception("Nenhum modelo Gemini conseguiu responder. " + " | ".join(erros[:3]))

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

def gerar_sugestoes_com_ia(bloco_sel, semana_sel, dia_nome="", focus_dia="", treinos_Atuais_semana={}):
    try:
        prompt = f"""
        Você é o head coach especialista em periodização de CrossFit, LPO, HYROX, ATHX e MetCon da metodologia oficial Alpha Iron Athletics.
        CONTEXTO ATUAL DA PROGRAMAÇÃO:
        - Fase de Periodização: {bloco_sel}
        - Semana do Ciclo: {semana_sel}
        - Dia Sendo Montado: {dia_nome}
        - Foco Obrigatório do Dia: {focus_dia}
        
        Retorne APENAS um JSON estrito contendo uma lista de objetos com as chaves exatas "Session Block" e "Recommended Programming". Não coloque nenhum texto explicativo ou markdown fora do JSON.
        """
        txt_resp = chamar_gemini_direto(prompt)
        txt = txt_resp.strip()
        if txt.startswith("```json"):
            txt = txt[7:]
        if txt.endswith("```"):
            txt = txt[:-3]
        parsed = json.loads(txt.strip())
        return pd.DataFrame(parsed)
    except Exception as e:
        return pd.DataFrame({
            "Session Block": ["Erro na Integração IA", "Detalhe Técnico"],
            "Recommended Programming": ["Não foi possível conectar ao Gemini via API.", str(e)]
        })

dias_semana = [
    {"day": "Monday", "focus": "HYROX"},
    {"day": "Tuesday", "focus": "CrossFit - Strength / LPO (Snatch Focus)"},
    {"day": "Wednesday", "focus": "CrossFit - Gymnastics Progressivo"},
    {"day": "Thursday", "focus": "CrossFit - Strength / LPO (Clean Focus)"},
    {"day": "Friday", "focus": "ATHX / GHX"},
    {"day": "Saturday", "focus": "Community WOD"},
    {"day": "Sunday", "focus": "Benchmark / Hero WOD"}
]

treinos_salvos = carregar_treinos_salvos()

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

elif st.session_state.menu_escolhido == "🖥️ WOD TV (Para a TV)":
    st.title("🖥️ WOD TV — Tela para a TV do Box (LG 42LN5700)")
    st.markdown("Como o sistema está na nuvem, basta abrir o link especial abaixo diretamente no navegador da TV para exibir os treinos em tela cheia na parede!")
    
    link_tv_nuvem = "https://mikaelsjeronimo-dotcom-alpha-iron-athletic--app-d1qo92.streamlit.app/?modo=tv"
    st.success(f"📺 **Link Direto para a TV:** `{link_tv_nuvem}`")
    st.markdown("Basta digitar esse link exato no navegador da TV (com `?modo=tv` no final) para abrir o painel limpo, com detecção automática do dia de hoje e em tela cheia!")

elif st.session_state.menu_escolhido == "🧠 Coach Intelligence":
    st.title("🧠 Coach Intelligence")
    st.markdown("Painel de apoio à decisão para revisar a programação salva. Ele não altera nem gera treinos automaticamente.")
    st.caption(f"Análise da programação salva • {bloco} • {semana}")

    if not treinos_salvos:
        st.info("Ainda não há treinos salvos para analisar. Monte e salve a programação na aba Montagem de Treinos.")
    else:
        dias_analise = [
            ("Monday", "Segunda-feira", "HYROX"),
            ("Tuesday", "Terça-feira", "Força / LPO"),
            ("Wednesday", "Quarta-feira", "Ginástica"),
            ("Thursday", "Quinta-feira", "Foco configurado"),
            ("Friday", "Sexta-feira", "ATHX"),
            ("Saturday", "Sábado", "Community WOD"),
            ("Sunday", "Domingo", "CrossFit / Benchmark")
        ]
        movimentos = {
            "Squat": ["squat", "agach", "wall ball", "wallball", "thruster", "lunge", "pistol"],
            "Hinge": ["deadlift", "terra", "hinge", "swing", "clean", "snatch", "rdl", "good morning"],
            "Push": ["push", "press", "jerk", "hspu", "dip", "bench", "supino", "flexão", "flexao", "thruster"],
            "Pull": ["pull-up", "pullup", "pull up", "chest to bar", "c2b", "row", "remada", "rope climb", "muscle-up", "muscle up"],
            "Core": ["toes to bar", "ttb", "sit-up", "sit up", "hollow", "plank", "prancha", "v-up", "l-sit"],
            "Snatch": ["snatch", "arranco"],
            "Clean & Jerk": ["clean & jerk", "clean and jerk", "clean", "jerk", "arremesso"],
            "Run / Engine": ["run", "corrida", "row", "rowing", "ski", "bike", "assault bike", "burpee"]
        }
        linhas_dias = []
        volume_semana = {k: 0 for k in movimentos}
        exercicios_por_dia = {}
        for dia, nome_pt, foco in dias_analise:
            blocos = []
            for sufixo, rotulo in [("w", "Warm-Up"), ("s", "Strength"), ("l", "Skill"), ("e", "Endurance"), ("m", "WOD"), ("a", "Accessory"), ("r", "Mobility")]:
                texto_bloco = str(treinos_salvos.get(f"{dia}_{sufixo}", "") or "").strip()
                if texto_bloco:
                    blocos.append((rotulo, texto_bloco))
            texto_dia = "\n".join(t for _, t in blocos)
            exercicios_por_dia[dia] = texto_dia
            if texto_dia:
                capacidades = [nome for nome, termos in movimentos.items() if any(termo in texto_dia.lower() for termo in termos)]
                for cap in capacidades:
                    volume_semana[cap] += sum(texto_dia.lower().count(termo) for termo in movimentos[cap])
                minutos = 0
                for sufixo in ["w", "s", "l", "e", "m", "a", "r"]:
                    try:
                        minutos += int(float(treinos_salvos.get(f"{dia}_t_{sufixo}", 0) or 0))
                    except (ValueError, TypeError):
                        pass
                linhas_dias.append({"Dia": nome_pt, "Foco": foco, "Blocos preenchidos": len(blocos), "Tempo planejado (min)": minutos, "Estímulos identificados": ", ".join(capacidades) if capacidades else "Não identificados"})

        preenchidos = len(linhas_dias)
        tempo_total = sum(l["Tempo planejado (min)"] for l in linhas_dias)
        c1, c2, c3 = st.columns(3)
        c1.metric("Dias com programação", f"{preenchidos}/7")
        c2.metric("Tempo semanal planejado", f"{tempo_total} min")
        c3.metric("Fase analisada", bloco.split(" - ", 1)[-1])

        st.subheader("Visão geral da semana")
        if linhas_dias:
            st.dataframe(pd.DataFrame(linhas_dias), use_container_width=True, hide_index=True)
        else:
            st.warning("Foram encontrados dados salvos, mas nenhum bloco de treino preenchido nos dias esperados.")

        st.subheader("Distribuição de estímulos detectados")
        dados_estimulos = pd.DataFrame([{"Estímulo": k, "Menções nos treinos": v} for k, v in volume_semana.items()])
        dados_estimulos = dados_estimulos.sort_values("Menções nos treinos", ascending=False)
        st.bar_chart(dados_estimulos.set_index("Estímulo"))

        st.subheader("Alertas para revisão do coach")
        alertas = []
        if preenchidos < 7:
            alertas.append(("info", f"Há programação identificada em {preenchidos} de 7 dias. Confirme se os dias vazios são intencionais."))
        if tempo_total > 420:
            alertas.append(("warning", f"O tempo semanal somado é de {tempo_total} minutos."))
        elif tempo_total and tempo_total < 180:
            alertas.append(("info", f"O tempo semanal registrado é de {tempo_total} minutos."))
        if not alertas:
            alertas.append(("success", "Nenhum alerta básico foi acionado."))
        for tipo, mensagem in alertas:
            if tipo == "warning": st.warning(mensagem)
            elif tipo == "info": st.info(mensagem)
            else: st.success(mensagem)

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
        r_txt = treinos_salvos.get(f"{d_name}_r", "Não cadastrado")
        
        st.markdown(f"**2. Strength ({s_t} min):**")
        st.code(s_txt, language="text")
        st.markdown(f"**3. Skill ({l_t} min):**")
        st.code(l_txt, language="text")
        st.markdown(f"**4. WOD ({m_t} min):**")
        st.code(m_txt, language="text")
        st.markdown(f"**5. Accessory ({a_t} min):**")
        st.code(a_txt, language="text")
        st.markdown(f"**6. Mobility ({r_t} min):**")
        st.code(r_txt, language="text")
    else:
        st.markdown(f"**Main Block / MetCon ({m_t} min):**")
        st.code(m_txt, language="text")

elif st.session_state.menu_escolhido == "Montagem de Treinos":
    st.title("Alpha Iron 2.0 — Workout Builder & Editor")
    st.markdown("Monte e ajuste os blocos diários com salvamento automático e controle de volume (Otimizado para máxima velocidade).")
    
    tabs = st.tabs([d["day"] for d in dias_semana])
    lista_blocos_semana_acumulados = []
    dados_para_salvar = {}

    for i, tab in enumerate(tabs):
        day_info = dias_semana[i]
        day_name = day_info["day"]
        day_focus = day_info["focus"]
        
        with tab:
            st.subheader(f"{day_name} — {day_focus}")
            
            with st.expander("Ferramenta de Duplicação Rápida"):
                col_dup1, col_dup2 = st.columns([2, 1])
                with col_dup1:
                    dia_destino = st.selectbox("Copiar programação deste dia para:", [d["day"] for d in dias_semana if d["day"] != day_name], key=f"dup_sel_{i}")
                with col_dup2:
                    if st.button("Duplicar Agora", key=f"btn_dup_{i}"):
                        treinos_salvos[f"{dia_destino}_t_w"] = treinos_salvos.get(f"{day_name}_t_w", 10)
                        treinos_salvos[f"{dia_destino}_w"] = treinos_salvos.get(f"{day_name}_w", "")
                        treinos_salvos[f"{dia_destino}_t_m"] = treinos_salvos.get(f"{day_name}_t_m", 15)
                        treinos_salvos[f"{dia_destino}_m"] = treinos_salvos.get(f"{day_name}_m", "")
                        salvar_treinos_disco(treinos_salvos)
                        st.success(f"Treino duplicado com sucesso para {dia_destino}!")
            
            col1, col2 = st.columns([1.3, 1])
            lista_blocos_do_dia = []
            m_input_atual = ""
            
            with col1:
                st.markdown("### Session Structure (60 min)")
                t_s, t_m = 0, 0
                
                if day_name == "Monday":
                    st.info("HYROX Session: Running + Functional Stations")
                    c1, c2 = st.columns([1, 4])
                    with c1: t_w = st.text_input("Warm (min)", value=str(treinos_salvos.get(f"{day_name}_t_w", "10")), key=f"t_hy_w_{i}")
                    with c2: w_input = st.text_area("Warm-Up Descrição", treinos_salvos.get(f"{day_name}_w", "Dynamic Mobility"), height=75, key=f"hy_w_{i}")
                    
                    c3, c4 = st.columns([1, 4])
                    with c3: t_m = st.text_input("Main (min)", value=str(treinos_salvos.get(f"{day_name}_t_m", "40")), key=f"t_hy_m_{i}")
                    with c4: m_input_atual = st.text_area("HYROX Main Block", treinos_salvos.get(f"{day_name}_m", "Running + Stations"), height=110, key=f"hy_m_{i}")
                    
                    c5, c6 = st.columns([1, 4])
                    with c5: t_r = st.text_input("Mob (min)", value=str(treinos_salvos.get(f"{day_name}_t_r", "10")), key=f"t_hy_r_{i}")
                    with c6: r_input = st.text_area("Mobility Descrição", treinos_salvos.get(f"{day_name}_r", "Stretching"), height=75, key=f"hy_r_{i}")
                    
                    tw_val = int(t_w) if t_w.isdigit() else 0
                    tm_val = int(t_m) if t_m.isdigit() else 0
                    tr_val = int(t_r) if t_r.isdigit() else 0
                    total_time = tw_val + tm_val + tr_val

                    lista_blocos_do_dia = [{"texto": w_input, "tempo": tw_val}, {"texto": m_input_atual, "tempo": tm_val}]
                    dados_para_salvar.update({f"{day_name}_t_w": tw_val, f"{day_name}_w": w_input, f"{day_name}_t_m": tm_val, f"{day_name}_m": m_input_atual, f"{day_name}_t_r": tr_val, f"{day_name}_r": r_input})

                elif day_name == "Friday":
                    st.info("ATHX Session: Fixed Structure")
                    c1, c2 = st.columns([1, 4])
                    with c1: t_w = st.text_input("Warm (min)", value=str(treinos_salvos.get(f"{day_name}_t_w", "10")), key=f"t_athx_w_{i}")
                    with c2: w_input = st.text_area("Warm-Up Descrição", treinos_salvos.get(f"{day_name}_w", "Dynamic"), height=75, key=f"athx_w_{i}")

                    c3, c4 = st.columns([1, 4])
                    with c3: t_s = st.text_input("Str (min)", value=str(treinos_salvos.get(f"{day_name}_t_s", "15")), key=f"t_athx_s_{i}")
                    with c4: s_input = st.text_area("Strength Max Descrição", treinos_salvos.get(f"{day_name}_s", ""), height=75, key=f"athx_s_{i}")

                    c5, c6 = st.columns([1, 4])
                    with c5: t_e = st.text_input("End (min)", value=str(treinos_salvos.get(f"{day_name}_t_e", "15")), key=f"t_athx_e_{i}")
                    with c6: l_input = st.text_area("Endurance Descrição", treinos_salvos.get(f"{day_name}_e", ""), height=75, key=f"athx_e_{i}")

                    c7, c8 = st.columns([1, 4])
                    with c7: t_m = st.text_input("WOD (min)", value=str(treinos_salvos.get(f"{day_name}_t_m", "15")), key=f"t_athx_m_{i}")
                    with c8: m_input_atual = st.text_area("MetCon X Descrição", treinos_salvos.get(f"{day_name}_m", ""), height=90, key=f"athx_m_{i}")

                    c9, c10 = st.columns([1, 4])
                    with c9: t_r = st.text_input("Mob (min)", value=str(treinos_salvos.get(f"{day_name}_t_r", "5")), key=f"t_athx_r_{i}")
                    with c10: r_input = st.text_area("Mobility Descrição", treinos_salvos.get(f"{day_name}_r", "Stretching"), height=75, key=f"athx_r_{i}")

                    tw_val = int(t_w) if t_w.isdigit() else 0
                    ts_val = int(t_s) if t_s.isdigit() else 0
                    te_val = int(t_e) if t_e.isdigit() else 0
                    tm_val = int(t_m) if t_m.isdigit() else 0
                    tr_val = int(t_r) if t_r.isdigit() else 0
                    total_time = tw_val + ts_val + te_val + tm_val + tr_val

                    lista_blocos_do_dia = [{"texto": w_input, "tempo": tw_val}, {"texto": s_input, "tempo": ts_val}, {"texto": l_input, "tempo": te_val}, {"texto": m_input_atual, "tempo": tm_val}]
                    dados_para_salvar.update({f"{day_name}_t_w": tw_val, f"{day_name}_w": w_input, f"{day_name}_t_s": ts_val, f"{day_name}_s": s_input, f"{day_name}_t_e": te_val, f"{day_name}_e": l_input, f"{day_name}_t_m": tm_val, f"{day_name}_m": m_input_atual, f"{day_name}_t_r": tr_val, f"{day_name}_r": r_input})

                else:
                    c1, c2 = st.columns([1, 4])
                    with c1: t_w = st.text_input("Warm (min)", value=str(treinos_salvos.get(f"{day_name}_t_w", "10")), key=f"t_cf_w_{i}")
                    with c2: w_input = st.text_area("1. Warm-Up", treinos_salvos.get(f"{day_name}_w", ""), height=75, key=f"cf_w_{i}")

                    c3, c4 = st.columns([1, 4])
                    with c3: t_s = st.text_input("Str (min)", value=str(treinos_salvos.get(f"{day_name}_t_s", "15")), key=f"t_cf_s_{i}")
                    with c4: s_input = st.text_area("2. Strength", treinos_salvos.get(f"{day_name}_s", ""), height=75, key=f"cf_s_{i}")

                    c5, c6 = st.columns([1, 4])
                    with c5: t_l = st.text_input("Skill (min)", value=str(treinos_salvos.get(f"{day_name}_t_l", "10")), key=f"t_cf_l_{i}")
                    with c6: l_input = st.text_area("3. Skill", treinos_salvos.get(f"{day_name}_l", ""), height=75, key=f"cf_l_{i}")

                    c7, c8 = st.columns([1, 4])
                    with c7: t_m = st.text_input("WOD (min)", value=str(treinos_salvos.get(f"{day_name}_t_m", "15")), key=f"t_cf_m_{i}")
                    with c8: m_input_atual = st.text_area("4. WOD", treinos_salvos.get(f"{day_name}_m", ""), height=90, key=f"cf_wod_{i}")

                    c9, c10 = st.columns([1, 4])
                    with c9: t_a = st.text_input("Acc (min)", value=str(treinos_salvos.get(f"{day_name}_t_a", "5")), key=f"t_cf_a_{i}")
                    with c10: a_input = st.text_area("5. Accessory", treinos_salvos.get(f"{day_name}_a", ""), height=75, key=f"cf_a_{i}")

                    c11, c12 = st.columns([1, 4])
                    with c11: t_r = st.text_input("Mob (min)", value=str(treinos_salvos.get(f"{day_name}_t_r", "5")), key=f"t_cf_r_{i}")
                    with c12: r_input = st.text_area("6. Mobility", treinos_salvos.get(f"{day_name}_r", ""), height=75, key=f"cf_m_{i}")

                    tw_val = int(t_w) if t_w.isdigit() else 0
                    ts_val = int(t_s) if t_s.isdigit() else 0
                    tl_val = int(t_l) if t_l.isdigit() else 0
                    tm_val = int(t_m) if t_m.isdigit() else 0
                    ta_val = int(t_a) if t_a.isdigit() else 0
                    tr_val = int(t_r) if t_r.isdigit() else 0
                    
                    total_time = tw_val + ts_val + tl_val + tm_val + ta_val + tr_val

                    lista_blocos_do_dia = [
                        {"texto": w_input, "tempo": tw_val}, {"texto": s_input, "tempo": ts_val},
                        {"texto": l_input, "tempo": tl_val}, {"texto": m_input_atual, "tempo": tm_val},
                        {"texto": a_input, "tempo": ta_val}
                    ]
                    
                    dados_para_salvar.update({
                        f"{day_name}_t_w": tw_val, f"{day_name}_w": w_input,
                        f"{day_name}_t_s": ts_val, f"{day_name}_s": s_input,
                        f"{day_name}_t_l": tl_val, f"{day_name}_l": l_input,
                        f"{day_name}_t_m": tm_val, f"{day_name}_m": m_input_atual,
                        f"{day_name}_t_a": ta_val, f"{day_name}_a": a_input,
                        f"{day_name}_t_r": tr_val, f"{day_name}_r": r_input
                    })

                lista_blocos_semana_acumulados.extend(lista_blocos_do_dia)

                vol_dia = extrair_volume_acumulado_estruturado(lista_blocos_do_dia)
                eh_especial = ("HYROX" in day_focus or "ATHX" in day_focus)
                iacs_dia = calcular_iacs_de_vol(vol_dia, eh_especial)
                
                tm_wod_val = int(t_m) if 't_m' in locals() and str(t_m).isdigit() else 15
                alpha_wod_score = calcular_alpha_wod_load(m_input_atual, tm_wod_val)

                st.markdown("---")
                col_metric1, col_metric2 = st.columns(2)
                
                with col_metric1:
                    if total_time > 60:
                        st.warning(f"Duration: {total_time} min / 60 min")
                    else:
                        st.success(f"Duration: {total_time} min / 60 min")

                with col_metric2:
                    st.info(f"Daily Alpha Load (IACS): {iacs_dia} pts")
                    st.success(f"Alpha WOD Load: {alpha_wod_score} pts")

            with col2:
                st.markdown("### Scaling Chart (RX / INT / BEG / MASTERS)")
                escala_df = pd.DataFrame({
                    "Level": ["RX", "Intermediate", "Beginner", "Masters"],
                    "Load / Category": ["100% RX Load", "70-80% Load", "50% Load / Dumbbells", "Custom Scaling"],
                    "Gymnastics": ["Full Movement", "Medium Progression", "Basic Scale", "Range Focus"]
                })
                st.table(escala_df)
                
                st.markdown(f"### Intelligence Suggestions ({day_name})")
                st.caption("As sugestões de IA agora são carregadas sob demanda para garantir máxima velocidade e eliminar a lentidão.")
                
                key_sugestao_ia = f"sugestoes_ia_{day_name}"
                if key_sugestao_ia not in st.session_state:
                    st.session_state[key_sugestao_ia] = None

                if st.button(f"🤖 Gerar Sugestões via IA ({day_name})", key=f"btn_ia_{i}._otimizado"):
                    with st.spinner("Consultando o Coach Intelligence..."):
                        st.session_state[key_sugestao_ia] = gerar_sugestoes_com_ia(bloco, semana, day_name, day_focus, treinos_salvos)

                if st.session_state[key_sugestao_ia] is not None:
                    st.table(st.session_state[key_sugestao_ia])
                else:
                    st.info("Clique no botão acima para carregar as sugestões de IA para este dia.")
                
                st.markdown("---")
                st.markdown("### Validation Checklist")
                st.checkbox("Session objective clearly defined?", value=True, key=f"chk1_{i}")
                st.checkbox("Dominant movement pattern respected?", value=True, key=f"chk2_{i}")
                st.checkbox("Session within 60 minutes time cap?", value=True, key=f"chk3_{i}")
                st.checkbox("Scaling options available for all levels?", value=True, key=f"chk4_{i}")

    salvar_treinos_disco(dados_para_salvar)

elif st.session_state.menu_escolhido == "🤖 Teste de Diagnóstico da IA":
    st.title("🤖 Painel de Diagnóstico Direto da IA (Gemini API)")
    st.markdown("Envie qualquer mensagem ou comando de teste abaixo para verificar instantaneamente se a API está conectada e respondendo.")
    
    api_key_status = st.session_state.get("gemini_api_key", "")
    if not api_key_status and "GEMINI_API_KEY" in st.secrets:
        api_key_status = "Configurada via st.secrets"
    
    if api_key_status:
        st.success("✅ Chave da API detectada no sistema!")
    else:
        st.error("❌ Chave da API NÃO encontrada! Configure na aba Configurações ou nos Secrets.")

    mensagem_teste = st.text_input("Mensagem de Teste para o Gemini", value="Olá Gemini, você está operando na Alpha Iron Athletics?")
    
    if st.button("Enviar Mensagem de Teste"):
        if not api_key_status:
            st.error("Insira a chave da API primeiro.")
        else:
            with st.spinner("Conectando com o Gemini..."):
                try:
                    resposta_ia = chamar_gemini_direto(mensagem_teste)
                    st.success("🎉 Resposta recebida com sucesso da API!")
                    st.markdown("### Resposta do Gemini:")
                    st.info(resposta_ia)
                except Exception as e:
                    st.error(f"❌ Erro ao comunicar com a API do Gemini:")
                    st.code(str(e), language="text")

elif st.session_state.menu_escolhido == "Biblioteca de WODs":
    st.title("Biblioteca de WODs Alpha — Benchmarks Oficiais")
    st.markdown("Clique em qualquer Benchmark abaixo para expandir, visualizar e **editar** o treino completo, tipo e movimentos conforme sua preferência.")
    
    if "benchmarks_editaveis" not in st.session_state:
        st.session_state.benchmarks_editaveis = {
            "The Girls": [
                {"Nome": "Fran", "Tipo": "For Time (21-15-9)", "Movimentos": "21-15-9 reps: Thrusters (95/65 lbs) + Pull-ups"},
                {"Nome": "Diane", "Tipo": "For Time (21-15-9)", "Movimentos": "21-15-9 reps: Deadlifts (225/155 lbs) + Handstand Push-ups"},
                {"Nome": "Elizabeth", "Tipo": "For Time (21-15-9)", "Movimentos": "21-15-9 reps: Cleans (135/95 lbs) + Ring Dips"},
                {"Nome": "Barbara", "Tipo": "5 Rounds For Time (Rest 3:00)", "Movimentos": "5 Rounds (rest 3 min): 20 Pull-ups + 30 Push-ups + 40 Sit-ups + 50 Air Squats"},
                {"Nome": "Chelsea", "Tipo": "EMOM 30 min", "Movimentos": "EMOM 30 min: 5 Pull-ups + 10 Push-ups + 15 Air Squats"},
                {"Nome": "Angie", "Tipo": "For Time", "Movimentos": "For Time: 100 Pull-ups + 100 Push-ups + 100 Sit-ups + 100 Air Squats"},
                {"Nome": "Cindy", "Tipo": "AMRAP 20 min", "Movimentos": "AMRAP 20 min: 5 Pull-ups + 10 Push-ups + 15 Air Squats"},
                {"Nome": "Helen", "Tipo": "3 Rounds For Time", "Movimentos": "3 Rounds For Time: 400m Run + 21 KB Swings (24/16 kg) + 12 Pull-ups"},
                {"Nome": "Karen", "Tipo": "For Time (150 Reps)", "Movimentos": "For Time: 150 Wall Ball Shots (20/14 lbs)"},
                {"Nome": "Nancy", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 400m Run + 15 Overhead Squats (95/65 lbs)"},
                {"Nome": "Eva", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 800m Run + 30 KB Swings (32/24 kg) + 30 Pull-ups"},
                {"Nome": "Kelly", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 400m Run + 30 Box Jumps + 30 Wall Balls"},
                {"Nome": "Annie", "Tipo": "For Time (50-40-30-20-10)", "Movimentos": "50-40-30-20-10 reps For Time: Double-Unders + AbMat Sit-ups"},
                {"Nome": "Nicole", "Tipo": "AMRAP 20 min", "Movimentos": "AMRAP 20 min: 400m Run + Max Reps Pull-ups"},
                {"Nome": "Lynne", "Tipo": "5 Rounds For Max Reps", "Movimentos": "5 Rounds For Max Reps: Max Bench Press + Max Pull-ups"},
                {"Nome": "Maggie", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 20 HSPU + 40 Pull-ups + 50 Air Squats"},
                {"Nome": "Grettel", "Tipo": "10 Rounds For Time", "Movimentos": "10 Rounds For Time: 3 Clean & Jerks (135/95 lbs) + 3 Bar-Facing Burpees"},
                {"Nome": "Lulu", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 10 Pull-ups + 15 Push-ups + 20 Air Squats"},
                {"Nome": "Gus", "Tipo": "For Time", "Movimentos": "For Time: 2000m Row + 50 Push-ups"},
                {"Nome": "Roxanne", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 7 Pull-ups + 7 Burpees + 7 Snatches (95/65 lbs)"}
            ],
            "Weightlifting & Engine": [
                {"Nome": "Isabel", "Tipo": "For Time (30 Reps)", "Movimentos": "For Time: 30 Power Snatches (135/95 lbs)"},
                {"Nome": "Grace", "Tipo": "For Time (30 Reps)", "Movimentos": "For Time: 30 Clean & Jerks (135/95 lbs)"},
                {"Nome": "Jackie", "Tipo": "For Time", "Movimentos": "For Time: 1000m Row + 50 Thrusters + 30 Pull-ups"},
                {"Nome": "Amanda", "Tipo": "For Time (9-7-5)", "Movimentos": "9-7-5 reps For Time: Muscle-ups + Snatches (135/95 lbs)"},
                {"Nome": "Mary", "Tipo": "AMRAP 20 min", "Movimentos": "AMRAP 20 min: 5 Handstand Push-ups + 10 Pistols + 15 Pull-ups"},
                {"Nome": "Nate", "Tipo": "AMRAP 20 min", "Movimentos": "AMRAP 20 min: 2 Muscle-ups + 4 HSPU + 8 KB Swings (32/24 kg)"},
                {"Nome": "Wrangler", "Tipo": "For Time", "Movimentos": "For Time: 30 Clean & Jerks (225/145 lbs)"},
                {"Nome": "Cynthia", "Tipo": "AMRAP 20 min", "Movimentos": "AMRAP 20 min: 10 Pull-ups + 20 Push-ups + 30 Air Squats"}
            ],
            "Hero WODs": [
                {"Nome": "Murph", "Tipo": "For Time", "Movimentos": "For Time: 1 Mile Run + 100 Pull-ups + 200 Push-ups + 300 Air Squats + 1 Mile Run"},
                {"Nome": "DT", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 12 Deadlifts + 9 Hang Power Cleans + 6 Push Jerks (155/105 lbs)"},
                {"Nome": "Kalsu", "Tipo": "For Time (EMOM Thrusters)", "Movimentos": "For Time: 100 Thrusters (135/95 lbs) with EMOM 5 Burpees"},
                {"Nome": "Randy", "Tipo": "For Time (75 Reps)", "Movimentos": "For Time: 75 Power Snatches (75/55 lbs)"},
                {"Nome": "J.T.", "Tipo": "21-15-9 For Time", "Movimentos": "21-15-9 For Time: Handstand Push-ups + Ring Dips + Push-ups"},
                {"Nome": "Michael", "Tipo": "3 Rounds For Time", "Movimentos": "3 Rounds For Time: 800m Run + 50 Back Extensions + 50 Sit-ups"},
                {"Nome": "Daniel", "Tipo": "For Time", "Movimentos": "For Time: 50 Pull-ups + 400m Run + 21 Thrusters + 800m Run + 21 Thrusters + 400m Run + 50 Pull-ups"},
                {"Nome": "Jason", "Tipo": "For Time", "Movimentos": "For Time: 100 Squats + 5 Muscle-ups"},
                {"Nome": "Josh", "Tipo": "For Time", "Movimentos": "For Time: 21 OHS + 42 Pull-ups + 15 OHS + 30 Pull-ups + 9 OHS + 18 Pull-ups"},
                {"Nome": "Badger", "Tipo": "3 Rounds For Time", "Movimentos": "3 Rounds For Time: 30 Squat Cleans (95/65 lbs) + 30 Pull-ups + 800m Run"},
                {"Nome": "Bull", "Tipo": "2 Rounds For Time", "Movimentos": "2 Rounds For Time: 2 Mile Run + 50 Pull-ups + 50 Push-ups + 50 Bodyweight Squats"},
                {"Nome": "Holleyman", "Tipo": "30 Rounds For Time", "Movimentos": "30 Rounds For Time: 5 Wall Balls + 3 HSPU + 1 Power Clean (225/155 lbs)"},
                {"Nome": "Luce", "Tipo": "3 Rounds For Time", "Movimentos": "3 Rounds For Time: 1000m Run + 10 Ring Muscle-ups + 100 Air Squats"},
                {"Nome": "Roy", "Tipo": "5 Rounds For Time", "Movimentos": "5 Rounds For Time: 15 Deadlifts (225/155 lbs) + 20 Box Jumps + 25 Pull-ups"},
                {"Nome": "Coffland", "Tipo": "For Time / Complex", "Movimentos": "For Time (6 min cap): Complex of Deadlift + Clean & Jerk + Sled Push"},
                {"Nome": "McCluskey", "Tipo": "For Time", "Movimentos": "For Time: Run + Burpees + Heavy Kettlebell Swings"},
                {"Nome": "Rankel", "Tipo": "For Time", "Movimentos": "For Time: Run + Heavy Deadlifts + Burpee Pull-ups"}
            ]
        }
    
    categoria_escolhida = st.selectbox("Filtrar por Categoria", ["Todas as Categorias", "The Girls", "Weightlifting & Engine", "Hero WODs"])
    
    for cat, lista in st.session_state.benchmarks_editaveis.items():
        if categoria_escolhida != "Todas as Categorias" and categoria_escolhida != cat:
            continue
            
        st.markdown(f"### {cat}")
        for idx, wod in enumerate(lista):
            with st.expander(f"{wod['Nome']} — [{wod['Tipo']}]"):
                modo_edicao = st.checkbox("Editar este WOD", key=f"chk_edit_{cat}_{idx}")
                if modo_edicao:
                    with st.form(key=f"form_wods_{cat}_{idx}"):
                        novo_tipo = st.text_input("Tipo / Formato do WOD", value=wod['Tipo'], key=f"t_{cat}_{idx}")
                        novos_movimentos = st.text_area("Descrição e Movimentos", value=wod['Movimentos'], height=120, key=f"m_{cat}_{idx}")
                        if st.form_submit_button("Salvar Alterações"):
                            st.session_state.benchmarks_editaveis[cat][idx]["Tipo"] = novo_tipo
                            st.session_state.benchmarks_editaveis[cat][idx]["Movimentos"] = novos_movimentos
                            st.success("Atualizado com sucesso!")
                            st.rerun()
                else:
                    st.markdown(f"**Tipo de WOD:** {wod['Tipo']}")
                    st.markdown(f"**Descrição Oficial e Movimentos:**")
                    st.code(wod['Movimentos'], language="text")

elif st.session_state.menu_escolhido == "Biblioteca de Exercícios":
    st.title("Biblioteca de Exercícios & Padrões")
    st.markdown("Consulta e gerenciamento dos padrões de movimento monitorados pelo IACS (MCVS). Você pode editar, adicionar ou remover exercícios livremente.")
    
    if "exercicios_editaveis" not in st.session_state:
        st.session_state.exercicios_editaveis = [
            {"Padrão": "Squat", "Exercícios Principais": "Back Squat, Front Squat, OHS, Wall Ball, Thruster, Lunges"},
            {"Padrão": "Hinge", "Exercícios Principais": "Deadlift, RDL, Power Clean, Squat Clean, Snatch, KB Swing"},
            {"Padrão": "Push", "Exercícios Principais": "Strict Press, Push Press, HSPU, Bench Press, Push-ups"},
            {"Padrão": "Pull", "Exercícios Principais": "Pull-ups, Chest-to-Bar, Bar Muscle-Up, Row, Rope Climb"},
            {"Padrão": "Core", "Exercícios Principais": "Toes-to-Bar, Sit-ups, V-ups, Hollow Hold, Planks"}
        ]
    
    with st.expander("➕ Adicionar Novo Padrão / Exercício"):
        with st.form("form_novo_exercicio"):
            novo_padrao = st.text_input("Nome do Padrão (ex: Squat, Hinge, etc.)")
            novos_itens = st.text_area("Exercícios Principais (separados por vírgula)")
            if st.form_submit_button("Cadastrar Padrão"):
                if novo_padrao.strip():
                    st.session_state.exercicios_editaveis.append({
                        "Padrão": novo_padrao.strip(),
                        "Exercícios Principais": novos_itens.strip()
                    })
                    st.success("Novo padrão adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("O nome do padrão não pode estar vazio.")

    st.markdown("---")
    st.subheader("Padrões Cadastrados (Editáveis)")
    
    for idx, ex in enumerate(st.session_state.exercicios_editaveis):
        with st.expander(f"✏️ {ex['Padrão']} — [{ex['Exercícios Principais'][:40]}...]"):
            with st.form(key=f"form_edit_ex_{idx}"):
                p_nome = st.text_input("Nome do Padrão", value=ex["Padrão"], key=f"p_nome_{idx}")
                p_itens = st.text_area("Exercícios Principais", value=ex["Exercícios Principais"], key=f"p_itens_{idx}")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    salvar = st.form_submit_button("Salvar Alterações")
                with col_btn2:
                    remover = st.form_submit_button("🗑️ Excluir Padrão")
                
                if salvar:
                    st.session_state.exercicios_editaveis[idx]["Padrão"] = p_nome
                    st.session_state.exercicios_editaveis[idx]["Exercícios Principais"] = p_itens
                    st.success("Alterações salvas com sucesso!")
                    st.rerun()
                if remover:
                    st.session_state.exercicios_editaveis.pop(idx)
                    st.success("Padrão removido com sucesso!")
                    st.rerun()

elif st.session_state.menu_escolhido == "Treinos Salvos":
    st.title("Histórico de Treinos Salvos")
    st.markdown("Visualize os treinos programados e salvos de forma organizada e limpa, exatamente igual à Biblioteca de WODs. Clique em qualquer dia para expandir os blocos.")
    
    if not treinos_salvos:
        st.info("Nenhum treino salvo no momento. Utilize a aba de Montagem de Treinos para registrar dados.")
    else:
        dias_traducao = {
            "Monday": "Segunda-feira (HYROX)",
            "Tuesday": "Terça-feira (CrossFit - Strength / LPO)",
            "Wednesday": "Quarta-feira (CrossFit - Gymnastics)",
            "Thursday": "Quinta-feira (CrossFit - Strength / LPO)",
            "Friday": "Sexta-feira (ATHX)",
            "Saturday": "Sábado (Community WOD)",
            "Sunday": "Domingo (Benchmark / Hero)"
        }
        dias_encontrados = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for d in dias_encontrados:
            nome_amigavel = dias_traducao.get(d, d)
            chaves_dia = [k for k in treinos_salvos.keys() if k.startswith(d)]
            if not chaves_dia:
                continue
                
            w_t = treinos_salvos.get(f"{d}_t_w", 0)
            w_txt = treinos_salvos.get(f"{d}_w", "")
            s_t = treinos_salvos.get(f"{d}_t_s", 0)
            s_txt = treinos_salvos.get(f"{d}_s", "")
            l_t = treinos_salvos.get(f"{d}_t_l", 0)
            l_txt = treinos_salvos.get(f"{d}_l", "")
            m_t = treinos_salvos.get(f"{d}_t_m", 0)
            m_txt = treinos_salvos.get(f"{d}_m", "")
            a_t = treinos_salvos.get(f"{d}_t_a", 0)
            a_txt = treinos_salvos.get(f"{d}_a", "")
            r_t = treinos_salvos.get(f"{d}_t_r", 0)
            r_txt = treinos_salvos.get(f"{d}_r", "")
            e_t = treinos_salvos.get(f"{d}_t_e", 0)
            e_txt = treinos_salvos.get(f"{d}_e", "")
            
            if not any([w_txt, s_txt, l_txt, m_txt, a_txt, r_txt, e_txt]):
                continue
                
            with st.expander(f"📅 {nome_amigavel}"):
                if w_txt:
                    st.markdown(f"**1. Warm-Up ({w_t} min):**")
                    st.code(w_txt, language="text")
                if s_txt:
                    st.markdown(f"**2. Strength ({s_t} min):**")
                    st.code(s_txt, language="text")
                if l_txt:
                    st.markdown(f"**3. Skill ({l_t} min):**")
                    st.code(l_txt, language="text")
                if e_txt:
                    st.markdown(f"**Endurance ({e_t} min):**")
                    st.code(e_txt, language="text")
                if m_txt:
                    st.markdown(f"**Main Block / WOD ({m_t} min):**")
                    st.code(m_txt, language="text")
                if a_txt:
                    st.markdown(f"**Accessory ({a_t} min):**")
                    st.code(a_txt, language="text")
                if r_txt:
                    st.markdown(f"**Mobility ({r_t} min):**")
                    st.code(r_txt, language="text")

elif st.session_state.menu_escolhido == "Configurações":
    st.title("Configurações do Sistema & Gestão de Usuários")
    st.markdown("Ajustes gerais do ambiente Alpha Iron 2.0 e controle de acesso.")
    
    st.subheader("Informações da Unidade")
    st.text_input("Nome da Unidade", value="Alpha Iron Athletics - São Paulo")
    st.text_input("Responsável Técnico", value="Mikael Santos")
    st.selectbox("Tema da Interface", ["Dark Alpha (Padrão)", "High Contrast"])
    
    st.markdown("---")
    st.subheader("🤖 Configuração da Inteligência Artificial (Gemini API)")
    st.markdown("Insira sua chave de API do Google Gemini para ativar as **Intelligence Suggestions** com IA em tempo real.")
    api_key_input = st.text_input("Chave API Google Gemini", value=st.session_state.get("gemini_api_key", ""), type="password")
    if st.button("Salvar Chave da IA"):
        st.session_state.gemini_api_key = api_key_input.strip()
        st.success("Chave de IA salva com sucesso para esta sessão!")
    if st.button("Salvar Configurações"):
        st.success("Configurações atualizadas com sucesso!")
        
    st.markdown("---")
    st.subheader("👥 Cadastro e Gestão de Usuários (Login)")
    st.markdown("Cadastre novos usuários/coaches para que cada um tenha seu próprio acesso com senha e treinos salvos isoladamente.")
    
    with st.form("form_cadastrar_usuario_novo"):
        novo_username = st.text_input("Nome de Usuário para Login (ex: coachjoao)")
        novo_nome_completo = st.text_input("Nome Completo / Apelido")
        nova_senha = st.text_input("Senha de Acesso", type="password")
        tipo_user = st.selectbox("Nível de Acesso", ["Treinador / Coach", "Administrador"])
        
        if st.form_submit_button("Cadastrar Novo Usuário"):
            if novo_username.strip() and nova_senha.strip():
                u_key = novo_username.strip().lower()
                if u_key not in credenciais_sistema:
                    slug_db = f"treinos_salvos_{u_key}.json"
                    credenciais_sistema[u_key] = {
                        "senha": nova_senha.strip(),
                        "nome": novo_nome_completo.strip() if novo_nome_completo.strip() else novo_username.strip(),
                        "tipo": tipo_user,
                        "db": slug_db
                    }
                    salvar_credenciais(credenciais_sistema)
                    st.success(f"Usuário '{u_key}' cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Este nome de usuário já existe.")
            else:
                st.error("Preencha o usuário e a senha.")
                
    st.markdown("#### Usuários Atualmente Cadastrados:")
    for u_k, u_v in credenciais_sistema.items():
        st.write(f"- **Usuário de Login:** `{u_k}` | **Nome:** {u_v['nome']} | **Tipo:** *{u_v['tipo']}*")
