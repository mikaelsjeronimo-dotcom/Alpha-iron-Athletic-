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

# --- ESTILIZAÇÃO ESTÉTICA (MODERN DARK MODE & FITNESS DASHBOARD) ---
st.markdown("""
    <style>
    /* Importando fonte moderna Google Fonts (Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo geral da aplicação */
    .main {
        background-color: #0b0e14;
        color: #e2e8f0;
    }

    /* Sidebar com tom ligeiramente diferenciado para contraste */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    /* Estilização de Títulos */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 1.8
