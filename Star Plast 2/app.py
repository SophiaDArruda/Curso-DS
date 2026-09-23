import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import time
import re
import html
import requests

# -----------------------------------------------------------------------------
# 1. FUNÇÃO DE AVATARES DINÂMICOS (DICEBEAR - HTTP NATIVO)
# -----------------------------------------------------------------------------
def gerar_avatar(seed: str, estilo: str = "bottts") -> str:
    """Gera URLs de avatares vetorizados dinamicamente sem pacotes adicionais."""
    seed_limpa = re.sub(r'[^a-zA-Z0-9]', '', seed) if seed else "starplast"
    return f"https://api.dicebear.com/9.x/{estilo}/svg?seed={seed_limpa}"

# -----------------------------------------------------------------------------
# 2. INTEGRAÇÃO COM A API DO GOOGLE GEMINI 1.5 FLASH
# -----------------------------------------------------------------------------
def chamar_api_gemini(prompt: str, api_key: str) -> str:
    """Consome a API do Google Gemini 1.5 Flash para responder a qualquer Pergunta de forma humana."""
    if not api_key:
        return (
            "⚠️ **Chave da API do Gemini não configurada.**\n\n"
            "Para conversar com a IA em tempo real, insira sua **API Key do Gemini** "
            "no campo correspondente na barra lateral esquerda."
        )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    system_instruction = (
        "Você é uma assistente virtual e coach de carreira da empresa Starplast. "
        "Sua missão é responder a QUALQUER pergunta do usuário com tom profundamente humano, "
        "empático, claro, acolhedor e altamente profissional. "
        "Ajude com dicas de carreira, currículos, preparação para entrevistas e dúvidas gerais."
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_instruction}\n\nPergunta do usuário: {prompt}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        elif response.status_code == 400:
            return "❌ Chave de API inválida ou malformatada. Verifique a chave informada na barra lateral."
        elif response.status_code == 429:
            return "⏳ Cota limite atingida temporariamente. Aguarde alguns segundos e tente novamente."
        else:
            return f"❌ Erro ao conectar à API do Gemini (Código {response.status_code})."
    except Exception as e:
        return f"⚠️ Falha de rede ao se comunicar com a IA: {str(e)}"

