
from pathlib import Path

arquivo = Path("app.py")
if not arquivo.exists():
    raise FileNotFoundError("Coloque este script na mesma pasta do app.py.")

codigo = arquivo.read_text(encoding="utf-8")

marcador = "credenciais_sistema = carregar_credenciais()"

if "MODO WOD TV ALPHA IRON" in codigo:
    print("O modo WOD TV já está instalado.")
    raise SystemExit

if marcador not in codigo:
    raise RuntimeError("Não encontrei o ponto de inserção no app.py original.")

bloco_tv = r'''

# ================= MODO WOD TV ALPHA IRON =================
import html
from datetime import datetime
from zoneinfo import ZoneInfo

modo_tv = st.query_params.get("modo", "") == "tv"

if modo_tv:
    credenciais_tv = carregar_credenciais()
    usuario_tv = str(st.query_params.get("usuario", "mikael")).strip().lower()

    if usuario_tv not in credenciais_tv:
        usuario_tv = "mikael"

    info_tv = credenciais_tv.get(usuario_tv, {})
    arquivo_tv = info_tv.get("db", "treinos_salvos_mikael.json")

    try:
        with open(arquivo_tv, "r", encoding="utf-8") as f:
            dados_tv = json.load(f)
    except (OSError, json.JSONDecodeError):
        dados_tv = {}

    dia_ingles = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%A")
    dias_pt = {
        "Monday": "SEGUNDA-FEIRA",
        "Tuesday": "TERÇA-FEIRA",
        "Wednesday": "QUARTA-FEIRA",
        "Thursday": "QUINTA-FEIRA",
        "Friday": "SEXTA-FEIRA",
        "Saturday": "SÁBADO",
        "Sunday": "DOMINGO",
    }
    focos = {
        "Monday": "HYROX",
        "Tuesday": "CROSSFIT — FORÇA / LPO",
        "Wednesday": "CROSSFIT — GINÁSTICA",
        "Thursday": "CROSSFIT — FORÇA / LPO",
        "Friday": "ATHX / GHX",
        "Saturday": "COMMUNITY WOD",
        "Sunday": "BENCHMARK / HERO WOD",
    }

    st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stHeader"],
    [data-testid="stToolbar"], [data-testid="stDecoration"], footer {
        display: none !important;
    }
    .stApp {
        background: #0e1117 !important;
        color: #f0f2f6 !important;
    }
    .block-container {
        max-width: 1600px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
    }
    .tv-header {
        text-align: center;
        border-bottom: 1px solid #26313c;
        padding: 12px 0 25px;
        margin-bottom: 24px;
    }
    .tv-brand {
        color: #00E5FF;
        font-size: clamp(18px, 2vw, 28px);
        font-weight: 900;
        letter-spacing: 4px;
    }
    .tv-day {
        color: white;
        font-size: clamp(32px, 5vw, 62px);
        font-weight: 900;
        margin-top: 8px;
    }
    .tv-focus {
        color: #00E5FF;
        font-size: clamp(17px, 2vw, 27px);
        font-weight: 700;
        margin-top: 5px;
    }
    .tv-block {
        background: #161920;
        border: 1px solid #2a3440;
        border-left: 6px solid #00E5FF;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 17px;
        overflow-wrap: anywhere;
    }
    .tv-title {
        color: #00E5FF;
        font-size: clamp(21px, 2.5vw, 32px);
        font-weight: 900;
        margin-bottom: 12px;
    }
    .tv-text {
        color: #ffffff;
        font-size: clamp(19px, 2.1vw, 29px);
        line-height: 1.5;
        white-space: pre-wrap;
    }
    .tv-empty {
        text-align: center;
        padding: 45px 15px;
        color: #9ca3af;
        font-size: 24px;
        border: 1px solid #2a3440;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="tv-header">'
        f'<div class="tv-brand">ALPHA IRON ATHLETICS</div>'
        f'<div class="tv-day">{html.escape(dias_pt.get(dia_ingles, dia_ingles.upper()))}</div>'
        f'<div class="tv-focus">{html.escape(focos.get(dia_ingles, "WOD DO DIA"))}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    blocos_tv = [
        ("w", "WARM-UP", "t_w"),
        ("s", "STRENGTH", "t_s"),
        ("l", "SKILL", "t_l"),
        ("e", "ENDURANCE", "t_e"),
        ("m", "WOD / MAIN BLOCK", "t_m"),
        ("a", "ACCESSORY", "t_a"),
        ("r", "MOBILITY", "t_r"),
    ]

    encontrou = False

    for chave, titulo, chave_tempo in blocos_tv:
        texto = str(dados_tv.get(f"{dia_ingles}_{chave}", "") or "").strip()
        if not texto:
            continue

        encontrou = True
        tempo = dados_tv.get(f"{dia_ingles}_{chave_tempo}", "")
        try:
            tempo_num = float(tempo)
            tempo_txt = f" — {tempo_num:g} MIN"
        except (ValueError, TypeError):
            tempo_txt = ""

        st.markdown(
            f'<div class="tv-block">'
            f'<div class="tv-title">{html.escape(titulo + tempo_txt)}</div>'
            f'<div class="tv-text">{html.escape(texto)}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    if not encontrou:
        st.markdown(
            '<div class="tv-empty">NENHUM TREINO CADASTRADO PARA HOJE</div>',
            unsafe_allow_html=True
        )

    st.stop()
# =============== FIM DO MODO WOD TV ALPHA IRON ===============
'''

codigo = codigo.replace(marcador, marcador + bloco_tv, 1)

# Corrige somente o caso em que não existe imagem de fundo.
codigo = codigo.replace(
    'if img_bg_base64:\n    css_bg =',
    'css_bg = \'.stApp { background-color: #0e1117; color: #f0f2f6; }\'\nif img_bg_base64:\n    css_bg =',
    1
)

backup = Path("app_backup_antes_modo_tv.py")
backup.write_text(arquivo.read_text(encoding="utf-8"), encoding="utf-8")
arquivo.write_text(codigo, encoding="utf-8")

print("Modo WOD TV instalado. Backup criado em app_backup_antes_modo_tv.py")
