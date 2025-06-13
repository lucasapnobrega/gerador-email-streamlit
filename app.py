import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io
from fpdf import FPDF
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="Consultor de E-mails Profissionais",
    page_icon="📧",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>📧 Consultor de E-mails Profissionais</h1>", unsafe_allow_html=True)
st.markdown("---")

def gerar_prompt_melhoria_email(rascunho, tom, idioma):    
    instrucoes_tom = {
        "formal": "Use linguagem formal, tratamento respeitoso, evite contrações e gírias. Adicione cumprimentos e fechamentos apropriados para contexto corporativo.",
        "amigável": "Use linguagem calorosa e acessível, mas mantenha profissionalismo. Pode usar contrações moderadas e tom mais pessoal.",
        "assertivo": "Use linguagem direta, confiante e objetiva. Evite hesitações e seja claro nas solicitações."
    }

    instrucoes_idioma = {
        "português": "Responda inteiramente em português.",
        "inglês": "Respond entirely in English.",
        "espanhol": "Redacta absolutamente todo en español, sin ninguna palabra en portugués o inglés. Esto incluye encabezados, explicaciones y todo el contenido del correo."
    }
    
    prompt = f"""
        Você é um especialista em comunicação profissional. Sua tarefa é revisar e aperfeiçoar o seguinte rascunho de e-mail:

        RASCUNHO ORIGINAL:
        {rascunho}

        INSTRUÇÕES:
        1. Revise o e-mail aplicando o tom {tom}: {instrucoes_tom[tom]}
        2. Corrija erros gramaticais, ortográficos e de pontuação
        3. Melhore a clareza e estrutura do texto
        4. Substitua abreviações informais por termos profissionais (ex: vc → você, obg → obrigado)
        5. Adicione cumprimentos e fechamentos apropriados se necessário
        6. {instrucoes_idioma[idioma]}

        FORMATO DA RESPOSTA:
        Forneça sua resposta em duas seções claramente separadas:

        **E-MAIL REVISADO:**
        [Aqui coloque a versão melhorada do e-mail]

        **SUGESTÕES E EXPLICAÇÕES:**
        [Aqui liste as principais melhorias feitas e o porquê de cada uma, em formato de lista com bullets]
    """
    return prompt

def gerar_prompt_por_objetivo(objetivo, tom, idioma):
    instrucoes_tom = {
        "formal": "Use linguagem formal e apropriada para o ambiente corporativo.",
        "amigável": "Use linguagem acessível e gentil, mantendo o profissionalismo.",
        "assertivo": "Use linguagem objetiva e confiante, sem rodeios."
    }

    instrucoes_idioma = {
        "português": "Escreva todo o e-mail em português.",
        "inglês": "Write the entire email in English.",
        "espanhol": "Escribe todo el correo en español, sin usar portugués ni inglés."
    }

    prompt = f"""
    Você é um especialista em comunicação por e-mail. Crie um e-mail profissional com base no seguinte objetivo descrito pelo usuário:

    OBJETIVO:
    {objetivo}

    INSTRUÇÕES:
    - Siga o tom {tom}: {instrucoes_tom[tom]}
    - {instrucoes_idioma[idioma]}
    - Inclua uma saudação e uma despedida adequadas.
    - Mantenha o texto claro, conciso e bem estruturado.

    FORMATO DA RESPOSTA:
    **E-MAIL GERADO:**
    [Escreva aqui o e-mail gerado]
    """
    return prompt

def processar_email_com_gemini(rascunho, tom, idioma):
    try:
        api_key = st.secrets["API_KEY"]
        genai.configure(api_key=api_key)
        modelo = genai.GenerativeModel('gemini-1.5-flash')
        
        if aba == "✏️ Melhorar rascunho":
            prompt = gerar_prompt_melhoria_email(rascunho, tom, idioma)
        else:
            prompt = gerar_prompt_por_objetivo(rascunho, tom, idioma)
        
        resposta = modelo.generate_content(prompt)
        return resposta.text

    except Exception as erro:
        raise Exception(f"Erro ao processar com Gemini AI: {str(erro)}")

def extrair_resposta_gemini(texto_resposta):
    try:
        separadores = [
            "**SUGESTÕES E EXPLICAÇÕES:**",
            "**SUGGESTIONS AND EXPLANATIONS:**",
            "**SUGERENCIAS Y EXPLICACIONES:**"
        ]

        for separador in separadores:
            if separador in texto_resposta:
                partes = texto_resposta.split(separador)
                if len(partes) == 2:
                    email_revisado = partes[0].replace("**E-MAIL REVISADO:**", "").replace("**REVISED EMAIL:**", "").strip()
                    sugestoes = partes[1].strip()

                    return email_revisado, sugestoes

        return texto_resposta, "❗ Não foi possível separar as sugestões."

    except Exception as erro:
        return texto_resposta, f"Erro ao interpretar resposta: {str(erro)}"

