import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Consultor de E-mails Profissionais",
    page_icon="📧",
    layout="wide"
)

def gerar_prompt_melhoria_email(rascunho, tom):    
    instrucoes_tom = {
        "formal": "Use linguagem formal, tratamento respeitoso, evite contrações e gírias. Adicione cumprimentos e fechamentos apropriados para contexto corporativo.",
        "amigável": "Use linguagem calorosa e acessível, mas mantenha profissionalismo. Pode usar contrações moderadas e tom mais pessoal.",
        "assertivo": "Use linguagem direta, confiante e objetiva. Evite hesitações e seja claro nas solicitações."
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

        FORMATO DA RESPOSTA:
        Forneça sua resposta em duas seções claramente separadas:

        **E-MAIL REVISADO:**
        [Aqui coloque a versão melhorada do e-mail]

        **SUGESTÕES E EXPLICAÇÕES:**
        [Aqui liste as principais melhorias feitas e o porquê de cada uma, em formato de lista com bullets]
    """
    return prompt

def processar_email_com_gemini(rascunho, tom):
    try:
        api_key = st.secrets["API_KEY"]
        genai.configure(api_key=api_key)
        modelo = genai.GenerativeModel('gemini-1.5-flash')

        prompt = gerar_prompt_melhoria_email(rascunho, tom)
        resposta = modelo.generate_content(prompt)
        return resposta.text

    except Exception as erro:
        raise Exception(f"Erro ao processar com Gemini AI: {str(erro)}")

def extrair_resposta_gemini(texto_resposta):
    try:
        partes = texto_resposta.split("**SUGESTÕES E EXPLICAÇÕES:**")

        if len(partes) == 2:
            email_revisado = partes[0].replace("**E-MAIL REVISADO:**", "").strip()
            sugestoes = partes[1].strip()
            return email_revisado, sugestoes
        else:
            return texto_resposta, "❗ Não foi possível separar as sugestões."
            
    except Exception as erro:
        return texto_resposta, f"Erro ao interpretar resposta: {str(erro)}"

st.markdown("<h1 style='text-align: center;'>📧 Consultor de E-mails Profissionais</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Seu Rascunho")
    rascunho_email = st.text_area(
        "Digite seu rascunho de e-mail:",
        height=200,
        placeholder="Cole ou digite seu rascunho de e-mail aqui..."
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

    botao_processar = st.button(
        "🔄 Revisar e Aperfeiçoar",
        type="primary",
        use_container_width=True
    )

with col2:
    st.markdown("### ✨ Resultado")

    if not rascunho_email.strip():
        st.info("👈 Digite seu rascunho de e-mail para ver o resultado")
    else:
        if botao_processar:
            with st.spinner("🤖 Processando seu texto..."):
                try:
                    resposta = processar_email_com_gemini(rascunho_email, tom)
                    email_final, sugestoes = extrair_resposta_gemini(resposta)

                    st.success("✅ E-mail processado com sucesso!")

                    st.markdown("#### 📧 E-mail Revisado:")
                    st.text_area(
                        "Resultado:",
                        value=email_final,
                        height=350,
                        disabled=True
                    )

                    st.markdown("#### 💡 Sugestões de Melhoria:")
                    st.markdown(sugestoes)

                except Exception as erro:
                    st.error(f"❌ Erro ao processar: {str(erro)}")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.9rem;'>
        Desenvolvido usando <strong>Streamlit</strong> e <strong>Google Gemini AI</strong>
    </div>
    """,
    unsafe_allow_html=True
)