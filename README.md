# Consultor de E-mails Profissionais

Uma ferramenta web desenvolvida com **Python**, **Streamlit** e **Google Gemini AI** que transforma rascunhos de e-mail em versões profissionais, claras e objetivas.

## 🚀 Funcionalidades

- **Interface intuitiva**: Desenvolvida com Streamlit para facilidade de uso
- **Integração com Gemini AI**: Usa inteligência artificial avançada para revisão de texto
- **Múltiplos tons**: Escolha entre formal, amigável ou assertivo
- **Correções automáticas**: Substitui abreviações informais por termos profissionais
- **Sugestões detalhadas**: Explica todas as melhorias aplicadas
- **Interface responsiva**: Funciona bem em desktop e mobile

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Chave da API do Google Gemini AI

## 🔧 Instalação

1. **Clone ou extraia o projeto**
   ```bash
   cd email_consultant_streamlit
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Obtenha sua chave da API Gemini**
   - Acesse: https://makersuite.google.com/app/apikey
   - Crie uma conta Google se necessário
   - Gere uma nova chave da API
   - Guarde a chave para usar na aplicação

## 🚀 Como usar

1. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

2. **Acesse no navegador**
   - A aplicação abrirá automaticamente em `http://localhost:8501`
   - Ou acesse manualmente o endereço

3. **Configure a API**
   - Na barra lateral, insira sua chave da API Gemini
   - Aguarde a confirmação de configuração

4. **Use a ferramenta**
   - Digite seu rascunho de e-mail
   - Escolha o tom desejado (formal, amigável, assertivo)
   - Clique em "Revisar e Aperfeiçoar"
   - Veja o resultado e as sugestões!

## 📁 Estrutura do projeto

```
email_consultant_streamlit/
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências Python
└── README.md          # Este arquivo
```

## 🔧 Dependências

- **streamlit**: Framework para interface web
- **google-generativeai**: SDK oficial do Google Gemini AI
- **python-dotenv**: Gerenciamento de variáveis de ambiente

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

## 🛠️ Personalização

Você pode personalizar os prompts da IA editando as funções no arquivo `app.py`:

- `get_email_improvement_prompt()`: Modifica as instruções para a IA
- `tone_instructions`: Ajusta as definições de cada tom

## 🔒 Segurança

- Sua chave da API é mantida apenas na sessão local
- Nenhuma informação é armazenada permanentemente
- Os dados são processados diretamente pela API do Google

## 🐛 Solução de problemas

### Erro de API Key
- Verifique se a chave está correta
- Confirme se a API Gemini está habilitada em sua conta Google

### Erro de conexão
- Verifique sua conexão com a internet
- Tente reiniciar a aplicação

### Aplicação não carrega
- Confirme se todas as dependências foram instaladas
- Verifique se a porta 8501 está disponível

## 📞 Suporte

Para problemas ou sugestões:
1. Verifique se seguiu todos os passos de instalação
2. Confirme se sua chave da API está funcionando
3. Reinicie a aplicação se necessário

## 🎯 Desenvolvido com

- **Python 3.11**
- **Streamlit 1.28.1**
- **Google Gemini AI**
- **Amor e dedicação** ❤️

---

**Nota**: Esta ferramenta requer uma chave da API do Google Gemini AI para funcionar. A API pode ter custos associados dependendo do uso.

