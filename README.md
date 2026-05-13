# GovJob IA Scout

**Monitor Inteligente de Concursos Públicos com IA Generativa**

Este projeto foi desenvolvido para otimizar a busca por oportunidades no setor público, focando em **vagas de Física e Nível Médio**. Ele utiliza Web Scraping para coleta e o **Gemini 2.5 Flash** para análise e resumo automático de editais.

## Tecnologias Utilizadas

- **Python 3.12**: Linguagem base.
- **Google Gemini 2.5 Flash API**: Resumo inteligente de editais via LLM.
- **Streamlit**: Dashboard interativo e minimalista.
- **SQLite**: Persistência de dados local.
- **BeautifulSoup4**: Web Scraping para coleta de dados.

## Arquitetura do Sistema

O projeto segue uma arquitetura modular focada em escalabilidade:

1. **Scrapers**: Varredura automatizada em portais de concursos.
2. **Database Handler**: Persistência robusta com validação de duplicatas.
3. **AI Engine**: Integração com a nova biblioteca `google-genai` para processamento de linguagem natural.
4. **Frontend**: Interface de usuário minimalista e funcional.

## Como Executar

1. Instale as dependências: `pip install -r requirements.txt`
2. Configure sua chave no `.env`: `GEMINI_API_KEY=sua_chave_aqui`
3. Execute o coletor: `python backend/scrapers/pci_scraper.py`
4. Gere os resumos: `python backend/engine/summarizer.py`
5. Inicie o dashboard: `streamlit run frontend/app.py`

## Desenvolvido por

**Camila Larissa Gonçalves**  
Analista de Sistemas | Pós-graduanda em IA e Ciência de Dados