# -----------------------------------------------------------------------------
# 3. CONFIGURAÇÃO DE PÁGINA E CSS TEMA CLARO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Starplast | Portal de Carreiras & IA",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');
        
        #MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }
        
        .stApp {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }

        .light-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 28px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
            margin-bottom: 24px;
        }
        
        .brand-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 28px;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            margin-bottom: 25px;
        }
        .brand-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: #0F172A;
        }
        .brand-title span { color: #2563EB; }

        .badge-sec {
            background: #ECFDF5;
            color: #059669;
            border: 1px solid #A7F3D0;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .stButton button {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.5rem !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease-in-out !important;
            width: 100%;
        }

        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 10px !important;
            padding: 10px 14px !important;
        }

        .diag-pill-ok {
            background: #F0FDF4;
            border-left: 4px solid #16A34A;
            padding: 14px 18px;
            border-radius: 8px;
            color: #15803D;
            margin-bottom: 12px;
        }
        .diag-pill-warn {
            background: #FEFCE8;
            border-left: 4px solid #CA8A04;
            padding: 14px 18px;
            border-radius: 8px;
            color: #A16207;
            margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. SEGURANÇA E BANCO DE DADOS
# -----------------------------------------------------------------------------
DB_PATH = "starplast_enterprise.db"

def sanitizar_texto(texto: str) -> str:
    if not texto:
        return ""
    return html.escape(texto.strip())

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT NOT NULL,
            cidade TEXT NOT NULL,
            objetivo TEXT NOT NULL,
            nivel TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            score_ia INTEGER NOT NULL,
            data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha_hash BLOB NOT NULL
        )
    """)
    c.execute("SELECT * FROM usuarios_admin WHERE usuario = 'admin'")
    if not c.fetchone():
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw("starplast2026".encode('utf-8'), salt)
        c.execute("INSERT INTO usuarios_admin (usuario, senha_hash) VALUES (?, ?)", ("admin", senha_hash))
        
    conn.commit()
    conn.close()

init_db()

def autenticar_admin(usuario, senha):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT senha_hash FROM usuarios_admin WHERE usuario = ?", (sanitizar_texto(usuario),))
    row = c.fetchone()
    conn.close()
    return bool(row and bcrypt.checkpw(senha.encode('utf-8'), row[0]))

def salvar_candidato_db(dados):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO candidatos (nome, email, telefone, cidade, objetivo, nivel, conteudo, score_ia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sanitizar_texto(dados['nome']),
            sanitizar_texto(dados['email']),
            sanitizar_texto(dados['telefone']),
            sanitizar_texto(dados['cidade']),
            sanitizar_texto(dados['objetivo']),
            sanitizar_texto(dados['nivel']),
            sanitizar_texto(dados['conteudo']),
            int(dados['score'])
        ))
        conn.commit()
        conn.close()
        return True, "Currículo cadastrado com sucesso no banco corporativo!"
    except sqlite3.IntegrityError:
        return False, "Este e-mail já possui um cadastro ativo."
    except Exception as e:
        return False, f"Erro ao salvar: {str(e)}"

# -----------------------------------------------------------------------------
# 5. CONTROLE DE SESSÃO E BARRA LATERAL
# -----------------------------------------------------------------------------
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "curriculo"

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

if "chat_mensagens" not in st.session_state:
    st.session_state["chat_mensagens"] = [
        {"role": "assistant", "content": "Olá! Sou a **Assistente de IA da Starplast**. Como posso ajudar você hoje? Fique à vontade para tirar qualquer dúvida sobre vagas, currículo ou carreira!"}
    ]

# Header
st.markdown("""
    <div class="brand-header">
        <div class="brand-title">STARPLAST <span>CAREER & AI</span></div>
        <div class="badge-sec">⚡ Powered by Gemini 1.5 Flash API</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧭 Navegação")
    if st.button("📄 Submissão de Currículo"):
        st.session_state["pagina"] = "curriculo"
        st.rerun()
        
    if st.button("🤖 Chatbot com IA Gemini"):
        st.session_state["pagina"] = "chat_ia"
        st.rerun()
        
    if st.button("✉️ Carta de Apresentação"):
        st.session_state["pagina"] = "carta"
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🔑 Conexão com a IA")
    gemini_api_key = st.text_input(
        "Chave da API Gemini",
        type="password",
        help="Obtenha uma chave grátis no Google AI Studio (aistudio.google.com)"
    )
    
    st.markdown("---")
    if not st.session_state["admin_autenticado"]:
        if st.button("🔒 Portal do RH"):
            st.session_state["pagina"] = "login_admin"
            st.rerun()
    else:
        if st.button("🚪 Sair do RH"):
            st.session_state["admin_autenticado"] = False
            st.session_state["pagina"] = "curriculo"
            st.rerun()

# -----------------------------------------------------------------------------
# 6. PÁGINAS DA APLICAÇÃO
# -----------------------------------------------------------------------------

# SUBMISSÃO DE CURRÍCULO
if st.session_state["pagina"] == "curriculo":
    st.markdown("""
        <div class="light-card">
            <h2 style="margin:0; color:#0F172A; font-weight:800;">Cadastro de Talento & Diagnóstico</h2>
            <p style="color:#475569; margin-top:6px;">Envie suas informações para análise pelo comitê de seleção.</p>
        </div>
    """, unsafe_allow_html=True)

    col_form, col_avatar = st.columns([3, 1])

    with col_form:
        with st.form("form_curriculo"):
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome Completo *")
                email = st.text_input("E-mail *")
                cidade = st.text_input("Cidade/Estado *")
            with c2:
                telefone = st.text_input("Telefone *")
                objetivo = st.text_input("Cargo Pretendido *")
                nivel = st.selectbox("Nível Profissional *", ["Operacional", "Analista / Especialista", "Liderança", "Executivo"])

            conteudo = st.text_area("Resumo da Experiência ou Currículo em Texto *", height=180)

            b1, b2 = st.columns(2)
            with b1:
                btn_analisar = st.form_submit_button("📊 Diagnóstico Instantâneo")
            with b2:
                btn_salvar = st.form_submit_button("📤 Enviar Currículo")

    with col_avatar:
        avatar_url = gerar_avatar(email if email else "starplast_user", estilo="micah")
        st.image(avatar_url, width=150, caption="Seu Avatar Exclusivo")

    if btn_analisar and conteudo:
        termos = ["qualidade", "projetos", "gestão", "metas", "liderança", "processos"]
        encontrados = [t for t in termos if t in conteudo.lower()]
        if encontrados:
            st.markdown(f"<div class='diag-pill-ok'>✅ Termos identificados: <b>{', '.join(encontrados).upper()}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='diag-pill-warn'>💡 Adicione termos quantitativos e metas alcançadas.</div>", unsafe_allow_html=True)

    if btn_salvar and nome and email and conteudo:
        ok, msg = salvar_candidato_db({
            "nome": nome, "email": email, "telefone": telefone, "cidade": cidade,
            "objetivo": objetivo, "nivel": nivel, "conteudo": conteudo, "score": 85
        })
        if ok:
            st.success(msg)
        else:
            st.error(msg)

