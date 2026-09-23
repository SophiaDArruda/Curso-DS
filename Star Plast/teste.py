import streamlit as strpt
import random
import time

# Configuração global da página para o ecossistema Maroon 4
strpt.set_page_config(page_title="Star Plast - AI Human Capital Suite", layout="wide")

# --- DESIGN SYSTEM EM CSS (Visual Limpo, Moderno e Profissional) ---
strpt.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Inter', sans-serif !important; }
        .stApp { background-color: #F8FAFC; }
        
        /* Estilização dos blocos de currículo (Folha Limpa) */
        .resume-paper {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 35px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
            margin-top: 15px;
        }
        .resume-title {
            color: #1E3A8A;
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 4px;
            margin-top: 18px;
            margin-bottom: 6px;
        }
        .resume-desc {
            color: #334155;
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
            white-space: pre-wrap;
        }
        
        /* Caixa do Parecer da IA Eva */
        .eva-box {
            background: linear-gradient(135deg, #F0FDF4 0%, #E8F5E9 100%);
            border: 1px solid #BBF7D0;
            padding: 18px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        
        /* Histórico de Notificação de Feedback */
        .feedback-alert {
            background-color: #EFF6FF;
            border-left: 4px solid #3B82F6;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS E MEMÓRIA DE SESSÃO GLOBAL ---
if "banco_talentos" not in strpt.session_state:
    strpt.session_state["banco_talentos"] = [
        {
            "id": 1,
            "nome": "Antonio da Silva",
            "email": "antonio.silva@gmail.com",
            "telefone": "+55 11 99123-4567",
            "cidade": "Campinas - SP",
            "setor": "Tecnologia da Informação (T.I)",
            "formacao": "T.I - Unicamp",
            "objetivo": "Atuar no desenvolvimento de sistemas e automação industrial.",
            "resumo": "Experiência de 2009-2015 em uma empresa de marketing digital atuando diretamente com infraestrutura corporativa, segurança de dados e modelagem SQL.",
            "genero": "Masculino",
            "score": 95,
            "status": "Aguardando Análise",
            "feedback_texto": "",
            "nascimento": "18/01/1994"
        },
        {
            "id": 2,
            "nome": "Ana Maria Arruda de Oliveira",
            "email": "ana.arruda@gmail.com",
            "telefone": "+55 11 98888-7777",
            "cidade": "Jundiaí - SP",
            "setor": "Operações / Produção",
            "formacao": "Técnico em Logística - SENAI",
            "objetivo": "Busco atuar na otimização de fluxos de estoque e expedição industrial.",
            "resumo": "Experiência de 3 anos liderando inventários rotativos, conferência de entrada de insumos plásticos e paletização automatizada.",
            "genero": "Feminino",
            "score": 88,
            "status": "Aguardando Análise",
            "feedback_texto": "",
            "nascimento": "05/11/1997"
        }
    ]

if "rh_logado" not in strpt.session_state:
    strpt.session_state["rh_logado"] = False
if "chat_candidato" not in strpt.session_state:
    strpt.session_state["chat_candidato"] = []
if "chat_rh" not in strpt.session_state:
    strpt.session_state["chat_rh"] = []

# --- MENU LATERAL DE SEPARAÇÃO TOTAL DE DOMÍNIOS ---
strpt.sidebar.markdown(
    """
    <div style='padding: 5px 0px; margin-bottom: 15px; border-bottom: 1px solid #E2E8F0;'>
        <h3 style='color: #0F172A; margin: 0; font-size: 1.2rem; letter-spacing: -0.5px;'>STAR PLAST</h3>
        <p style='color: #64748B; margin: 2px 0 0 0; font-size: 0.7rem; text-transform: uppercase; font-weight: 600;'>Plataforma Maroon 4</p>
    </div>
    """, unsafe_allow_html=True
)

dominio = strpt.sidebar.selectbox("Mudar de Domínio (Ambiente):", [
    "🌐 portal-candidato.starplast.com",
    "🔒 intranet-rh.starplast.internal"
])

# -----------------------------------------------------------------------------------------
# AMBIENTE 1: PORTAL DO CANDIDATO (CLIENTE EXTERNO)
# -----------------------------------------------------------------------------------------
if dominio == "🌐 portal-candidato.starplast.com":
    aba_cand = strpt.sidebar.radio("Navegação do Candidato:", ["📝 Enviar Currículo", "🔍 Acompanhar Status", "🤖 Conversar com a Eva"])
    
    if aba_cand == "📝 Enviar Currículo":
        strpt.markdown(
            """
            <div style="background-color: #FFFFFF; padding: 25px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px;">
                <h2 style="margin: 0; font-size: 1.5rem; color: #0F172A;">Cadastro no Banco de Talentos</h2>
                <p style="color: #475569; margin: 4px 0 0 0; font-size: 0.9rem;">Seus dados serão processados instantaneamente por inteligência artificial.</p>
            </div>
            """, unsafe_allow_html=True
        )
        
        with strpt.form("cadastro_cliente", clear_on_submit=True):
            strpt.markdown("<h4>1. Identificação Pessoal</h4>", unsafe_allow_html=True)
            col1, col2 = strpt.columns(2)
            with col1:
                n_nome = strpt.text_input("Nome Completo")
                n_cidade = strpt.text_input("Cidade e Estado")
                n_genero = strpt.selectbox("Gênero", ["Masculino", "Feminino", "Não Informar"])
            with col2:
                n_email = strpt.text_input("E-mail")
                n_telef = strpt.text_input("Telefone Fone", placeholder="(XX) XXXXX-XXXX")
                n_nasc = strpt.text_input("Data de Nascimento", placeholder="DD/MM/AAAA")
                
            strpt.markdown("<br><h4>2. Dados Profissionais</h4>", unsafe_allow_html=True)
            n_setor = strpt.selectbox("Setor de Interesse", ["Tecnologia da Informação (T.I)", "Marketing Digital", "Recursos Humanos", "Operações / Produção"])
            n_obj = strpt.text_input("Objetivo Curto")
            n_form = strpt.text_area("Formação Acadêmica")
            n_res = strpt.text_area("Experiências Profissionais")
            
            strpt.markdown("---")
            concorda = strpt.checkbox("Autorizo a Star Plast a armazenar e processar meus dados nos termos da LGPD.")
            
            _, b_col = strpt.columns([4, 1])
            with b_col:
                btn_cad = strpt.form_submit_button("Submeter", use_container_width=True)
                
            if btn_cad:
                if not n_nome or not n_email or not n_res:
                    strpt.error("🚨 Preencha todos os campos obrigatórios para análise.")
                elif not concorda:
                    strpt.error("🚨 Você deve aceitar as diretrizes da LGPD.")
                else:
                    score_rand = random.randint(50, 82)
                    if "unicamp" in n_form.lower() or "senai" in n_form.lower():
                        score_rand += 15
                    
                    novo_registro = {
                        "id": len(strpt.session_state["banco_talentos"]) + 1,
                        "nome": n_nome, "email": n_email, "telefone": n_telef, "cidade": n_cidade,
                        "setor": n_setor, "formacao": n_form, "objetivo": n_obj, "resumo": n_res,
                        "genero": n_genero, "score": min(score_rand, 100), "status": "Aguardando Análise",
                        "feedback_texto": "", "nascimento": n_nasc
                    }
                    strpt.session_state["banco_talentos"].append(novo_registro)
                    strpt.success("🎉 Seu currículo foi recebido e já está na fila de triagem da IA!")

    elif aba_cand == "🔍 Acompanhar Status":
        strpt.markdown("<h2>Painel de Transparência do Candidato</h2>", unsafe_allow_html=True)
        email_busca = strpt.text_input("Digite o e-mail cadastrado para verificar seu retorno:")
        
        if email_busca:
            match = [c for c in strpt.session_state["banco_talentos"] if c["email"].lower() == email_busca.lower()]
            if match:
                cand = match[0]
                strpt.info(f"📋 **Candidato:** {cand['nome']} | **Setor:** {cand['setor']}")
                strpt.success(f"📊 **Status Atual da Candidatura:** {cand['status']}")
                
                if cand["feedback_texto"]:
                    strpt.markdown(
                        f"""
                        <div class="feedback-alert">
                            <strong>✉️ Retorno Oficial do departamento de RH:</strong><br>
                            <p style="margin: 5px 0 0 0; color: #1E3A8A; font-style: italic;">"{cand['feedback_texto']}"</p>
                        </div>
                        """, unsafe_allow_html=True
                    )
                else:
                    strpt.caption("Seu perfil está em fase de triagem pela Inteligência Artificial. Você receberá o feedback assim que o recrutador concluir a análise.")
            else:
                strpt.error("Nenhum currículo associado a este e-mail foi encontrado no sistema.")

    elif aba_cand == "🤖 Conversar com a Eva":
        strpt.markdown("<h2>Conversar com a Assistente de Carreira Eva</h2>", unsafe_allow_html=True)
        h_cand = strpt.session_state["chat_candidato"]
        if not h_cand:
            h_cand.append({"role": "assistant", "content": "Olá! Sou a Eva, assistente virtual da Star Plast. Posso tirar dúvidas sobre os nossos benefícios ou sobre como funciona nossa triagem de talentos. O que deseja saber?"})
            
        for m in h_cand:
            with strpt.chat_message(m["role"]):
                strpt.write(m["content"])
                
        if p_cand := strpt.chat_input("Pergunte algo para a Eva..."):
            with strpt.chat_message("user"):
                strpt.write(p_cand)
            h_cand.append({"role": "user", "content": p_cand})
            
            low = p_cand.lower()
            with strpt.chat_message("assistant"):
                if "benefic" in low or "vale" in low or "plano" in low:
                    resp = "Oferecemos refeitório corporativo na fábrica, assistência médica, odontológica e vale-alimentação estruturado."
                elif "vaga" in low or "produção" in low or "t.i" in low:
                    resp = "Temos oportunidades ativas para a área de Tecnologia e Operações Industriais. Candidate-se enviando seu currículo na aba correspondente!"
                elif "oi" in low or "olá" in low:
                    resp = "Olá! Como posso te ajudar na sua jornada profissional hoje?"
                else:
                    resp = "Excelente ponto! Minha inteligência arquivou sua dúvida. Lembre-se de preencher seus dados no portal para triagem eletrônica."
                strpt.write(resp)
            h_cand.append({"role": "assistant", "content": resp})
            strpt.rerun()

# -----------------------------------------------------------------------------------------
# AMBIENTE 2: INTRANET INTERNA DO RH (PROTÓTIPO MAROON 4 COMPLETO)
# -----------------------------------------------------------------------------------------
else:
    if not strpt.session_state["rh_logado"]:
        _, c_login, _ = strpt.columns([1.2, 1, 1.2])
        with c_login:
            strpt.markdown("<br><br>", unsafe_allow_html=True)
            with strpt.form("login_painel_rh"):
                strpt.markdown("<h3 style='text-align:center;'>Acesso Administrativo - RH</h3>", unsafe_allow_html=True)
                adm_email = strpt.text_input("E-mail do Recrutador")
                adm_senha = strpt.text_input("Senha", type="password")
                if strpt.form_submit_button("Entrar", use_container_width=True):
                    if adm_email == "rh@starplast.com.br" and adm_senha == "star2026":
                        strpt.session_state["rh_logado"] = True
                        strpt.rerun()
                    else:
                        strpt.error("Acesso negado.")
    else:
        aba_rh = strpt.sidebar.radio("Menu do Recrutador:", ["📋 Analisar Currículos", "🤖 Copiloto IA (RH)"])
        
        if strpt.sidebar.button("🚪 Sair da Intranet"):
            strpt.session_state["rh_logado"] = False
            strpt.rerun()
            
        if aba_rh == "📋 Analisar Currículos":
            strpt.markdown("<h2>Painel do Recrutador - Gestão de Atração de Talentos</h2>", unsafe_allow_html=True)
            
            c_filtros, c_visualizar = strpt.columns([1.1, 2.3])
            
            with c_filtros:
                strpt.markdown("<div style='background-color: #FFFFFF; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
                strpt.markdown("<h4 style='margin:0 0 10px 0; font-size:1rem; color:#475569;'>Filtros do Protótipo</h4>", unsafe_allow_html=True)
                filtro_setor = strpt.selectbox("Filtrar por Setor:", ["Todos", "Tecnologia da Informação (T.I)", "Marketing Digital", "Recursos Humanos", "Operações / Produção"])
                filtro_genero = strpt.radio("Filtrar por Gênero:", ["Todos", "Masculino", "Feminino"])
                filtro_top = strpt.checkbox("⭐ Melhores Candidatos (>80% Match)")
                filtro_az = strpt.checkbox("🔤 Ordenação Alfabética (A-Z)")
                strpt.markdown("</div>", unsafe_allow_html=True)
                
                # Regras de filtragem baseadas no protótipo Maroon 4
                base = strpt.session_state["banco_talentos"]
                if filtro_setor != "Todos":
                    base = [b for b in base if b["setor"] == filtro_setor]
                if filtro_genero != "Todos":
                    base = [b for b in base if b["genero"] == filtro_genero]
                if filtro_top:
                    base = [b for b in base if b["score"] >= 80]
                if filtro_az:
                    base = sorted(base, key=lambda x: x["nome"])
                    
                strpt.markdown("<br><p style='font-size:0.9rem; font-weight:600; color:#64748B; margin-bottom:5px;'>Selecione o Currículo:</p>", unsafe_allow_html=True)
                if not base:
                    strpt.caption("Nenhum candidato encontrado com estes critérios.")
                    escolhido = None
                else:
                    nomes_disponiveis = [b["nome"] for b in base]
                    selecionado_nome = strpt.radio("Fila:", nomes_disponiveis, label_visibility="collapsed")
                    escolhido = next(b for b in base if b["nome"] == selecionado_nome)
                    
            with c_visualizar:
                if escolhido:
                    # Geração dinâmica do parecer da IA Eva
                    pontos_fortes = "Forte domínio conceitual e ótima aderência técnica para o ecossistema Star Plast." if escolhido["score"] >= 90 else "Boa capacitação inicial, apto para triagem inicial de competências."
                    
                    strpt.markdown(
                        f"""
                        <div class="eva-box">
                            <h4 style="margin: 0 0 5px 0; color: #166534; font-size:0.95rem;">🤖 Parecer Analítico: Assistente Eva</h4>
                            <p style="margin: 0; font-size:0.9rem; color:#1E293B;"><strong>Métricas de Análise:</strong> {pontos_fortes}</p>
                            <div style="background-color: #FFFFFF; padding: 6px 12px; border-radius: 4px; margin-top: 8px; border-left: 3px solid #16A34A;">
                                <span style="font-size:0.85rem; font-weight:600; color:#0F172A;">Recomendação IA: Perfil compatível em {escolhido['score']}% com a vaga de {escolhido['setor']}.</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                    
                    # Alteração "Telefone:" e "E-mail:" aplicada aqui!
                    strpt.markdown(
                        f"""
                        <div class="resume-paper">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #F1F5F9; padding-bottom: 15px;">
                                <div>
                                    <h2 style="margin: 0 0 4px 0; font-size: 1.5rem; color: #0F172A;">Nome: {escolhido['nome']}</h2>
                                    <span style="color: #64748B; font-size: 0.85rem;">📍 Localização: {escolhido['cidade']} &nbsp;|&nbsp; 🎂 Nascimento: {escolhido['nascimento']}</span>
                                </div>
                                <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 6px 12px; border-radius: 6px; text-align: center;">
                                    <span style="font-size: 0.65rem; font-weight: 700; color: #1E40AF; text-transform: uppercase; display: block;">Match Score</span>
                                    <strong style="font-size: 1.3rem; color: #1D4ED8;">{escolhido['score']}%</strong>
                                </div>
                            </div>
                            
                            <div class="resume-title">Formação</div>
                            <p class="resume-desc">{escolhido['formacao']}</p>
                            
                            <div class="resume-title">Experiência</div>
                            <p class="resume-desc">{escolhido['resumo']}</p>
                            
                            <div style="margin-top: 25px; padding-top: 15px; border-top: 1px solid #E2E8F0; font-size: 0.85rem; color: #64748B;">
                                📞 <strong>Telefone:</strong> {escolhido['telefone']} &nbsp;|&nbsp; ✉️ <strong>E-mail:</strong> {escolhido['email']} &nbsp;|&nbsp; ⚙️ <strong>Status:</strong> {escolhido['status']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                    
                    # SISTEMA DE REALIMENTAÇÃO DE FEEDBACKS REALISTA
                    strpt.markdown("<br>", unsafe_allow_html=True)
                    feedback_input = strpt.text_area("Escreva a justificativa ou feedback de retorno ao candidato:", placeholder="Escreva aqui as observações que o candidato lerá no painel dele...")
                    
                    col_b1, col_b2, _ = strpt.columns([1, 1, 1.5])
                    with col_b1:
                        if strpt.button("✔️ Aprovar e Chamar", use_container_width=True):
                            escolhido["status"] = "Aprovado para Entrevista"
                            escolhido["feedback_texto"] = feedback_input if feedback_input else "Seu perfil foi qualificado positivamente na triagem Star Plast. Entraremos em contato para agendar a entrevista presencial."
                            strpt.success("Candidato aprovado! Notificação vinculada com sucesso.")
                            time.sleep(0.5)
                            strpt.rerun()
                    with col_b2:
                        if strpt.button("❌ Marcar Incompatível", use_container_width=True):
                            escolhido["status"] = "Não Classificado"
                            escolhido["feedback_texto"] = feedback_input if feedback_input else "Agradecemos sua participação. Identificamos que sua trajetória atual diverge de alguns critérios técnicos exigidos para esta vaga."
                            strpt.warning("Candidato movido para a lista de Não Aceitos.")
                            time.sleep(0.5)
                            strpt.rerun()
                else:
                    strpt.info("Selecione um candidato na listagem para inspecionar os dados.")
                    
        elif aba_rh == "🤖 Copiloto IA (RH)":
            strpt.markdown("<h2>Central Eva: Copiloto Estratégico de RH</h2>", unsafe_allow_html=True)
            h_rh = strpt.session_state["chat_rh"]
            if not h_rh:
                h_rh.append({"role": "assistant", "content": "Olá, recrutador! Sou a Eva. Posso sugerir dinâmicas, perguntas de entrevista focadas no padrão Maroon 4 ou trazer relatórios rápidos sobre os scores mais altos. Como posso ajudar?"})
                
            for m in h_rh:
                with strpt.chat_message(m["role"]):
                    strpt.write(m["content"])
                    
            if p_rh := strpt.chat_input("Solicite orientações de triagem à Eva..."):
                with strpt.chat_message("user"):
                    strpt.write(p_rh)
                h_rh.append({"role": "user", "content": p_rh})
                
                low_rh = p_rh.lower()
                with strpt.chat_message("assistant"):
                    if "pergunta" in low_rh or "roteiro" in low_rh or "entrevista" in low_rh:
                        resp = "Para as vagas técnicas industriais, recomendo: 1) 'Como era feito o controle de refugo e avarias nas máquinas anteriores?' e 2) 'Descreva sua rotina com normas de segurança do trabalho e EPIs'."
                    elif "melhor" in low_rh or "indica" in low_rh or "score" in low_rh:
                        resp = "Atualmente, o candidato Antonio da Silva apresenta o maior match score da base ativa (95%), devido à formação acadêmica alinhada na Unicamp."
                    elif "oi" in low_rh or "olá" in low_rh:
                        resp = "Olá, recrutador! Como posso auxiliar nas tomadas de decisão de contratação hoje?"
                    else:
                        resp = "Compreendido. Diretriz registrada para otimização dos parâmetros de leitura de currículos corporativos da Star Plast."
                    strpt.write(resp)
                h_rh.append({"role": "assistant", "content": resp})
                strpt.rerun()