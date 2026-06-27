# IA Scout: Área de **Física**

Plataforma SaaS automatizada para monitorização de concursos públicos na área de **Física**. O sistema utiliza Inteligência Artificial para realizar o *scraping* profundo de editais, filtrar vagas específicas e gerir o acompanhamento do candidato através de um quadro Kanban dinâmico.

##  Arquitetura do Sistema

O projeto foi desenhado seguindo as melhores práticas de Engenharia de Dados:

* **Backend:** Scripts Python com *web scraping* profundo (BeautifulSoup).
* **Inteligência Artificial:** Google Gemini (modelo 2.5 Flash) para análise semântica e estruturação de dados em JSON.
* **Database & Auth:** Supabase (PostgreSQL) com RLS (Row Level Security).
* **Frontend:** Streamlit para uma interface de gestão interativa e intuitiva.
* **Automação:** GitHub Actions (CI/CD) para orquestração diária do robô de busca.
* **Deploy:** Streamlit Community Cloud.

## Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework Web:** Streamlit
- **Banco de Dados:** Supabase (PostgreSQL)
- **IA/LLM:** Google Gemini API
- **Infraestrutura:** GitHub Actions & Streamlit Cloud

## Funcionalidades

- **Monitorização Automática:** O robô varre o PCI Concursos diariamente.
- **Filtragem Inteligente:** A IA descarta vagas irrelevantes e valida requisitos de Física.
- **Segurança:** Gestão de utilizadores com autenticação integrada.
-  **Kanban Dinâmico:** Quadro de acompanhamento com fases personalizáveis e blocos de notas.
-  **Gestão de Prazos:** Controlo de datas críticas para cada etapa do concurso.

## ⚙️ Como Funciona o Fluxo de Dados

1. **Rastreio:** O script `motor_ia_scout.py` entra nos editais encontrados na página inicial.
2. **Análise:** O Gemini extrai o órgão, salário e confirma a área de Física.
3. **Persistência:** O Supabase armazena os dados validados.
4. **Interface:** A usuária acede à plataforma via Streamlit e gere o seu pipeline de estudos/provas.





---

Quer que eu o ajude a escrever o "texto de motivação" para colocar no topo, ou prefere adicionar mais alguma secção técnica ao seu README?
