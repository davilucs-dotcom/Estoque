import streamlit as st
from supabase import create_client

# 1. SEGURANÇA: Lê as chaves do cofre
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Mix Estoque", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- ESTILIZAÇÃO VISUAL (CSS) - DARK MODE ---
st.markdown("""
    <style>
    /* Base: Fundo Preto Puro */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #000000 !important;
        color: #ffffff;
    }
    .stApp {
        background-color: #000000 !important;
    }

    header[data-testid="stHeader"] { display: none; }
    .block-container { padding-top: 1rem; }

    /* ── CABEÇALHO ── */
    .top-bar {
        background-color: #111111;
        border-bottom: 1px solid #222222;
        padding: 20px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -1rem -4rem 2.5rem -4rem;
    }
    .top-bar-title {
        font-family: 'Sora', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .top-bar-sub {
        font-size: 13px;
        color: #888888;
        margin-top: 2px;
    }
    .top-bar-badge {
        background: #FF6600; 
        color: #ffffff;
        font-family: 'Sora', sans-serif;
        font-weight: 700;
        font-size: 11px;
        padding: 6px 14px;
        border-radius: 20px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* ── BARRA DE BUSCA (Dark Mode) ── */
    div[data-testid="stTextInput"] input {
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif;
        font-size: 15px;
        padding: 10px 18px !important;
        background: #1A1A1A !important;
        color: #ffffff !important;
        box-shadow: none;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #FF6600 !important;
    }

    /* ── CARDS DE PRODUTO ── */
    .card {
        background: #141414; /* Cinza super escuro */
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
        border: 1px solid #2a2a2a;
        margin-bottom: 25px;
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #FF6600;
    }

    /* Foto/Ícone mais discreto */
    .card-img {
        height: 140px;
        background: linear-gradient(135deg, #222222 0%, #181818 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 18px;
    }
    .card-img-icon {
        width: 60px;
        height: 60px;
        opacity: 0.2; 
    }

    .card-nome {
        font-family: 'Sora', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #FFFFFF; /* Texto branco */
        margin-bottom: 5px;
        text-align: center;
    }
    
    .card-preco {
        font-family: 'DM Sans', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #FF6600; /* Laranja em destaque */
        margin-bottom: 12px;
        text-align: center;
    }
    .card-preco span {
        font-size: 14px;
        font-weight: 500;
        color: #777777;
        margin-right: 4px;
    }

    /* Badges com estilo "Neon/Dark" */
    .estoque-wrapper {
        text-align: center;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 20px;
        letter-spacing: 0.2px;
    }
    .badge-ok { background: rgba(30, 122, 69, 0.2); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3); }
    .badge-baixo { background: rgba(192, 94, 0, 0.2); color: #fb923c; border: 1px solid rgba(251, 146, 60, 0.3); }
    .badge-zero { background: rgba(192, 57, 43, 0.2); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }

    div[data-testid="column"] button { display: none; }
    </style>
""", unsafe_allow_html=True)

# ── CABEÇALHO ──
st.markdown("""
    <div class="top-bar">
        <div>
            <div class="top-bar-title">MIX Mateus Estoque</div>
            <div class="top-bar-sub">Consulta de disponibilidade em tempo real</div>
        </div>
        <div class="top-bar-badge">Live</div>
    </div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def buscar_produtos():
    res = supabase.table("produtos").select("id, nome, preco, quantidade").order("nome").execute()
    return res.data

produtos = buscar_produtos()

# ── BUSCA ──
c_b1, c_b2, c_b3 = st.columns([1, 2, 1])
with c_b2:
    busca = st.text_input("", placeholder=" Digite o nome do produto para filtrar...", label_visibility="collapsed")

if busca:
    produtos = [p for p in produtos if busca.lower() in p['nome'].lower()]

# ── GRID DE PRODUTOS ──
st.markdown("<br>", unsafe_allow_html=True)

COLUNAS = 5 

if not produtos:
    st.info("Nenhum produto encontrado para essa busca.")
else:
    for i in range(0, len(produtos), COLUNAS):
        cols = st.columns(COLUNAS)
        for j, col in enumerate(cols):
            if i + j < len(produtos):
                p = produtos[i + j]
                qtd = p['quantidade']

                if qtd == 0:
                    badge = '<span class="badge badge-zero">Esgotado</span>'
                elif qtd <= 5:
                    badge = f'<span class="badge badge-baixo">Crítico: {qtd} un.</span>'
                else:
                    badge = f'<span class="badge badge-ok">Disponível</span>'

                # Ícone em tons de cinza escuro
                icone_svg = """<svg class="card-img-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="6" y="14" width="36" height="28" rx="3" fill="#444444"/>
                    <path d="M6 20h36" stroke="#222222" stroke-width="2"/>
                    <path d="M18 14V10a6 6 0 0 1 12 0v4" stroke="#444444" stroke-width="2.5" stroke-linecap="round"/>
                </svg>"""

                with col:
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-img">{icone_svg}</div>
                            <div class="card-nome" title="{p['nome']}">{p['nome']}</div>
                            <div class="card-preco"><span>R$</span>{p['preco']:.2f}</div>
                            <div class="estoque-wrapper">{badge}</div>
                        </div>
                    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#555; font-size:12px;">MIX Mateus · Painel de Consulta Interna</p>', unsafe_allow_html=True)