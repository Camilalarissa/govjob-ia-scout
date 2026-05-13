import streamlit as st
import sqlite3
import pandas as pd
import os

# Configuração da página 
st.set_page_config(page_title="Monitor de Concursos IA", page_icon="📚", layout="wide")

# Estilo Minimalista 
st.markdown("""
    <style>
    /* Estilo do Card */
    .stCard { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #e6e0d4;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    /* Forçar cor do texto para legibilidade */
    .stCard h3 { color: #2c3e50 !important; margin-bottom: 5px; }
    .stCard p { color: #555555 !important; }
    .stCard div { color: #333333 !important; line-height: 1.6; }
    
    /* Links */
    .stCard a { color: #d4a373 !important; font-weight: bold; text-decoration: none; }
    .stCard a:hover { text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

def carregar_dados():
    # 1.  caminho de onde o app.py 
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(diretorio_atual, "..", "backend", "database", "concursos.db")
    
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT titulo, link, resumo_ia, data_coleta FROM editais WHERE lido = 1 ORDER BY data_coleta DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except sqlite3.OperationalError:
        # Retorna um DataFrame vazio se o banco não for encontrado para não quebrar a tela
        return pd.DataFrame()
      
    # Trazemos apenas os que já foram processados pela IA
    query = "SELECT titulo, link, resumo_ia, data_coleta FROM editais WHERE lido = 1 ORDER BY data_coleta DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("📚 Monitor Inteligente de Concursos")
st.subheader("Vagas filtradas para Física e Nível Médio com resumo da IA")

dados = carregar_dados()

if dados.empty:
    st.info("Ainda não há resumos processados. Rode o `summarizer.py` primeiro!")
else:
    # Barra lateral para filtros rápidos
    busca = st.sidebar.text_input("Filtrar por palavra-chave:")
    if busca:
        dados = dados[dados['titulo'].str.contains(busca, case=False)]

    # Exibição das Vagas em "Cards"
    for index, row in dados.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="stCard">
                <h3>{row['titulo']}</h3>
                <p style="color: #666; font-size: 0.9em;">Coletado em: {row['data_coleta']}</p>
                <div style="background-color: #f9f9f9; padding: 10px; border-left: 5px solid #d4a373;">
                    {row['resumo_ia'].replace('\n', '<br>')}
                </div>
                <br>
                <a href="{row['link']}" target="_blank">🔗 Ver edital completo no PCI</a>
            </div>
            """, unsafe_allow_html=True)