# CHATBOT COM IA REAL
elif st.session_state["pagina"] == "chat_ia":
    st.markdown("""
        <div class="light-card">
            <h2 style="margin:0; color:#0F172A; font-weight:800;">🤖 Assistente Virtual de IA (Gemini 1.5 Flash)</h2>
            <p style="color:#475569; margin-top:6px;">Tire dúvidas sobre processos seletivos, peça conselhos de carreira ou faça qualquer pergunta livremente.</p>
        </div>
    """, unsafe_allow_html=True)

    avatar_ia = gerar_avatar("starplast_bot", estilo="bottts")
    avatar_user = gerar_avatar("usuario_chat", estilo="avataaars")

    for msg in st.session_state["chat_mensagens"]:
        ic = avatar_ia if msg["role"] == "assistant" else avatar_user
        with st.chat_message(msg["role"], avatar=ic):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Pergunto o que quiser à IA..."):
        st.session_state["chat_mensagens"].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatar_user):
            st.markdown(prompt)

        with st.spinner("Processando resposta humana..."):
            resposta = chamar_api_gemini(prompt, gemini_api_key)

        st.session_state["chat_mensagens"].append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant", avatar=avatar_ia):
            st.markdown(resposta)

# CARTA DE APRESENTAÇÃO
elif st.session_state["pagina"] == "carta":
    st.markdown("<div class='light-card'><h2>✉️ Gerador de Carta de Apresentação</h2></div>", unsafe_allow_html=True)
    with st.form("form_carta"):
        c_nome = st.text_input("Nome Completo")
        c_cargo = st.text_input("Cargo Desejado")
        c_exp = st.text_area("Principais Pontos Fortes")
        if st.form_submit_button("Gerar Carta") and c_nome and c_cargo:
            carta = f"Prezada Equipe Starplast,\n\nTenho grande interesse no cargo de {c_cargo}. Possuo bagagem focada em {c_exp}.\n\nAtenciosamente,\n{c_nome}"
            st.text_area("Resultado:", carta, height=180)

# PAINEL RH ADMINISTRATIVO
elif st.session_state["pagina"] == "login_admin" and not st.session_state["admin_autenticado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='light-card'><h3>Acesso Restrito RH</h3>", unsafe_allow_html=True)
        with st.form("f_adm"):
            u = st.text_input("Usuário")
            p = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                if autenticar_admin(u, p):
                    st.session_state["admin_autenticado"] = True
                    st.session_state["pagina"] = "painel_admin"
                    st.rerun()
                else:
                    st.error("Credenciais incorretas.")
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state["admin_autenticado"]:
    st.markdown("### Painel do Recrutador — Starplast")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM candidatos ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        st.dataframe(df[['id', 'nome', 'email', 'telefone', 'objetivo', 'data_envio']], use_container_width=True)
        id_sel = st.selectbox("Selecione o candidato para detalhes:", df['id'].tolist())
        cand = df[df['id'] == id_sel].iloc[0]
        
        col_t, col_i = st.columns([3, 1])
        with col_t:
            st.write(f"**Nome:** {cand['nome']} | **Cargo:** {cand['objetivo']}")
            st.text_area("Conteúdo do Currículo:", cand['conteudo'], height=200)
        with col_i:
            st.image(gerar_avatar(cand['email'], estilo="micah"), width=150)