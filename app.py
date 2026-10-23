import streamlit as st
import pandas as pd
import os
import glob
import base64
import re
import json
import google.generativeai as genai

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

def chamar_gemini_sdk(prompt_texto):
    api_key = st.session_state.get("gemini_api_key", "")
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    
    if not api_key:
        raise Exception("Chave da API do Gemini não configurada.")
        
    genai.configure(api_key=api_key)
    # Modelo atualizado e estável
    model = genai.GenerativeModel('gemini-3.8-flash')
    response = model.generate_content(prompt_texto)
    return response.text

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
        txt_resp = chamar_gemini_sdk(prompt)
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
            "Recommended Programming": ["Não foi possível conectar ao Gemini via SDK oficial.", str(e)]
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
    st.markdown("Monte e ajuste os blocos diários com salvamento automático e controle de volume.")
    
    tabs = st.tabs([d["day"] for d in dias_semana])
    dados_para_salvar = {}

    for i, tab in enumerate(tabs):
        day_info = dias_semana[i]
        day_name = day_info["day"]
        day_focus = day_info["focus"]
        
        with tab:
            st.subheader(f"{day_name} — {day_focus}")
            col1, col2 = st.columns([1.3, 1])
            lista_blocos_do_dia = []
            m_input_atual = ""
            
            with col1:
                st.markdown("### Session Structure (60 min)")
                if day_name == "Monday":
                    t_w = st.text_input("Warm (min)", value=str(treinos_salvos.get(f"{day_name}_t_w", "10")), key=f"t_hy_w_{i}")
                    w_input = st.text_area("Warm-Up Descrição", treinos_salvos.get(f"{day_name}_w", "Dynamic Mobility"), height=75, key=f"hy_w_{i}")
                    t_m = st.text_input("Main (min)", value=str(treinos_salvos.get(f"{day_name}_t_m", "40")), key=f"t_hy_m_{i}")
                    m_input_atual = st.text_area("HYROX Main Block", treinos_salvos.get(f"{day_name}_m", "Running + Stations"), height=110, key=f"hy_m_{i}")
                    t_r = st.text_input("Mob (min)", value=str(treinos_salvos.get(f"{day_name}_t_r", "10")), key=f"t_hy_r_{i}")
                    r_input = st.text_area("Mobility Descrição", treinos_salvos.get(f"{day_name}_r", "Stretching"), height=75, key=f"hy_r_{i}")
                    
                    tw_val = int(t_w) if t_w.isdigit() else 0
                    tm_val = int(t_m) if t_m.isdigit() else 0
                    tr_val = int(t_r) if t_r.isdigit() else 0
                    total_time = tw_val + tm_val + tr_val
                    lista_blocos_do_dia = [{"texto": w_input, "tempo": tw_val}, {"texto": m_input_atual, "tempo": tm_val}]
                    dados_para_salvar.update({f"{day_name}_t_w": tw_val, f"{day_name}_w": w_input, f"{day_name}_t_m": tm_val, f"{day_name}_m": m_input_atual, f"{day_name}_t_r": tr_val, f"{day_name}_r": r_input})

                elif day_name == "Friday":
                    t_w = st.text_input("Warm (min)", value=str(treinos_salvos.get(f"{day_name}_t_w", "10")), key=f"t_athx_w_{i}")
                    w_input = st.text_area("Warm-Up Descrição", treinos_salvos.get(f"{day_name}_w", "Dynamic"), height=75, key=f"athx_w_{i}")
                    t_s = st.text_input("Str (min)", value=str(treinos_salvos.get(f"{day_name}_t_s", "15")), key=f"t_athx_s_{i}")
                    s_input = st.text_area("Strength Max Descrição", treinos_salvos.get(f"{day_name}_s", ""), height=75, key=f"athx_s_{i}")
                    t_e = st.text_input("End (min)", value=str(treinos_salvos.get(f"{day_name}_t_e", "15")), key=f"t_athx_e_{i}")
                    l_input = st.text_area("Endurance Descrição", treinos_salvos.get(f"{day_name}_e", ""), height=75, key=f"athx_e_{i}")
                    t_m = st.text_input("WOD (min)", value=str(treinos_salvos.get(f"{day_name}_t_m", "15")), key=f"t_athx_m_{i}")
                    m_input_atual = st.text_area("MetCon X Descrição", treinos_salvos.get(f"{day_name}_m", ""), height=90, key=f"athx_m_{i}")
                    t_r = st.text_input("Mob (min)", value=str(treinos_salvos.get(f"{day_name}_t_r", "5")), key=f"t_athx_r_{i}")
                    r_input = st.text_area("Mobility Descrição", treinos_salvos.get(f"{day_name}_r", "Stretching"), height=75, key=f"athx_r_{i}")

                    tw_val = int(t_w) if t_w.isdigit() else 0
                    ts_val = int(t_s) if t_s.isdigit() else 0
                    te_val = int(t_e) if t_e.isdigit() else 0
                    tm_val = int(t_m) if t_m.isdigit() else 0
                    tr_val = int(t_r) if t_r.isdigit() else 0
                    total_time = tw_val + ts_val + te_val + tm_val + tr_val
                    lista_blocos_do_dia = [{"texto": w_input, "tempo": tw_val}, {"texto": s_input, "tempo": ts_val}, {"texto": l_input, "tempo": te_val}, {"texto": m_input_atual, "tempo": tm_val}]
                    dados_para_salvar.update({f"{day_name}_t_w": tw_val, f"{day_name}_w": w_input, f"{day_name}_t_s": ts_val, f"{day_name}_s": s_input, f"{day_name}_t_e": te_val, f"{day_name}_e": l_input, f"{day_name}_t_m": tm_val, f"{day_name}_m": m_input_atual, f"{day_name}_t_r": tr_val, f"{day_name}_r": r_input})

                else:
                    t_w = st.text_input("Warm (min)", value=str(treinos_salvos.get(f"{day_name}_t_w", "10")), key=f"t_cf_w_{i}")
                    w_input = st.text_area("1. Warm-Up", treinos_salvos.get(f"{day_name}_w", ""), height=75, key=f"cf_w_{i}")
                    t_s = st.text_input("Str (min)", value=str(treinos_salvos.get(f"{day_name}_t_s", "15")), key=f"t_cf_s_{i}")
                    s_input = st.text_area("2. Strength", treinos_salvos.get(f"{day_name}_s", ""), height=75, key=f"cf_s_{i}")
                    t_l = st.text_input("Skill (min)", value=str(treinos_salvos.get(f"{day_name}_t_l", "10")), key=f"t_cf_l_{i}")
                    l_input = st.text_area("3. Skill", treinos_salvos.get(f"{day_name}_l", ""), height=75, key=f"cf_l_{i}")
                    t_m = st.text_input("WOD (min)", value=str(treinos_salvos.get(f"{day_name}_t_m", "15")), key=f"t_cf_m_{i}")
                    m_input_atual = st.text_area("4. WOD", treinos_salvos.get(f"{day_name}_m", ""), height=90, key=f"cf_wod_{i}")
                    t_a = st.text_input("Acc (min)", value=str(treinos_salvos.get(f"{day_name}_t_a", "5")), key=f"t_cf_a_{i}")
                    a_input = st.text_area("5. Accessory", treinos_salvos.get(f"{day_name}_a", ""), height=75, key=f"cf_a_{i}")
                    t_r = st.text_input("Mob (min)", value=str(treinos_salvos.get(f"{day_name}_t_r", "5")), key=f"t_cf_r_{i}")
                    r_input = st.text_area("6. Mobility", treinos_salvos.get(f"{day_name}_r", ""), height=75, key=f"cf_m_{i}")

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

            with col2:
                st.markdown("### Intelligence Suggestions")
                df_sugestoes = gerar_sugestoes_com_ia(bloco, semana, day_name, day_focus, treinos_salvos)
                st.table(df_sugestoes)

    salvar_treinos_disco(dados_para_salvar)

elif st.session_state.menu_escolhido == "🤖 Teste de Diagnóstico da IA":
    st.title("🤖 Painel de Diagnóstico Direto da IA (Google SDK)")
    st.markdown("Envie qualquer mensagem ou comando de teste abaixo para verificar instantaneamente se a API está conectada.")
    
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
            with st.spinner("Conectando com o Gemini via SDK oficial..."):
                try:
                    resposta_ia = chamar_gemini_sdk(mensagem_teste)
                    st.success("🎉 Resposta recebida com sucesso!")
                    st.info(resposta_ia)
                except Exception as e:
                    st.error(f"❌ Erro ao comunicar com a API:")
                    st.code(str(e), language="text")

elif st.session_state.menu_escolhido == "Configurações":
    st.title("Configurações do Sistema")
    api_key_input = st.text_input("Chave API Google Gemini", value=st.session_state.get("gemini_api_key", ""), type="password")
    if st.button("Salvar Chave da IA"):
        st.session_state.gemini_api_key = api_key_input.strip()
        st.success("Chave salva com sucesso!")
