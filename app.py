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
# Inserido antes do login para abrir direto sem restrições
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
    
    # Identifica o dia atual do Brasil (Fuso de Brasília UTC-3)
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

    # Seletor rápido de usuário na TV caso queira alternar bases de dados
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

    # Exibição otimizada em destaque para a TV do dia atual
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
# SISTEMA PRINCIPAL (Mantido intacto)
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
