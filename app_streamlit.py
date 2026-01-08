"""
Interface Streamlit para o Sistema de Recomendação de Cursos
Interface web interativa para demonstração do sistema.
"""

import streamlit as st
import pandas as pd
from sistema_recomendacao import SistemaRecomendacaoCursos
from dotenv import load_dotenv
import os
import time

# Configuração da página
st.set_page_config(
    page_title="Sistema de Recomendação de Cursos",
    page_icon="🎓",
    layout="wide"
)

# Título e descrição
st.title("🎓 Sistema de Recomendação de Cursos")
st.markdown("""
Este sistema demonstra múltiplas estratégias de recomendação para matching entre 
interesses de alunos e ofertas de cursos disponíveis.
""")

# Verificação das variáveis de ambiente
load_dotenv()

@st.cache_resource
def carregar_sistema():
    """Carrega o sistema de recomendação (cacheado para performance)"""
    st.info("⏳ Carregando sistema de recomendação...")
    
    # Caminhos das bases (em produção, seriam variáveis de ambiente)
    OFERTAS_PATH = os.getenv('OFERTAS_PATH', 'data/exemplos/ofertas_exemplo.csv')
    INTERESSES_PATH = os.getenv('INTERESSES_PATH', 'data/exemplos/interesses_exemplo.parquet')
    ESTRUTURA_PATH = os.getenv('ESTRUTURA_PATH', 'data/exemplos/estrutura_exemplo.xlsx')
    
    try:
        sistema = SistemaRecomendacaoCursos(
            path_interesses=INTERESSES_PATH,
            path_ofertas=OFERTAS_PATH,
            path_estrutura=ESTRUTURA_PATH
        )
        st.success("✅ Sistema carregado com sucesso!")
        return sistema
    except Exception as e:
        st.error(f"❌ Erro ao carregar sistema: {str(e)}")
        return None

# Carrega o sistema
sistema = carregar_sistema()

if sistema is None:
    st.stop()

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Informações")
    st.markdown("""
    **Estratégias de Recomendação:**
    1. **Match Completo**: Curso + Unidade + Horários
    2. **Outras Unidades**: Mesmo curso em locais diferentes
    3. **Trilha Profissional**: Cursos da mesma área
    4. **Similaridade**: Cursos com títulos semelhantes
    5. **Modalidade EAD**: Cursos a distância
    """)
    
    # Estatísticas rápidas
    st.subheader("📊 Estatísticas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cursos", len(sistema.df_cursos))
        st.metric("Interesses", len(sistema.df_interesses))
    with col2:
        st.metric("Ofertas", len(sistema.df_ofertas))
        st.metric("Unidades", len(sistema.df_unidades))

# Seção principal
st.header("🔍 Buscar Recomendações")

# Lista de interesses disponíveis
st.subheader("Interesses Disponíveis")
interesses_sample = sistema.listar_interesses_disponiveis()

