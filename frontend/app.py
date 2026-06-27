import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Configuração da Página
st.set_page_config(page_title="Vagas de Física", layout="wide")

# 2. Conexão com o Banco de Dados
load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- FUNÇÕES DE BANCO DE DADOS ---
def buscar_catalogo_vagas():
    resposta = supabase.table("concursos_fisica").select("*").order("data_descoberta", desc=True).execute()
    return resposta.data

def buscar_meus_concursos():
    if not st.session_state.usuario:
        return []
    resposta = supabase.table("acompanhamento_candidato") \
        .select("id, fase_atual, anotacoes, prazo, concurso_id, concursos_fisica(titulo, orgao, salario, link_edital)") \
        .eq("user_id", st.session_state.usuario.user.id) \
        .execute()
    return resposta.data

def salvar_concurso(id_concurso):
    busca_duplicata = supabase.table("acompanhamento_candidato") \
        .select("id").eq("user_id", st.session_state.usuario.user.id).eq("concurso_id", id_concurso).execute()
    
    if len(busca_duplicata.data) > 0:
        st.toast("⚠️ Vaga já salva!", icon="⚠️")
        return

    novo = {
        "user_id": st.session_state.usuario.user.id,
        "concurso_id": id_concurso,
        "fase_atual": "Fase 1: Inscrição"
    }
    supabase.table("acompanhamento_candidato").insert(novo).execute()
    st.toast("✅ Vaga salva!", icon="✅")
    st.rerun()

def atualizar_detalhes(id_acompanhamento, nova_fase, novo_prazo, novas_anotacoes):
    dados = {
        "fase_atual": nova_fase,
        "anotacoes": novas_anotacoes,
        "prazo": str(novo_prazo) if novo_prazo else None
    }
    supabase.table("acompanhamento_candidato").update(dados).eq("id", id_acompanhamento).execute()
    st.rerun()

def excluir_concurso(id_acompanhamento):
    supabase.table("acompanhamento_candidato").delete().eq("id", id_acompanhamento).execute()
    st.rerun()

# --- TELAS ---
def tela_autenticacao():
    st.title("🎯 VAGAS DE FÍSICA")
    aba1, aba2 = st.tabs(["Login", "Criar Conta"])
    with aba1:
        email = st.text_input("E-mail", key="l_email")
        senha = st.text_input("Senha", type="password", key="l_senha")
        if st.button("Entrar"):
            try:
                st.session_state.usuario = supabase.auth.sign_in_with_password({"email": email, "password": senha})
                st.rerun()
            except:
                st.error("Erro no login.")
    with aba2:
        email = st.text_input("E-mail", key="c_email")
        senha = st.text_input("Senha", type="password", key="c_senha")
        if st.button("Cadastrar"):
            try:
                supabase.auth.sign_up({"email": email, "password": senha})
                st.success("Conta criada!")
            except Exception as e:
                st.error(str(e))

def tela_principal():
    st.title(f"Bem-vinda, {st.session_state.usuario.user.email.split('@')[0]}!")
    if st.button("Sair"):
        supabase.auth.sign_out()
        st.session_state.usuario = None
        st.rerun()
            
    aba1, aba2 = st.tabs(["📋 Minhas Vagas", "🔍 Explorar"])
    
    with aba2:
        for vaga in buscar_catalogo_vagas():
            with st.expander(f"🏛️ {vaga['orgao']} - {vaga['titulo']}"):
                st.write(f"**Salário:** {vaga['salario']}")
                if st.button("Acompanhar", key=f"add_{vaga['id']}"):
                    salvar_concurso(vaga['id'])

    with aba1:
        meus = buscar_meus_concursos()
        if not meus:
            st.info("Nenhuma vaga salva.")
        else:
            fases_padrao = ["Fase 1: Inscrição", "Fase 2: Entrega de Documentos", "Fase 3: Prova Objetiva", "Fase 4: Prova Prática", "Fase 5: Retorno da Banca"]
            colunas = st.columns(len(fases_padrao))
            
            for i, fase in enumerate(fases_padrao):
                with colunas[i]:
                    st.markdown(f"### {fase}")
                    for c in [x for x in meus if x['fase_atual'] == fase]:
                        with st.container(border=True):
                            st.write(f"**{c['concursos_fisica']['orgao']}**")
                            with st.expander("Editar"):
                                nova_fase = st.selectbox("Fase", fases_padrao, index=i, key=f"f_{c['id']}")
                                data_val = datetime.strptime(c['prazo'], "%Y-%m-%d") if c.get('prazo') else None
                                prazo = st.date_input("Prazo", value=data_val, key=f"p_{c['id']}")
                                nota = st.text_area("Anotações", value=c.get('anotacoes') or "", key=f"n_{c['id']}")
                                if st.button("💾 Salvar", key=f"s_{c['id']}"):
                                    atualizar_detalhes(c['id'], nova_fase, prazo, nota)
                                st.divider()
                                if st.button("🗑️ Remover", key=f"d_{c['id']}", type="primary"):
                                    excluir_concurso(c['id'])

if st.session_state.usuario is None:
    tela_autenticacao()
else:
    tela_principal()