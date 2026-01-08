# Sistema de Recomendação de Cursos

Sistema híbrido de recomendação para instituições de ensino que combina:
- Filtragem baseada em atributos (local, horário, data)
- Similaridade semântica de títulos de cursos
- Trilhas de formação profissional

## Funcionalidades
1. **Recomendações baseadas em preferências**: Match exato de curso + local + horário
2. **Recomendações por similaridade**: Cursos semanticamente similares
3. **Recomendações por trilha profissional**: Cursos da mesma área de formação
4. **Recomendações EAD**: Cursos a distância similares
5. **Filtro geográfico**: Distância entre unidades

## Tecnologias
- Python 3.10+
- SentenceTransformer (paraphrase-multilingual-mpnet-base-v2)
- Streamlit (interface web)
- Pandas, NumPy
- Scikit-learn (cosine similarity)