email_final = ""

def gerar_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    linhas = texto.split('\n')
    for linha in linhas:
        pdf.multi_cell(0, 10, linha)

    pdf_bytes = pdf.output(dest='S').encode('latin1')

    return pdf_bytes

aba = st.radio("Escolha o modo:", ["✏️ Melhorar rascunho", "🧠 Gerar por objetivo"], horizontal=True)

if 'ultima_aba' not in st.session_state:
    st.session_state['ultima_aba'] = aba
elif st.session_state['ultima_aba'] != aba:
    st.session_state['email_final'] = ""
    st.session_state['sugestoes'] = ""
    st.session_state['ultima_aba'] = aba

col1, col2 = st.columns([1, 1])

with col1:
    if aba == "✏️ Melhorar rascunho":
        st.markdown("### 📝 Seu Rascunho")
        rascunho_email = st.text_area(
            "Digite seu rascunho de e-mail:", 
            height=200, 
            placeholder="Cole ou digite seu rascunho de email aqui..."
        )
    else:
        st.markdown("### 🎯 Objetivo do E-mail")
        objetivo_email = st.text_area(
            "Descreva o objetivo ou palavras-chave:", 
            height=200, 
            placeholder="Cole ou digite seu objetivo aqui..."
        )

    tom = st.selectbox(
        "Escolha o tom:",
        ["formal", "amigável", "assertivo"],
        format_func=lambda x: {
            "formal": "🎩 Formal",
            "amigável": "😊 Amigável",
            "assertivo": "💪 Assertivo"
        }[x]
    )

    idioma = st.selectbox(
        "Escolha o idioma de saída:",
        ["português", "inglês", "espanhol"],
        format_func=lambda x: {
            "português": "🇧🇷 Português (padrão)",
            "inglês": "🇺🇸 Inglês",
            "espanhol": "🇪🇸 Espanhol"
        }[x],
    )

    botao_processar = st.button(
        "🔄 Revisar e Aperfeiçoar",
        type="primary",
        use_container_width=True
    )

with col2:
    st.markdown("### 📬 Resultado")

    if aba == "✏️ Melhorar rascunho":
        if not rascunho_email.strip():
            st.info("👈 Digite seu rascunho de e-mail para ver o resultado")
        elif botao_processar:
            with st.spinner("Gerando e-mail..."):
                try:
                    resposta = processar_email_com_gemini(rascunho_email, tom, idioma)
                    email_final, sugestoes = extrair_resposta_gemini(resposta)
                    st.session_state['email_final'] = email_final
                    st.session_state['sugestoes'] = sugestoes
                    st.success("✅ E-mail processado com sucesso!")
                except Exception as erro:
                    st.error(f"❌ Erro ao processar: {str(erro)}")
    else:
        if not objetivo_email.strip():
            st.info("👈 Descreva o objetivo do e-mail para ver o resultado")
        elif botao_processar:
            with st.spinner("Gerando e-mail..."):
                try:                    
                    texto = processar_email_com_gemini(objetivo_email, tom, idioma)
                    email_final = texto.split("**E-MAIL GERADO:**")[-1].strip()

                    st.session_state['email_final'] = email_final
                    st.session_state['sugestoes'] = "ℹ️ Gerado diretamente a partir do objetivo informado."
                    st.success("✅ E-mail gerado com sucesso!")
                except Exception as erro:
                    st.error(f"❌ Erro ao gerar: {str(erro)}")

    if 'email_final' in st.session_state and st.session_state['email_final']:
        st.markdown("#### 📧 E-mail Gerado:")
        st.text_area("Resultado:", value=st.session_state['email_final'], height=350, disabled=True)

        if aba == "✏️ Melhorar rascunho":
            st.markdown("#### 💡 Sugestões:")
            st.markdown(st.session_state['sugestoes'])

        pdf_bytes = gerar_pdf(st.session_state['email_final'])
        txt_bytes = st.session_state['email_final'].encode('utf-8')

        st.download_button(
            label="⬇️ Baixar e-mail (.txt)",
            data=txt_bytes,
            file_name=f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        st.download_button(
            label="⬇️ Baixar e-mail (.pdf)",
            data=pdf_bytes,
            file_name=f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.9rem;'>
        Desenvolvido usando <strong>Streamlit</strong> e <strong>Google Gemini AI</strong>
    </div>
    """,
    unsafe_allow_html=True
)