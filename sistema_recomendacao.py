"""
Sistema de Recomendação de Cursos - Classe Principal
Sistema híbrido que combina múltiplas estratégias de matching
"""

import numpy as np
import pandas as pd
from datetime import datetime
import math
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import time

load_dotenv()

class SistemaRecomendacaoCursos:
    """
    Sistema principal de recomendação que implementa múltiplas estratégias
    de matching entre interesses de alunos e ofertas de cursos.
    """
    
    def __init__(self, path_interesses, path_ofertas, path_estrutura):
        """
        Inicializa o sistema carregando todas as bases de dados necessárias.
        
        Args:
            path_interesses: Caminho para base de interesses
            path_ofertas: Caminho para base de ofertas
            path_estrutura: Caminho para estrutura de dados (cursos, unidades)
        """
        
        t1 = time.time()
        
        # Carregamento das bases
        self.df_unidades, self.unidade_coord_dict = self._carregar_unidades(path_estrutura)
        print(f'⌛ Unidades carregadas')
        
        self.df_cursos = self._carregar_cursos(path_estrutura)
        print(f'⌛ Cursos carregados')
        
        self.df_interesses = self._carregar_interesses(path_interesses)
        print(f'⌛ Interesses carregados')
        
        self.df_ofertas = self._carregar_ofertas(path_ofertas)
        print(f'⌛ Ofertas carregadas')
        
        self.df_trilhas = self._carregar_trilhas_profissionais(path_estrutura)
        print(f'⌛ Trilhas profissionais carregadas')
        
        # Modelo de embeddings
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        print(f'⌛ Modelo de embeddings carregado')
        
        # Pré-cálculo de embeddings
        self._calcular_embeddings()
        print(f'⌛ Embeddings calculados')
        
        t_total = time.time() - t1
        print(f'✅ Sistema inicializado em {t_total:.2f} segundos\n')
    
    def _carregar_cursos(self, path_estrutura):
        """Carrega o catálogo de cursos"""
        df_cursos = pd.read_excel(path_estrutura, sheet_name='CATALOGO_CURSOS')
        return df_cursos
    
    def _carregar_unidades(self, path_estrutura):
        """Carrega informações das unidades/campi"""
        df_unidades = pd.read_excel(path_estrutura, sheet_name='UNIDADES')
        df_unidades = df_unidades[[
            'COD_UNIDADE',
            'NOME_UNIDADE',
            'LATITUDE',
            'LONGITUDE'
        ]]
        
        # Dicionário de coordenadas para cálculo de distância
        unidades_list = df_unidades.to_dict('records')
        unidade_coord_dict = {
            x['COD_UNIDADE']: [x['LATITUDE'], x['LONGITUDE']] 
            for x in unidades_list
        }
        
        return df_unidades, unidade_coord_dict
    
    def _carregar_trilhas_profissionais(self, path_estrutura):
        """Carrega mapeamento de cursos por trilha profissional"""
        df_trilhas_full = pd.read_excel(path_estrutura, sheet_name='TRILHAS')
        
        # Processamento das trilhas
        colunas_cursos = [col for col in df_trilhas_full.columns if 'CURSO' in col]
        df_trilhas = df_trilhas_full[['AREA_PROFISSIONAL'] + colunas_cursos]
        
        # Transforma colunas em lista
        df_trilhas['LISTA_CURSOS'] = df_trilhas[colunas_cursos].to_numpy().tolist()
        df_trilhas = df_trilhas.explode(column='LISTA_CURSOS')[['AREA_PROFISSIONAL', 'LISTA_CURSOS']]
        df_trilhas = df_trilhas.rename(columns={'LISTA_CURSOS': 'COD_CURSO'})
        
        # Remove valores nulos
        df_trilhas = df_trilhas.replace('-', np.nan).dropna()
        df_trilhas['COD_CURSO'] = df_trilhas['COD_CURSO'].astype(int)
        
        # Filtra cursos ativos
        df_trilhas = df_trilhas.merge(
            self.df_cursos[['COD_CURSO', 'TITULO', 'AREA_CONHECIMENTO', 'MODALIDADE', 'STATUS']],
            left_on='COD_CURSO',
            right_on='COD_CURSO',
            how='left'
        )
        
        # Remove cursos inativos
        df_trilhas = df_trilhas[
            ~df_trilhas['STATUS'].isin(['DESCONTINUADO', 'EM_REFORMULACAO'])
        ]
        
        return df_trilhas
    
    def _carregar_interesses(self, path_interesses):
        """Carrega base de interesses dos alunos"""
        try:
            df_interesses = pd.read_parquet(path_interesses)
        except:
            df_interesses = pd.read_csv(path_interesses, sep=';', encoding='latin1')
        
        # Seleção e renomeação de colunas
        df_interesses = df_interesses[[
            'COD_INTERESSE',
            'COD_ALUNO',
            'COD_CURSO',
            'COD_UNIDADE',
            'DATA_INTERESSE',
            'TURNO_MANHA',
            'TURNO_TARDE',
            'TURNO_NOITE',
            'DIA_SEG',
            'DIA_TER',
            'DIA_QUA',
            'DIA_QUI',
            'DIA_SEX',
            'DIA_SAB'
        ]]
        
        # Normalização de valores
        df_interesses = df_interesses.replace({'S': True, 'N': False, 's': True, 'n': False})
        
        # Adiciona informações dos cursos
        df_interesses = df_interesses.merge(
            self.df_cursos[['COD_CURSO', 'TITULO', 'MODALIDADE', 'AREA_CONHECIMENTO']],
            left_on='COD_CURSO',
            right_on='COD_CURSO',
            how='left'
        )
        
        # Adiciona informações da unidade
        df_interesses = df_interesses.merge(
            self.df_unidades[['COD_UNIDADE', 'NOME_UNIDADE']],
            left_on='COD_UNIDADE',
            right_on='COD_UNIDADE',
            how='left'
        )
        
        # Renomeação final
        df_interesses = df_interesses.rename(columns={
            'TITULO': 'TITULO_INTERESSE',
            'MODALIDADE': 'MODALIDADE_INTERESSE',
            'AREA_CONHECIMENTO': 'AREA_INTERESSE',
            'NOME_UNIDADE': 'UNIDADE_INTERESSE',
            'TURNO_MANHA': 'TURNO_MANHA',
            'TURNO_TARDE': 'TURNO_TARDE',
            'TURNO_NOITE': 'TURNO_NOITE',
            'DIA_SEG': 'DIA_SEG',
            'DIA_TER': 'DIA_TER',
            'DIA_QUA': 'DIA_QUA',
            'DIA_QUI': 'DIA_QUI',
            'DIA_SEX': 'DIA_SEX',
            'DIA_SAB': 'DIA_SAB'
        })
        
        return df_interesses
    
    def _carregar_ofertas(self, path_ofertas):
        """Carrega base de ofertas de cursos"""
        df_ofertas = pd.read_csv(path_ofertas, encoding='latin1', sep=";")
               
        # Conversão de datas
        for col in ['DATA_CRIACAO', 'DATA_INICIO']:
            try:
                df_ofertas[col] = pd.to_datetime(df_ofertas[col], format='%d/%m/%Y')
            except:
                df_ofertas[col] = pd.to_datetime(df_ofertas[col], format='%Y-%m-%d')
        
        # Filtro por ano
        df_ofertas = df_ofertas[df_ofertas['DATA_CRIACAO'].dt.year == 2025]
        
        # Processamento de dias da semana
        df_ofertas['DIAS_SEMANA'] = df_ofertas['DIAS_SEMANA'].str.replace(' ', '').str.split('-')
        
        dias_map = {
            'SEG': 'DIA_SEG',
            'TER': 'DIA_TER', 
            'QUA': 'DIA_QUA',
            'QUI': 'DIA_QUI',
            'SEX': 'DIA_SEX',
            'SAB': 'DIA_SAB'
        }
        
        for sigla, coluna in dias_map.items():
            df_ofertas[coluna] = df_ofertas['DIAS_SEMANA'].apply(lambda x: sigla in x if isinstance(x, list) else False)
        
        # Processamento de turnos
        df_ofertas['TURNO_MANHA'] = df_ofertas['TURNO'].str.contains('DIURNO|INTEGRAL')
        df_ofertas['TURNO_TARDE'] = df_ofertas['TURNO'].str.contains('VESPERTINO|INTEGRAL')
        df_ofertas['TURNO_NOITE'] = df_ofertas['TURNO'].str.contains('NOTURNO|INTEGRAL')
        
        # Seleção final de colunas
        df_ofertas = df_ofertas[[
            'COD_OFERTA',
            'COD_CURSO',
            'COD_UNIDADE',
            'DATA_CRIACAO',
            'DATA_INICIO',
            'DIA_SEG', 'DIA_TER', 'DIA_QUA', 'DIA_QUI', 'DIA_SEX', 'DIA_SAB',
            'TURNO_MANHA', 'TURNO_TARDE', 'TURNO_NOITE'
        ]]
        
        # Adiciona informações do curso
        df_ofertas = df_ofertas.merge(
            self.df_cursos[['COD_CURSO', 'TITULO', 'AREA_CONHECIMENTO', 'MODALIDADE']],
            left_on='COD_CURSO',
            right_on='COD_CURSO'
        )
        
        df_ofertas = df_ofertas.rename(columns={
            'TITULO': 'TITULO_OFERTA',
            'MODALIDADE': 'MODALIDADE_OFERTA',
            'AREA_CONHECIMENTO': 'AREA_OFERTA'
        })
        
        df_ofertas['AREA_TITULO'] = df_ofertas['AREA_OFERTA'] + ' - ' + df_ofertas['TITULO_OFERTA']
        
        return df_ofertas
    
    def _calcular_embeddings(self):
        """Calcula embeddings para todos os cursos ativos"""
        # Filtra cursos ativos
        df_cursos_emb = self.df_cursos.copy()
        df_cursos_emb = df_cursos_emb[
            ~df_cursos_emb['STATUS'].isin(['DESCONTINUADO', 'EM_REFORMULACAO', 'INDISPONIVEL'])
        ]
        
        # Cria coluna combinada para embedding
        df_cursos_emb['AREA_TITULO'] = df_cursos_emb['AREA_CONHECIMENTO'] + " - " + df_cursos_emb['TITULO']
        
        # Separa cursos EAD
        df_cursos_ead = df_cursos_emb[df_cursos_emb['MODALIDADE'].str.contains('EAD', na=False)]
        ead_index = df_cursos_ead.index.to_numpy()
        
        self.df_cursos_emb = df_cursos_emb.copy()
        self.lista_area_titulos = self.df_cursos_emb['AREA_TITULO'].tolist()
        
        # Calcula embeddings
        self.embeddings = self.model.encode(self.lista_area_titulos)
        
        # Salva embeddings para cursos EAD separadamente
        self.lista_area_titulos_ead = np.array(self.lista_area_titulos)[ead_index].tolist()
        self.embeddings_ead = self.embeddings[ead_index]
    
    def _calcular_distancia(self, lat1, lon1, lat2, lon2, raio_terra=6371):
        """Calcula distância entre duas coordenadas usando fórmula de Haversine"""
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat / 2) ** 2) + \
            (math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(dlon / 2) ** 2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia_km = raio_terra * c
        
        return distancia_km
    
    def _buscar_cursos_similares(self, cod_curso, top_n=3, apenas_ead=False):
        """Busca cursos similares usando embeddings"""
        curso_info = self.df_cursos[self.df_cursos['COD_CURSO'] == cod_curso]
        
        if curso_info.empty:
            return [], {}
        
        titulo_curso = curso_info['TITULO'].iloc[0]
        area_curso = curso_info['AREA_CONHECIMENTO'].iloc[0]
        area_titulo = area_curso + ' - ' + titulo_curso
        
        # Calcula embedding do curso alvo
        embedding_alvo = self.model.encode([area_titulo])
        
        # Escolhe base de embeddings
        if apenas_ead:
            embeddings_base = self.embeddings_ead
            lista_base = self.lista_area_titulos_ead
        else:
            embeddings_base = self.embeddings
            lista_base = self.lista_area_titulos
        
        # Calcula similaridade
        similaridades = cosine_similarity(embedding_alvo, embeddings_base)
        indices_similares = np.argsort(similaridades[0])[::-1]
        
        # Pega os top_n (excluindo o próprio curso)
        nomes_similares = np.array(lista_base)[indices_similares[1:top_n+1]].tolist()
        scores_similares = similaridades[0][indices_similares[1:top_n+1]].tolist()
        
        # Mapeia para códigos de curso
        similares_dict = {}
        for nome, score in zip(nomes_similares, scores_similares):
            curso_match = self.df_cursos_emb[self.df_cursos_emb['AREA_TITULO'] == nome]
            if not curso_match.empty:
                cod = curso_match['COD_CURSO'].iloc[0]
                similares_dict[cod] = score
        
        return list(similares_dict.keys()), similares_dict
    
    def _match_unidade_mesma(self, indice_interesse):
        """Match 1: Mesmo curso na mesma unidade"""
        dados_interesse = self.df_interesses.iloc[indice_interesse]
        
        # Filtros básicos
        mask_curso = self.df_ofertas['COD_CURSO'] == dados_interesse['COD_CURSO']
        mask_unidade = self.df_ofertas['COD_UNIDADE'] == dados_interesse['COD_UNIDADE']
        mask_data = self.df_ofertas['DATA_CRIACAO'] >= pd.to_datetime(dados_interesse['DATA_INTERESSE'])
        
        # Match completo (curso + unidade + dias + turnos)
        mask_dias = (
            (self.df_ofertas['DIA_SEG'] == dados_interesse['DIA_SEG']) |
            (self.df_ofertas['DIA_TER'] == dados_interesse['DIA_TER']) |
            (self.df_ofertas['DIA_QUA'] == dados_interesse['DIA_QUA']) |
            (self.df_ofertas['DIA_QUI'] == dados_interesse['DIA_QUI']) |
            (self.df_ofertas['DIA_SEX'] == dados_interesse['DIA_SEX']) |
            (self.df_ofertas['DIA_SAB'] == dados_interesse['DIA_SAB'])
        )
        
        mask_turnos = (
            (self.df_ofertas['TURNO_MANHA'] == dados_interesse['TURNO_MANHA']) |
            (self.df_ofertas['TURNO_TARDE'] == dados_interesse['TURNO_TARDE']) |
            (self.df_ofertas['TURNO_NOITE'] == dados_interesse['TURNO_NOITE'])
        )
        
        # Resultados hierárquicos
        resultados = []
        
        # Nível 1: Match completo
        match_completo = self.df_ofertas[mask_curso & mask_unidade & mask_dias & mask_turnos & mask_data].copy()
        if not match_completo.empty:
            match_completo['TIPO_INDICACAO'] = '1.MATCH_COMPLETO'
            match_completo['NIVEL_MATCH'] = 'CURSO+UNIDADE+DIAS+TURNOS'
            resultados.append(match_completo)
        
        # Nível 2: Sem turnos
        match_sem_turno = self.df_ofertas[mask_curso & mask_unidade & mask_dias & mask_data].copy()
        match_sem_turno = match_sem_turno[~match_sem_turno['COD_OFERTA'].isin(match_completo['COD_OFERTA'])]
        if not match_sem_turno.empty:
            match_sem_turno['TIPO_INDICACAO'] = '1.MATCH_COMPLETO'
            match_sem_turno['NIVEL_MATCH'] = 'CURSO+UNIDADE+DIAS'
            resultados.append(match_sem_turno)
        
        # Nível 3: Apenas curso + unidade
        match_basico = self.df_ofertas[mask_curso & mask_unidade & mask_data].copy()
        ofertas_ja_incluidas = match_completo['COD_OFERTA'].tolist() + match_sem_turno['COD_OFERTA'].tolist()
        match_basico = match_basico[~match_basico['COD_OFERTA'].isin(ofertas_ja_incluidas)]
        if not match_basico.empty:
            match_basico['TIPO_INDICACAO'] = '1.MATCH_COMPLETO'
            match_basico['NIVEL_MATCH'] = 'CURSO+UNIDADE'
            resultados.append(match_basico)
        
        return pd.concat(resultados) if resultados else pd.DataFrame()
    
    def _match_unidade_outra(self, indice_interesse):
        """Match 2: Mesmo curso em outras unidades"""
        dados_interesse = self.df_interesses.iloc[indice_interesse]
        
        # Coordenadas da unidade de interesse
        cod_unidade_interesse = dados_interesse['COD_UNIDADE']
        lat_lon = self.unidade_coord_dict.get(cod_unidade_interesse, [None, None])
        
        if None in lat_lon:
            return pd.DataFrame()
        
        lat_interesse, lon_interesse = lat_lon
        
        # Filtros
        mask_curso = self.df_ofertas['COD_CURSO'] == dados_interesse['COD_CURSO']
        mask_unidade = self.df_ofertas['COD_UNIDADE'] != cod_unidade_interesse
        mask_data = self.df_ofertas['DATA_CRIACAO'] >= pd.to_datetime(dados_interesse['DATA_INTERESSE'])
        
        # Match hierárquico
        resultados = []
        
        # Com dias e turnos
        mask_dias = (
            (self.df_ofertas['DIA_SEG'] == dados_interesse['DIA_SEG']) |
            (self.df_ofertas['DIA_TER'] == dados_interesse['DIA_TER']) |
            (self.df_ofertas['DIA_QUA'] == dados_interesse['DIA_QUA']) |
            (self.df_ofertas['DIA_QUI'] == dados_interesse['DIA_QUI']) |
            (self.df_ofertas['DIA_SEX'] == dados_interesse['DIA_SEX']) |
            (self.df_ofertas['DIA_SAB'] == dados_interesse['DIA_SAB'])
        )
        
        mask_turnos = (
            (self.df_ofertas['TURNO_MANHA'] == dados_interesse['TURNO_MANHA']) |
            (self.df_ofertas['TURNO_TARDE'] == dados_interesse['TURNO_TARDE']) |
            (self.df_ofertas['TURNO_NOITE'] == dados_interesse['TURNO_NOITE'])
        )
        
        # Nível 1: Com dias e turnos
        match_completo = self.df_ofertas[mask_curso & mask_unidade & mask_dias & mask_turnos & mask_data].copy()
        if not match_completo.empty:
            match_completo['TIPO_INDICACAO'] = '2.OUTRA_UNIDADE'
            match_completo['NIVEL_MATCH'] = 'CURSO+DIAS+TURNOS'
            resultados.append(match_completo)
        
        # Nível 2: Apenas dias
        match_dias = self.df_ofertas[mask_curso & mask_unidade & mask_dias & mask_data].copy()
        match_dias = match_dias[~match_dias['COD_OFERTA'].isin(match_completo['COD_OFERTA'])]
        if not match_dias.empty:
            match_dias['TIPO_INDICACAO'] = '2.OUTRA_UNIDADE'
            match_dias['NIVEL_MATCH'] = 'CURSO+DIAS'
            resultados.append(match_dias)
        
        # Nível 3: Apenas curso
        match_curso = self.df_ofertas[mask_curso & mask_unidade & mask_data].copy()
        ofertas_ja_incluidas = match_completo['COD_OFERTA'].tolist() + match_dias['COD_OFERTA'].tolist()
        match_curso = match_curso[~match_curso['COD_OFERTA'].isin(ofertas_ja_incluidas)]
        if not match_curso.empty:
            match_curso['TIPO_INDICACAO'] = '2.OUTRA_UNIDADE'
            match_curso['NIVEL_MATCH'] = 'CURSO'
            resultados.append(match_curso)
        
        # Adiciona cálculo de distância
        if resultados:
            resultados_df = pd.concat(resultados)
            resultados_df = resultados_df.merge(
                self.df_unidades[['COD_UNIDADE', 'NOME_UNIDADE', 'LATITUDE', 'LONGITUDE']],
                left_on='COD_UNIDADE',
                right_on='COD_UNIDADE',
                how='left'
            )
            
            resultados_df['DISTANCIA_KM'] = resultados_df.apply(
                lambda row: self._calcular_distancia(
                    lat_interesse, lon_interesse,
                    row['LATITUDE'], row['LONGITUDE']
                ),
                axis=1
            )
            
            return resultados_df
        
        return pd.DataFrame()
    
    def _match_trilha_profissional(self, indice_interesse):
        """Match 3: Cursos da mesma trilha profissional"""
        dados_interesse = self.df_interesses.iloc[indice_interesse]
        cod_curso_interesse = dados_interesse['COD_CURSO']
        
        # Encontra trilha do curso
        trilha_curso = self.df_trilhas[self.df_trilhas['COD_CURSO'] == cod_curso_interesse]
        
        if trilha_curso.empty:
            return pd.DataFrame()
        
        area_profissional = trilha_curso['AREA_PROFISSIONAL'].iloc[0]
        
        # Busca outros cursos da mesma trilha
        cursos_trilha = self.df_trilhas[
            (self.df_trilhas['AREA_PROFISSIONAL'] == area_profissional) &
            (self.df_trilhas['COD_CURSO'] != cod_curso_interesse)
        ]['COD_CURSO'].tolist()
        
        if not cursos_trilha:
            return pd.DataFrame()
        
        # Busca ofertas desses cursos
        mask_cursos = self.df_ofertas['COD_CURSO'].isin(cursos_trilha)
        mask_unidade = self.df_ofertas['COD_UNIDADE'] == dados_interesse['COD_UNIDADE']
        mask_data = self.df_ofertas['DATA_CRIACAO'] >= pd.to_datetime(dados_interesse['DATA_INTERESSE'])
        
        resultados = self.df_ofertas[mask_cursos & mask_unidade & mask_data].copy()
        
        if not resultados.empty:
            resultados['TIPO_INDICACAO'] = '3.TRILHA_PROFISSIONAL'
            resultados['NIVEL_MATCH'] = 'AREA_PROFISSIONAL+MESMA_UNIDADE'
            resultados['AREA_PROFISSIONAL'] = area_profissional
        
        return resultados
    
    def _match_similaridade_semantica(self, indice_interesse):
        """Match 4: Cursos com títulos semanticamente similares"""
        dados_interesse = self.df_interesses.iloc[indice_interesse]
        cod_curso_interesse = dados_interesse['COD_CURSO']
        
        # Busca cursos similares
        cursos_similares, scores = self._buscar_cursos_similares(cod_curso_interesse, top_n=5)
        
        if not cursos_similares:
            return pd.DataFrame()
        
        # Busca ofertas desses cursos similares
        mask_cursos = self.df_ofertas['COD_CURSO'].isin(cursos_similares)
        mask_unidade = self.df_ofertas['COD_UNIDADE'] == dados_interesse['COD_UNIDADE']
        mask_data = self.df_ofertas['DATA_CRIACAO'] >= pd.to_datetime(dados_interesse['DATA_INTERESSE'])
        
        resultados = self.df_ofertas[mask_cursos & mask_unidade & mask_data].copy()
        
        if not resultados.empty:
            resultados['TIPO_INDICACAO'] = '4.SIMILARIDADE_SEMANTICA'
            resultados['NIVEL_MATCH'] = 'TITULO_SIMILAR+MESMA_UNIDADE'
            
            # Adiciona score de similaridade
            resultados['SCORE_SIMILARIDADE'] = resultados['COD_CURSO'].map(
                lambda x: scores.get(x, 0)
            )
        
        return resultados
    
    def _match_ead(self, indice_interesse):
        """Match 5: Cursos EAD similares"""
        dados_interesse = self.df_interesses.iloc[indice_interesse]
        cod_curso_interesse = dados_interesse['COD_CURSO']
        
        # Busca cursos EAD similares
        cursos_ead_similares, scores = self._buscar_cursos_similares(
            cod_curso_interesse, top_n=5, apenas_ead=True
        )
        
        if not cursos_ead_similares:
            return pd.DataFrame()
        
        # Busca ofertas EAD desses cursos
        mask_cursos = self.df_ofertas['COD_CURSO'].isin(cursos_ead_similares)
        mask_ead = self.df_ofertas['MODALIDADE_OFERTA'].str.contains('EAD', na=False)
        mask_data = self.df_ofertas['DATA_CRIACAO'] >= pd.to_datetime(dados_interesse['DATA_INTERESSE'])
        
        resultados = self.df_ofertas[mask_cursos & mask_ead & mask_data].copy()
        
        if not resultados.empty:
            resultados['TIPO_INDICACAO'] = '5.MODALIDADE_EAD'
            resultados['NIVEL_MATCH'] = 'CURSO_EAD_SIMILAR'
            resultados['SCORE_SIMILARIDADE'] = resultados['COD_CURSO'].map(
                lambda x: scores.get(x, 0)
            )
        
        return resultados
    
    def gerar_recomendacoes(self, cod_interesse):
        """
        Gera recomendações para um interesse específico.
        
        Args:
            cod_interesse: Código do registro de interesse
            
        Returns:
            DataFrame com todas as recomendações ordenadas por prioridade
        """
        # Encontra o índice do interesse
        interesse_idx = self.df_interesses[
            self.df_interesses['COD_INTERESSE'] == cod_interesse
        ].index
        
        if len(interesse_idx) == 0:
            print(f"⚠️ Nenhum interesse encontrado com código {cod_interesse}")
            return None
        
        idx = interesse_idx[0]
        dados_interesse = self.df_interesses.iloc[idx]
        
        print(f"\n🔍 Gerando recomendações para:")
        print(f"   Aluno: {dados_interesse['COD_ALUNO']}")
        print(f"   Curso: {dados_interesse['TITULO_INTERESSE']}")
        print(f"   Unidade: {dados_interesse['UNIDADE_INTERESSE']}")
        
        # Executa todas as estratégias de matching
        resultados = []
        
        print("\n📊 Executando estratégias de matching...")
        
        # 1. Mesma unidade
        print("   1. Mesmo curso na mesma unidade...")
        match1 = self._match_unidade_mesma(idx)
        resultados.append(match1)
        print(f"      ✅ Encontrados: {len(match1)}")
        
        # 2. Outras unidades
        print("   2. Mesmo curso em outras unidades...")
        match2 = self._match_unidade_outra(idx)
        resultados.append(match2)
        print(f"      ✅ Encontrados: {len(match2)}")
        
        # 3. Trilha profissional
        print("   3. Cursos da mesma trilha profissional...")
        match3 = self._match_trilha_profissional(idx)
        resultados.append(match3)
        print(f"      ✅ Encontrados: {len(match3)}")
        
        # 4. Similaridade semântica
        print("   4. Cursos com títulos similares...")
        match4 = self._match_similaridade_semantica(idx)
        resultados.append(match4)
        print(f"      ✅ Encontrados: {len(match4)}")
        
        # 5. EAD
        print("   5. Cursos EAD similares...")
        match5 = self._match_ead(idx)
        resultados.append(match5)
        print(f"      ✅ Encontrados: {len(match5)}")
        
        # Combina todos os resultados
        todos_resultados = pd.concat([r for r in resultados if not r.empty], ignore_index=True)
        
        if todos_resultados.empty:
            print("\n🚫 Nenhuma recomendação encontrada")
            return None
        
        # Adiciona informações do interesse
        todos_resultados['COD_ALUNO'] = dados_interesse['COD_ALUNO']
        todos_resultados['CURSO_INTERESSE'] = dados_interesse['TITULO_INTERESSE']
        todos_resultados['UNIDADE_INTERESSE'] = dados_interesse['UNIDADE_INTERESSE']
        todos_resultados['AREA_INTERESSE'] = dados_interesse['AREA_INTERESSE']
        todos_resultados['MODALIDADE_INTERESSE'] = dados_interesse['MODALIDADE_INTERESSE']
        
        # Ordenação por prioridade
        ordem_prioridade = {
            '1.MATCH_COMPLETO': 1,
            '2.OUTRA_UNIDADE': 2,
            '3.TRILHA_PROFISSIONAL': 3,
            '4.SIMILARIDADE_SEMANTICA': 4,
            '5.MODALIDADE_EAD': 5
        }
        
        todos_resultados['PRIORIDADE'] = todos_resultados['TIPO_INDICACAO'].map(ordem_prioridade)
        
        # Ordena por prioridade e distância
        if 'DISTANCIA_KM' in todos_resultados.columns:
            todos_resultados['DISTANCIA_KM'] = todos_resultados['DISTANCIA_KM'].fillna(0)
            todos_resultados = todos_resultados.sort_values(
                ['PRIORIDADE', 'DISTANCIA_KM', 'SCORE_SIMILARIDADE'],
                ascending=[True, True, False]
            )
        else:
            todos_resultados = todos_resultados.sort_values(
                ['PRIORIDADE', 'SCORE_SIMILARIDADE'],
                ascending=[True, False]
            )
        
        # Filtra similaridades alta
        '''
        Similaridade cosseno varia de 0 a 1:

        1.0 = curso idêntico (mesmo embedding)

        0.0 = curso totalmente diferente

        > 0.7 geralmente indica similaridade "boa o suficiente"
        
        '''
        if 'SCORE_SIMILARIDADE' in todos_resultados.columns:
            todos_resultados = todos_resultados[
                (todos_resultados['SCORE_SIMILARIDADE'].isna()) |   #Mantém recomendações não baseadas em similaridade
                (todos_resultados['SCORE_SIMILARIDADE'] > 0.7)  # Mantém apenas recomendações COM ALTA similaridade
            ]
        
        print(f"\n✅ Total de recomendações geradas: {len(todos_resultados)}")
        
        return todos_resultados
    
    def listar_interesses_disponiveis(self):
        """Retorna lista de interesses disponíveis para consulta"""
        return self.df_interesses[['COD_INTERESSE', 'COD_ALUNO', 'TITULO_INTERESSE', 'UNIDADE_INTERESSE']].head(20)
       