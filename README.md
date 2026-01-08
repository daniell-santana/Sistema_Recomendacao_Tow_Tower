# Sistema de Recomendação Two-tower

Este projeto demonstra um exemplo de sistema de recomendação híbrido para oferta de cursos educacionais, combinando múltiplas estratégias de matching entre interesses de alunos e ofertas de cursos.

### 🔄 Fluxo
```mermaid
flowchart TB
    A[Entrada do Usuario<br/>Portal de Cursos] --> B[Coleta de Interacoes<br/>Clicks | Navegacao | Historico]

    subgraph TT[Two Tower Retrieval Model]
        direction LR

        subgraph UT[User Representation]
            C[User Features] --> D[User Encoder]
            D --> E[User Embedding]
        end

        subgraph IT[Item Representation]
            F[Course Features] --> G[Item Encoder]
            G --> H[Item Embedding]
        end

        E --> I[Similarity Scoring]
        H --> I
    end

    B --> C
    B --> F

    I --> J[Ranking and Filtering]
    J --> K[Top N Recommendations]
```
## 🎯 Funcionalidades

- **Matching Exato**: Curso + Localidade + Horário + turno + Data
- **Similaridade Semântica**: Embeddings de títulos de cursos
- **Trilhas Profissionais**: Cursos relacionados por área de formação
- **Filtro Geográfico**: Distância entre unidades
- **Modalidade EAD**: Recomendações para ensino a distância

## 🏗️ Arquitetura

1. **Carregamento e Pré-processamento** de bases (cursos, ofertas, interesses)
2. **Geração de Embeddings** usando modelo multilingual SentenceTransformer
3. **Múltiplas Estratégias de Matching** hierárquico
4. **Interface Streamlit** para demonstração interativa
5. **CLI** para uso em batch

## 🔧 Tecnologias

- Python 3.10+
- SentenceTransformers para embeddings
- Streamlit para interface web
- Pandas, NumPy para manipulação de dados
- Scikit-learn para similaridade cosseno

## 📁 Estrutura do Código
src/

├── sistema_recomendacao.py # Classe principal com lógica de recomendação

├── app_streamlit.py # Interface web interativa

└── main_cli.py # Interface de linha de comando


📊 Estratégias de Recomendação
1. O sistema implementa 7 níveis de recomendação:
2. Curso + Unidade: Match completo na mesma localidade
3. Curso sem Unidade: Mesmo curso em outras localidades
4. Ocupações Similares: Cursos da mesma trilha profissional
5. Títulos Similares: Cursos com nomes semanticamente próximos
6. EAD: Oferece cursos, quando o curso de interesse do usuário está distante da sua localidade

🔍 Detalhes Técnicos
1. Modelo de Embeddings: paraphrase-multilingual-mpnet-base-v2
2. Similaridade: Cosine similarity sobre embeddings
3. Pré-processamento: Filtragem por data de oferta do curso, modalidade de ensino, área, nível, status
4. Ordenação: Prioridade por tipo de match + distância (Geoloc)