if not interesses_sample.empty:
    # Seleção de interesse
    selecionado = st.selectbox(
        "Selecione um interesse para ver recomendações:",
        options=interesses_sample['COD_INTERESSE'].tolist(),
        format_func=lambda x: f"{x} - {interesses_sample[interesses_sample['COD_INTERESSE']==x]['TITULO_INTERESSE'].iloc[0]}"
    )
    
    if selecionado:
        # Botão para gerar recomendações
        if st.button("🎯 Gerar Recomendações", type="primary"):
            with st.spinner("Gerando recomendações..."):
                inicio = time.time()
                recomendacoes = sistema.gerar_recomendacoes(selecionado)
                tempo = time.time() - inicio
                
                if recomendacoes is not None and not recomendacoes.empty:
                    st.success(f"✅ {len(recomendacoes)} recomendações geradas em {tempo:.2f}s")
                    
                    # Mostra estatísticas
                    st.subheader("📈 Distribuição das Recomendações")
                    dist_tipo = recomendacoes['TIPO_INDICACAO'].value_counts()
                    st.bar_chart(dist_tipo)
                    
                    # Tabela detalhada
                    st.subheader("📋 Recomendações Detalhadas")
                    
                    # Formatação das colunas
                    cols_display = [
                        'TIPO_INDICACAO', 'NIVEL_MATCH',
                        'TITULO_OFERTA', 'AREA_OFERTA', 'MODALIDADE_OFERTA',
                        'NOME_UNIDADE', 'DATA_INICIO'
                    ]
                    
                    if 'DISTANCIA_KM' in recomendacoes.columns:
                        cols_display.append('DISTANCIA_KM')
                    
                    if 'SCORE_SIMILARIDADE' in recomendacoes.columns:
                        cols_display.append('SCORE_SIMILARIDADE')
                    
                    st.dataframe(
                        recomendacoes[cols_display],
                        use_container_width=True,
                        column_config={
                            "DISTANCIA_KM": st.column_config.NumberColumn(
                                "Distância (km)",
                                format="%.1f km"
                            ),
                            "SCORE_SIMILARIDADE": st.column_config.NumberColumn(
                                "Similaridade",
                                format="%.3f"
                            ),
                            "DATA_INICIO": st.column_config.DateColumn(
                                "Data Início",
                                format="DD/MM/YYYY"
                            )
                        }
                    )
                    
                    # Cards por tipo de recomendação
                    st.subheader("🃏 Visualização por Card")
                    
                    tipos = recomendacoes['TIPO_INDICACAO'].unique()
                    for tipo in tipos:
                        st.markdown(f"### {tipo}")
                        ofertas_tipo = recomendacoes[recomendacoes['TIPO_INDICACAO'] == tipo]
                        
                        # Mostra 3 cards por linha
                        col_count = 3
                        cols = st.columns(col_count)
                        
                        for idx, (_, oferta) in enumerate(ofertas_tipo.iterrows()):
                            with cols[idx % col_count]:
                                with st.container():
                                    st.markdown(f"""
                                    <div style='
                                        border: 1px solid #ddd;
                                        border-radius: 10px;
                                        padding: 15px;
                                        margin: 10px 0;
                                        background-color: #f9f9f9;
                                    '>
                                    <h4 style='margin-top: 0;'>{oferta['TITULO_OFERTA'][:30]}...</h4>
                                    <p><strong>Unidade:</strong> {oferta.get('NOME_UNIDADE', 'N/A')}</p>
                                    <p><strong>Modalidade:</strong> {oferta['MODALIDADE_OFERTA']}</p>
                                    <p><strong>Área:</strong> {oferta['AREA_OFERTA']}</p>
                                    """, unsafe_allow_html=True)
                                    
                                    if 'DISTANCIA_KM' in oferta and oferta['DISTANCIA_KM'] > 0:
                                        st.markdown(f"<p><strong>Distância:</strong> {oferta['DISTANCIA_KM']:.1f} km</p>", 
                                                   unsafe_allow_html=True)
                                    
                                    if 'SCORE_SIMILARIDADE' in oferta and pd.notna(oferta['SCORE_SIMILARIDADE']):
                                        st.markdown(f"<p><strong>Similaridade:</strong> {oferta['SCORE_SIMILARIDADE']:.3f}</p>", 
                                                   unsafe_allow_html=True)
                                    
                                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Nenhuma recomendação encontrada para este interesse.")
else:
    st.warning("⚠️ Nenhum interesse disponível para demonstração.")

# Seção de explicação
with st.expander("📚 Como funciona o sistema?"):
    st.markdown("""
    ### Estratégias de Recomendação
    
    1. **Match Completo na Mesma Unidade**
       - Busca exatamente o curso desejado
       - Na mesma unidade preferida
       - Nos mesmos dias e turnos
       - Criado após o interesse
    
    2. **Mesmo Curso em Outras Unidades**
       - Curso exato em unidades diferentes
       - Considera preferências de dias/turnos
       - Calcula distância da unidade original
       - Ordena por proximidade geográfica
    
    3. **Trilha Profissional**
       - Identifica a área profissional do curso
       - Busca outros cursos da mesma trilha
       - Mantém mesma unidade preferencial
       - Baseado em mapeamento curricular
    
    4. **Similaridade Semântica**
       - Usa embeddings de títulos de cursos
       - Modelo multilingual (SentenceTransformer)
       - Cosine similarity > 0.7
       - Mantém mesma unidade
    
    5. **Modalidade EAD**
       - Cursos a distância similares
       - Similaridade semântica apenas em EAD
       - Flexibilidade geográfica total
    
    ### Tecnologias Utilizadas
    - **Embeddings**: paraphrase-multilingual-mpnet-base-v2
    - **Similaridade**: Cosine similarity
    - **Geolocalização**: Fórmula de Haversine
    - **Interface**: Streamlit
    - **Processamento**: Pandas + NumPy
    """)

# Rodapé
st.markdown("---")
st.markdown(
    "*Sistema de Recomendação Híbrido - Projeto de Exemplo para Portfólio* "
)