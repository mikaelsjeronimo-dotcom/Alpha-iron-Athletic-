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
    css_bg_geral = f'background: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.92)), url("data:image/jpeg;base64,{img_bg_base64}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;'
else:
    css_bg_geral = 'background-color: #0e1117;'


# ==========================================
# MODO TV ANTIGA (WOD TV Raiz / Autônoma)
# ==========================================
query_params = st.query_params
if query_params.get("modo") == "tv_antiga":
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

    db_alvo = "treinos_salvos_mikael.json"
    dados_treinos = {}
    if os.path.exists(db_alvo):
        try:
            with open(db_alvo, "r", encoding="utf-8") as f_db:
                dados_treinos = json.load(f_db)
        except Exception:
            pass

    nome_dia_exibicao = dias_traducao_pt.get(dia_atual_str, dia_atual_str)
    w_t = dados_treinos.get(f"{dia_atual_str}_t_w", 10)
    w_txt = dados_treinos.get(f"{dia_atual_str}_w", "Nenhum cadastro")
    s_t = dados_treinos.get(f"{dia_atual_str}_t_s", 15)
    s_txt = dados_treinos.get(f"{dia_atual_str}_s", "Nenhum cadastro")
    m_t = dados_treinos.get(f"{dia_atual_str}_t_m", 15)
    m_txt = dados_treinos.get(f"{dia_atual_str}_m", "Nenhum cadastro")
    r_t = dados_treinos.get(f"{dia_atual_str}_t_r", 5)
    r_txt = dados_treinos.get(f"{dia_atual_str}_r", "Nenhum cadastro")

    bg_style_html = f'background: linear-gradient(rgba(14, 17, 23, 0.88), rgba(14, 17, 23, 0.94)), url("data:image/jpeg;base64,{img_bg_base64}"); background-size: cover; background-position: center; background-attachment: fixed;' if img_bg_base64 else 'background-color: #0e1117;'

    html_raiz = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="300">
        <title>ALPHA IRON WOD TV</title>
        <style>
            body {{
                {bg_style_html}
                color: #f0f2f6;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            h1 {{
                color: #00E5FF;
                text-align: center;
                font-size: 38px;
                margin-bottom: 5px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.8);
            }}
            h3 {{
                color: #00E5FF;
                font-size: 22px;
                border-bottom: 2px solid #00E5FF;
                padding-bottom: 5px;
                margin-top: 15px;
            }}
            .subtitle {{
                text-align: center;
                color: #9ca3af;
                font-size: 20px;
                margin-bottom: 25px;
            }}
            .container {{
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
            }}
            .card {{
                background-color: rgba(22, 25, 32, 0.88);
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 10px;
                padding: 20px;
                width: 45%;
                min-width: 300px;
                margin-bottom: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.7);
            }}
            pre {{
                background-color: rgba(11, 13, 18, 0.9);
                color: #ffffff;
                padding: 15px;
                border-radius: 6px;
                font-size: 17px;
                white-space: pre-wrap;
                word-wrap: break-word;
                font-family: 'Courier New', Courier, monospace;
            }}
        </style>
    </head>
    <body>
        <h1>ALPHA IRON ATHLETICS — WOD TV</h1>
        <div class="subtitle">📅 Hoje: <strong>{nome_dia_exibicao}</strong> (Atualização Automática)</div>
        
        <div class="container">
            <div class="card">
                <h3>⚡ Warm-Up ({w_t} min)</h3>
                <pre>{w_txt}</pre>
                
                <h3>🏋️ Strength ({s_t} min)</h3>
                <pre>{s_txt}</pre>
            </div>
            
            <div class="card">
                <h3>🔥 WOD / Main Block ({m_t} min)</h3>
                <pre>{m_txt}</pre>
                
                <h3>🧘 Mobility ({r_t} min)</h3>
                <pre>{r_txt}</pre>
            </div>
        </div>
    </body>
    </html>
    """
    st.components.v1.html(html_raiz, height=900, scrolling=True)
    st.stop()


# ==========================================
# MODO WOD TV MODERNA
# ==========================================
if query_params.get("modo") == "tv":
    st.markdown(f"""
        <style>
        [data-testid="stHeader"], [data-testid="stSidebar"], footer {{display: none !important;}}
        .stApp {{ {css_bg_geral} color: #f0f2f6 !important; }}
        div.stMarkdown, div.element-container {{ background-color: rgba(22, 25, 32, 0.75); padding: 15px; border-radius: 12px; border: 1px solid rgba(0,229,255,0.2); box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
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
css_bg_main = f'.stApp {{ {css_bg_geral} color: #f0f2f6; }}'

st.markdown(f"""
    <style>
    {css_bg_main}
    [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0) !important; }}
    [data-testid="stSidebar"] {{ background-color: rgba(14, 17, 23, 0.7) !important; backdrop-filter: blur(8px); border-right: 1px solid rgba(255, 255, 255, 0.1); }}
    h1, h2, h3, h4 {{ color: #00E5FF !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; letter-spacing: -0.5px; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; background-color: rgba(18, 20, 24, 0.85); padding: 6px; border-radius: 12px; border: 1px solid #22262d; }}
    .stTabs [data-baseweb="tab"] {{ background-color: rgba(26, 29, 36, 0.9); color: #9ca3af; border-radius: 8px; padding: 8px 16px; font-weight: 600; border: none !important; outline: none !important; }}
    .stTabs [aria-selected="true"] {{ background: linear-gradient(135deg, #0051ff 0%, #00e5ff 100%) !important; color: #0e1117 !important; border-radius: 8px !important; box-shadow: 0 4px 12px rgba(0, 229, 255, 0.3) !important; border: none !important; }}
    .stTextInput input, .stTextArea textarea {{ background-color: rgba(22, 25, 32, 0.9) !important; color: #ffffff !important; border: 1px solid #2a2f3a !important; border-radius: 8px !important; }}
    .stButton button {{ background: linear-gradient(135deg, #0051ff 0%, #00e5ff 100%); color: #0e1117; font-weight: 700; border-radius: 8px; border: none; padding: 0.6rem 1.2rem; box-shadow: 0 4px 12px rgba(0, 229, 255, 0.3); }}
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
    if st.sidebar.button(op, key=f"menu_btn_{op}", use_container_width=True):
        st.session_state.menu_escolhido = op
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Periodização (Planilha 2.0)")
bloco = st.sidebar.selectbox("Periodization Phase", [
    "Block 1 - Strength Focus", "Block 2 - Engine Focus", "Block 3 - Gymnastics Focus", "Block 4 - Weightlifting Focus"
], key="sel_bloco_per")

semana = st.sidebar.selectbox("Periodization Week", [
    "Week 1 - Accumulation", "Week 2 - Progression", "Week 3 - Overload", "Week 4 - Deload / Benchmark"
], key="sel_semana_per")

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
    st.markdown("Bem-vindo ao centro de comando da periodização e montagem de treinos.")
    
elif st.session_state.menu_escolhido == "🖥️ WOD TV (Para a TV)":
    st.title("🖥️ WOD TV — Tela para a TV do Box")
    st.markdown("Como a TV antiga bloqueia links seguros da nuvem por causa do certificado SSL, criamos a opção de **Baixar a WOD TV em arquivo HTML** para rodar direto nela sem erros!")
    
    link_tv_nuvem = "https://mikaelsjeronimo-dotcom-alpha-iron-athletic--app-d1qo92.streamlit.app/?modo=tv"
    
    st.success(f"📺 **Link para TV Moderna:** `{link_tv_nuvem}`")
    
    st.markdown("---")
    st.subheader("📥 Baixar Arquivo WOD TV para TV Antiga")
    st.markdown("Clique no botão abaixo para gerar e baixar o arquivo `wod_tv.html` atualizado com o treino de hoje. Você pode colocá-lo num pendrive ou abrir direto na TV antiga!")
    
    if st.button("Gerar e Baixar wod_tv.html"):
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
        nome_dia_exibicao = dias_traducao_pt.get(dia_atual_str, dia_atual_str)
        w_t = treinos_salvos.get(f"{dia_atual_str}_t_w", 10)
        w_txt = treinos_salvos.get(f"{dia_atual_str}_w", "Nenhum cadastro")
        s_t = treinos_salvos.get(f"{dia_atual_str}_t_s", 15)
        s_txt = treinos_salvos.get(f"{dia_atual_str}_s", "Nenhum cadastro")
        m_t = treinos_salvos.get(f"{dia_atual_str}_t_m", 15)
        m_txt = treinos_salvos.get(f"{dia_atual_str}_m", "Nenhum cadastro")
        r_t = treinos_salvos.get(f"{dia_atual_str}_t_r", 5)
        r_txt = treinos_salvos.get(f"{dia_atual_str}_r", "Nenhum cadastro")

        bg_css = f'background: linear-gradient(rgba(14, 17, 23, 0.88), rgba(14, 17, 23, 0.94)), url("data:image/jpeg;base64,{img_bg_base64}"); background-size: cover; background-position: center; background-attachment: fixed;' if img_bg_base64 else 'background-color: #0e1117;'

        html_arquivo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="300">
    <title>ALPHA IRON WOD TV</title>
    <style>
        body {{ {bg_css} color: #f0f2f6; font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        h1 {{ color: #00E5FF; text-align: center; font-size: 38px; margin-bottom: 5px; text-shadow: 0 2px 10px rgba(0,0,0,0.8); }}
        h3 {{ color: #00E5FF; font-size: 22px; border-bottom: 2px solid #00E5FF; padding-bottom: 5px; margin-top: 15px; }}
        .subtitle {{ text-align: center; color: #9ca3af; font-size: 20px; margin-bottom: 25px; }}
        .container {{ display: flex; justify-content: space-around; flex-wrap: wrap; }}
        .card {{ background-color: rgba(22, 25, 32, 0.88); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 10px; padding: 20px; width: 45%; min-width: 300px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.7); }}
        pre {{ background-color: rgba(11, 13, 18, 0.9); color: #ffffff; padding: 15px; border-radius: 6px; font-size: 17px; white-space: pre-wrap; word-wrap: break-word; font-family: 'Courier New', Courier, monospace; }}
    </style>
</head>
<body>
    <h1>ALPHA IRON ATHLETICS — WOD TV</h1>
    <div class="subtitle">📅 Hoje: <strong>{nome_dia_exibicao}</strong> (Atualização Automática)</div>
    <div class="container">
        <div class="card">
            <h3>⚡ Warm-Up ({w_t} min)</h3>
            <pre>{w_txt}</pre>
            <h3>🏋️ Strength ({s_t} min)</h3>
            <pre>{s_txt}</pre>
        </div>
        <div class="card">
            <h3>🔥 WOD / Main Block ({m_t} min)</h3>
            <pre>{m_txt}</pre>
            <h3>🧘 Mobility ({r_t} min)</h3>
            <pre>{r_txt}</pre>
        </div>
    </div>
</body>
</html>"""
        
        st.download_button(
            label="💾 Baixar Arquivo WOD TV Pronto",
            data=html_arquivo,
            file_name="wod_tv.html",
            mime="text/html"
        )
        st.success("Arquivo gerado com sucesso! Clique no botão acima para baixar.")

elif st.session_state.menu_escolhido == "Montagem de Treinos":
    st.title("Alpha Iron 2.0 — Workout Builder")
    st.markdown("Monte e ajuste os blocos diários.")

elif st.session_state.menu_escolhido == "Treinos Salvos":
    st.title("Histórico de Treinos Salvos")

elif st.session_state.menu_escolhido == "Configurações":
    st.title("Configurações do Sistema")
