# Consultor de E-mails Profissionais

Uma ferramenta web desenvolvida com **Python**, **Streamlit** e **Google Gemini AI** que transforma rascunhos de e-mail em versões profissionais, claras e objetivas.

## 🚀 Funcionalidades

- **Interface intuitiva**: Desenvolvida com Streamlit para facilidade de uso.
- **Integração com Gemini AI**: Usa inteligência artificial avançada para revisão de texto.
- **Múltiplos tons**: Escolha entre formal, amigável ou assertivo.
- **Idioma**: Escolha entre Português, Inglês ou Espanhol.
- **Baixar o email revisado**: Baixar arquivo .txt ou .pdf.
- **Gerar revisão de email ou por objetivo**: Poder de escolha entre enviar um e-mail ou enviar palavras chaves/objetivo.
- **Correções automáticas**: Substitui abreviações informais por termos profissionais.
- **Sugestões detalhadas**: Explica todas as melhorias aplicadas.
- **Interface responsiva**: Funciona bem em desktop e mobile.

## 📁 Estrutura do projeto

```
email_consultant_streamlit/
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências Python
└── README.md           # Este arquivo
```

## 🔧 Dependências

- **streamlit**: Framework para interface web
- **google-generativeai**: SDK oficial do Google Gemini AI
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **fpdf**: Download de PDF.

## 💡 Exemplos de uso

### Entrada (informal):
```
oi, vc pode me mandar o relatório? obg, preciso dele pra reunião de amanhã
```

### Saída (formal):
```
Prezado(a),

Você poderia me enviar o relatório? Agradeço antecipadamente, pois preciso dele para a reunião de amanhã.

Atenciosamente,
```

## 🎯 Desenvolvido com

- **Python 3.11**
- **Streamlit 1.28.1**
- **Google Gemini AI**

---

**Nota**: Esta ferramenta requer uma chave da API do Google Gemini AI para funcionar.

