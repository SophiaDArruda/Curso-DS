import streamlit as strpt
import json
import os
import time

strpt.set_page_config(
    page_title="Gestão de Talentos | Starplast", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

strpt.markdown("""
    <style>
        #MainMenu, footer, header, [data-testid="stSidebar"] { display: none !important; }
        .stApp { background-color: #FAFAFA !important; }
        .header-institucional { background-color: #004AAD; padding: 25px; text-align: center; border-radius: 0px 0px 12px 12px; margin-bottom: 25px; }
        .header-institucional h1 { color: #FFFFFF !important; font-size: 2rem !important; margin: 0 !important; font-weight: 700 !important; }
        .stForm { background-color: #FFFFFF !important; border: 1px solid #E5E7EB !important; border-radius: 12px !important; padding: 35px !important; }
        .stButton button { background-color: #004AAD !important; color: #FFFFFF !important; border-radius: 6px !important; font-weight: 600 !important; width: 100% !important; border: none !important; }
        .score-box { background-color: #F0FDF4; border: 1px solid #BBF7D0; color: #166534; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

ARQUIVO_BANCO = "banco_dados.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_BANCO):
        return []
    with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
        return json.load(f)

if "autenticado" not in strpt.session_state:
    strpt.session_state["autenticado"] = False

if "historico_eva" not in strpt.session_state:
    strpt.session_state["historico_eva"] = [
        {"role": "assistant", "content": "Olá! Sou a Eva. O que deseja consultar sobre os candidatos cadastrados?"}
    ]

strpt.markdown("""
    <div class="header-institucional">
        <h1>STARPLAST — Módulo de Seleção</h1>
    </div>
""", unsafe_allow_html=True)

# LOGIN
if not strpt.session_state["autenticado"]:
    strpt.markdown("<h3 style='text-align:center;'>Autenticação Corporativa</h3>", unsafe_allow_html=True)
    with strpt.form("login_rh"):
        usuario = strpt.text_input("Usuário Corporativo", placeholder="admin")
        senha = strpt.text_input("Senha", type="password", placeholder="••••••••")
        entrar = strpt.form_submit_button("Acessar Painel")
        
        if entrar:
            if usuario == "admin" and senha == "starplast2026":
                strpt.session_state["autenticado"] = True
                strpt.success("Acesso liberado!")
                time.sleep(0.5)
                strpt.rerun()
            else:
                strpt.error("Credenciais incorretas.")

    strpt.markdown("<p style='text-align: center;'><a href='/' target='_self' style='color: #004AAD;'>← Voltar ao Portal</a></p>", unsafe_allow_html=True)

# PAINEL DO RH
else:
    c_user, c_out = strpt.columns([3, 1])
    with c_user:
        strpt.markdown("🔒 Sessão Ativa: **Administrador (RH)**")
    with c_out:
        if strpt.button("🚪 Sair"):
            strpt.session_state["autenticado"] = False
            strpt.rerun()
            
    strpt.divider()
    
    aba_lista, aba_eva = strpt.tabs(["📋 Fila de Candidatos", "🤖 Assistente Eva"])
    
    # CARREGA OS DADOS SALVOS NO DISCO
    cand_lista = carregar_dados()
    
    with aba_lista:
        strpt.markdown(f"**{len(cand_lista)} candidato(s)** cadastrado(s) no sistema.")
        
        if not cand_lista:
            strpt.info("Nenhum cadastro encontrado no banco de dados.")
        else:
            for i, c in enumerate(cand_lista):
                col_txt, col_scr = strpt.columns([3, 1])
                with col_txt:
                    strpt.markdown(f"#### {c['nome']}")
                    strpt.caption(f"📍 {c['cidade']} | 💼 Alvo: {c['setor']}")
                with col_scr:
                    strpt.markdown(f'<div class="score-box">MATCH<br><span style="font-size:1.3rem;">{c["score"]}%</span></div>', unsafe_allow_html=True)
                    
                strpt.markdown(f"**Objetivo:** {c['objetivo']}")
                strpt.markdown(f"**Formação:** {c['formacao']}")
                strpt.markdown(f"**Resumo:** {c['resumo']}")
                strpt.caption(f"📧 {c['email']} | 📞 {c['telefone']}")
                strpt.text_area("Observações:", key=f"nota_{i}")
                strpt.divider()
                
    with aba_eva:
        strpt.markdown("#### Copiloto da Banca de Seleção — Eva")
        for msg in strpt.session_state["historico_eva"]:
            with strpt.chat_message(msg["role"]):
                strpt.write(msg["content"])

        if q := strpt.chat_input("Pergunte algo sobre os candidatos..."):
            with strpt.chat_message("user"):
                strpt.write(q)
            strpt.session_state["historico_eva"].append({"role": "user", "content": q})
            
            q_low = q.lower()
            if not cand_lista:
                resp = "Não há candidatos salvos no banco de dados para analisar."
            elif any(termo in q_low for termo in ["melhor", "indica", "score", "top"]):
                top_cand = max(cand_lista, key=lambda x: x["score"])
                resp = f"O candidato em destaque é **{top_cand['nome']}** com Match Score de **{top_cand['score']}%**."
            elif any(termo in q_low for termo in ["quantos", "total", "lista"]):
                nomes = "\n".join([f"- **{c['nome']}** ({c['setor']})" for c in cand_lista])
                resp = f"Temos **{len(cand_lista)} candidato(s)** salvos:\n\n{nomes}"
            else:
                encontrados = [c for c in cand_lista if q_low in c['resumo'].lower() or q_low in c['setor'].lower() or q_low in c['cidade'].lower()]
                if encontrados:
                    nomes_f = ", ".join([c['nome'] for c in encontrados])
                    resp = f"Encontrei **{len(encontrados)} perfil(is)** correspondente(s): **{nomes_f}**."
                else:
                    resp = f"Não encontrei o termo '{q}' no histórico dos cadastros salvos."

            with strpt.chat_message("assistant"):
                strpt.write(resp)
            strpt.session_state["historico_eva"].append({"role": "assistant", "content": resp})
            strpt.rerun()