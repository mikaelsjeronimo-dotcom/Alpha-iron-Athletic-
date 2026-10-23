import streamlit as st
import pandas as pd
import os
import glob
import base64
import re
import json
import urllib.request
import urllib.error

st.set_page_config(
    page_title="Alpha Iron Athletics 2.0 — Sistema de Gestão", 
    layout="wide"
)

query_params = st.query_params
if query_params.get("modo") == "tv":
    st.markdown("""
        <style>
        [data-testid="stHeader"], [data-testid="stSidebar"], footer {display: none !important;}
        body, .stApp { background-color: #0e1117 !important; color: #f0f2f6 !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #00E5FF; font-size: 38px;'>ALPHA IRON ATHLETICS — WOD TV</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 20px;'>Atualização Automática na Nuvem</p>", unsafe_allow_html=True)
    
    db_file = "treinos_salvos_mikael.json"
    dados_treinos = {}
    if os.path.exists(db_file):
        try:
            with open(db_file, "r", encoding="utf-8") as f:
                dados_treinos = json.load(f)
        except Exception:
            pass

    dias_semana_full = [
        ("Monday", "Segunda-feira — HYROX"),
        ("Tuesday", "Terça-feira — CrossFit (Strength / LPO)"),
        ("Wednesday", "Quarta-feira — CrossFit (Gymnastics)"),
        ("Thursday", "Quinta-feira — CrossFit (Strength / LPO)"),
        ("Friday", "Sexta-feira — ATHX"),
        ("Saturday", "Sábado — Community WOD"),
        ("Sunday", "Domingo — Benchmark / Hero WOD")
    ]
    
    cols_tv = st.columns(3)
    for idx, (d, nome_dia) in enumerate(dias_semana_full):
        w_t = dados_treinos.get(f"{d}_t_w", 10)
        w_txt = dados_treinos.get(f"{d}_w", "")
        s_t = dados_treinos.get(f"{d}_t_s", 15)
        s_txt = dados_treinos.get(f"{d}_s", "")
        l_t = dados_treinos.get(f"{d}_t_l", 10)
        l_txt = dados_treinos.get(f"{d}_l", "")
        m_t = dados_treinos.get(f"{d}_t_m", 15)
        m_txt = dados_treinos.get(f"{d}_m", "")
        a_t = dados_treinos.get(f"{d}_t_a", 5)
        a_txt = dados_treinos.get(f"{d}_a", "")
        r_t = dados_treinos.get(f"{d}_t_r", 5)
        r_txt = dados_treinos.get(f"{d}_r", "")
        e_t = dados_treinos.get(f"{d}_t_e", 15)
        e_txt = dados_treinos.get(f"{d}_e", "")
        
        with cols_tv[idx % 3]:
            st.markdown(f"### 📌 {nome_dia}")
            blocos_html = ""
            if w_txt:
                blocos_html += f"**Warm-Up ({w_t} min):**\n{w_txt}\n\n"
            if s_txt:
                blocos_html += f"**Strength ({s_t} min):**\n{s_txt}\n\n"
            if l_txt:
                blocos_html += f"**Skill ({l_t} min):**\n{l_txt}\n\n"
            if e_txt:
                blocos_html += f"**Endurance ({e_t} min):**\n{e_txt}\n\n"
            if m_txt:
                blocos_html += f"**WOD / Main ({m_t} min):**\n{m_txt}\n\n"
            if a_txt:
                blocos_html += f"**Accessory ({a_t} min):**\n{a_txt}\n\n"
            if r_txt:
                blocos_html += f"**Mobility ({r_t} min):**\n{r_txt}\n\n"
                
            if not blocos_html:
                st.info("Nenhum treino cadastrado.")
            else:
                st.markdown(blocos_html)
            st.markdown("---")
            
    st.stop()

def obter_fundo_base64():
    nomes_possiveis = ["alpha_iron.jpg", "alpha_iron.png", "Alpha_Iron.jpg", "Alpha_Iron.png"]
    for nome in nomes_possiveis:
        if os.path.exists(nome):
            with open(nome, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    return None

img_bg_base64 = obter_fundo_base64()
css_bg = f'.stApp {{ background: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.92)), url("data:image/jpeg;base64,{img_bg_base64}"); background-size: cover; background-position: center; color: #f0f2f6; }}' if img_bg_base64 else '.stApp { background-color: #0e1117; color: #f0f2f6; }'

st.markdown(f"""
    <style>
    {css_bg}
    [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0) !important; }}
    [data-testid="stSidebar"] {{ background-color: rgba(14, 17, 23, 0.45) !important; backdrop-filter: blur(8px); }}
    h1, h2, h3, h4 {{ color: #00E5FF !important; }}
    </style>
""", unsafe_allow_html=True)

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

def gerar_arquivo_wod_tv(dados_treinos, bloco_atual, semana_atual):
    pass

def salvar_treinos_disco(dados):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

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
    "Montagem de Treinos",
    "Configurações"
]

st.sidebar.markdown("### Menu Principal")
for op in opcoes_menu:
    if st.sidebar.button(op, key=f"menu_btn_{op}", use_container_width=True):
        st.session_state.menu_escolhido = op
        st.rerun()

bloco = st.sidebar.selectbox("Periodization Phase", ["Block 1 - Strength Focus", "Block 2 - Engine Focus"], key="sel_bloco_per")
semana = st.sidebar.selectbox("Periodization Week", ["Week 1 - Accumulation", "Week 2 - Progression"], key="sel_semana_per")

treinos_salvos = carregar_treinos_salvos()
dias_semana = [
    {"day": "Monday", "focus": "HYROX"},
    {"day": "Tuesday", "focus": "CrossFit - Strength / LPO"},
    {"day": "Wednesday", "focus": "CrossFit - Gymnastics"},
    {"day": "Thursday", "focus": "CrossFit - Strength / LPO"},
    {"day": "Friday", "focus": "ATHX / GHX"},
    {"day": "Saturday", "focus": "Community WOD"},
    {"day": "Sunday", "focus": "Benchmark / Hero WOD"}
]

if st.session_state.menu_escolhido == "Início (Dashboard)":
    st.title("Alpha Iron Athletics — Painel Principal")
    st.metric("Fase Atual", bloco)

elif st.session_state.menu_escolhido == "🖥️ WOD TV (Para a TV)":
    st.title("🖥️ WOD TV — Tela para a TV do Box (LG 42LN5700)")
    link_tv_nuvem = "https://mikaelsjeronimo-dotcom-app-d1qo92.streamlit.app/?modo=tv"
    st.success(f"📺 **Link Direto para a TV:** `{link_tv_nuvem}`")
    st.markdown("Basta digitar esse link exato no navegador da TV (com `?modo=tv` no final) para abrir os treinos limpos e em tela cheia!")

elif st.session_state.menu_escolhido == "Programação Semanal":
    st.title("Programação Semanal")
    for d in dias_semana:
        st.subheader(d["day"])
        st.code(treinos_salvos.get(f"{d['day']}_m", "Vazio"), language="text")

elif st.session_state.menu_escolhido == "Montagem de Treinos":
    st.title("Workout Builder & Editor")
    tabs = st.tabs([d["day"] for d in dias_semana])
    dados_para_salvar = {}
    for i, tab in enumerate(tabs):
        day_name = dias_semana[i]["day"]
        with tab:
            m_input = st.text_area("WOD / Main Block", treinos_salvos.get(f"{day_name}_m", ""), key=f"m_{i}")
            dados_para_salvar[f"{day_name}_m"] = m_input
    salvar_treinos_disco(dados_para_salvar)

elif st.session_state.menu_escolhido == "Configurações":
    st.title("Configurações")
    st.text_input("Unidade", value="Alpha Iron Athletics")

