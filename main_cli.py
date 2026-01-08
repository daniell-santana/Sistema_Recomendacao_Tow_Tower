"""
Interface de Linha de Comando (CLI) para o Sistema de Recomendação
Permite uso em batch e integração com outros sistemas.
"""

from sistema_recomendacao import SistemaRecomendacaoCursos
from dotenv import load_dotenv
import os
import pandas as pd
import argparse
import sys

def main():
    """Função principal da CLI"""
    parser = argparse.ArgumentParser(
        description='Sistema de Recomendação de Cursos - CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  %(prog)s --interesse 12345
  %(prog)s --interesse 12345 --output recomendacoes.csv
  %(prog)s --batch interesses.csv --output-dir resultados/
  %(prog)s --stats
        '''
    )
    
    # Argumentos
    parser.add_argument('--interesse', type=int, help='Código do interesse a processar')
    parser.add_argument('--output', help='Arquivo para salvar resultados (CSV)')
    parser.add_argument('--batch', help='Arquivo CSV com lista de interesses')
    parser.add_argument('--output-dir', help='Diretório para salvar resultados em batch')
    parser.add_argument('--stats', action='store_true', help='Mostrar estatísticas do sistema')
    parser.add_argument('--list', action='store_true', help='Listar interesses disponíveis')
    
    args = parser.parse_args()
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Caminhos das bases
    OFERTAS_PATH = os.getenv('OFERTAS_PATH')
    INTERESSES_PATH = os.getenv('INTERESSES_PATH')
    ESTRUTURA_PATH = os.getenv('ESTRUTURA_PATH')
    
    if not all([OFERTAS_PATH, INTERESSES_PATH, ESTRUTURA_PATH]):
        print("❌ Erro: Configure as variáveis de ambiente:")
        print("   OFERTAS_PATH, INTERESSES_PATH, ESTRUTURA_PATH")
        sys.exit(1)
    
    # Inicializa o sistema
    print("🚀 Inicializando Sistema de Recomendação...")
    try:
        sistema = SistemaRecomendacaoCursos(
            path_interesses=INTERESSES_PATH,
            path_ofertas=OFERTAS_PATH,
            path_estrutura=ESTRUTURA_PATH
        )
        print("✅ Sistema inicializado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema: {e}")
        sys.exit(1)
    
    # Modo: Estatísticas
    if args.stats:
        mostrar_estatisticas(sistema)
        return
    
    # Modo: Listar interesses
    if args.list:
        listar_interesses(sistema)
        return
    
    # Modo: Processamento em batch
    if args.batch:
        processar_batch(sistema, args.batch, args.output_dir)
        return
    
    # Modo: Interesse único
    if args.interesse:
        processar_interesse(sistema, args.interesse, args.output)
        return
    
    # Modo interativo
    modo_interativo(sistema)

def mostrar_estatisticas(sistema):
    """Mostra estatísticas do sistema"""
    print("📊 ESTATÍSTICAS DO SISTEMA")
    print("=" * 40)
    print(f"Cursos Cadastrados:     {len(sistema.df_cursos):>10}")
    print(f"Ofertas Ativas:         {len(sistema.df_ofertas):>10}")
    print(f"Interesses Registrados: {len(sistema.df_interesses):>10}")
    print(f"Unidades/Campi:         {len(sistema.df_unidades):>10}")
    print(f"Trilhas Profissionais:  {sistema.df_trilhas['AREA_PROFISSIONAL'].nunique():>10}")
    print("=" * 40)
    
    # Top 5 cursos mais procurados
    print("\n🏆 TOP 5 CURSOS MAIS PROCURADOS:")
    top_cursos = sistema.df_interesses['TITULO_INTERESSE'].value_counts().head(5)
    for i, (curso, qtd) in enumerate(top_cursos.items(), 1):
        print(f"  {i}. {curso[:40]:40} ({qtd:4} interesses)")
    
    # Distribuição por modalidade
    print("\n📈 DISTRIBUIÇÃO POR MODALIDADE:")
    mod_interesses = sistema.df_interesses['MODALIDADE_INTERESSE'].value_counts()
    for modalidade, qtd in mod_interesses.items():
        percentual = (qtd / len(sistema.df_interesses)) * 100
        print(f"  {modalidade:20} {qtd:6} ({percentual:5.1f}%)")

def listar_interesses(sistema):
    """Lista interesses disponíveis"""
    interesses = sistema.listar_interesses_disponiveis()
    
    print("📝 INTERESSES DISPONÍVEIS PARA RECOMENDAÇÃO")
    print("=" * 80)
    print(f"{'Código':<10} {'Aluno':<15} {'Curso':<40} {'Unidade':<20}")
    print("-" * 80)
    
    for _, row in interesses.iterrows():
        curso_abrev = row['TITULO_INTERESSE'][:37] + "..." if len(row['TITULO_INTERESSE']) > 40 else row['TITULO_INTERESSE']
        print(f"{row['COD_INTERESSE']:<10} {row['COD_ALUNO']:<15} {curso_abrev:<40} {row['UNIDADE_INTERESSE'][:17]:<20}")
    
    print("=" * 80)
    print(f"Total: {len(interesses)} interesses listados")

def processar_interesse(sistema, cod_interesse, output_file=None):
    """Processa um único interesse"""
    print(f"🔍 Processando interesse: {cod_interesse}")
    
    try:
        recomendacoes = sistema.gerar_recomendacoes(cod_interesse)
        
        if recomendacoes is None or recomendacoes.empty:
            print(f"⚠️  Nenhuma recomendação encontrada para o interesse {cod_interesse}")
            return
        
        # Mostra resumo
        print(f"✅  {len(recomendacoes)} recomendações encontradas")
        
        # Distribuição por tipo
        print("\n📊 Distribuição por tipo de recomendação:")
        dist = recomendacoes['TIPO_INDICACAO'].value_counts()
        for tipo, qtd in dist.items():
            print(f"  {tipo:30} {qtd:4} ({qtd/len(recomendacoes)*100:5.1f}%)")
        
        # Top 5 recomendações
        print("\n🏅 TOP 5 RECOMENDAÇÕES:")
        top5 = recomendacoes.head(5)
        for i, (_, rec) in enumerate(top5.iterrows(), 1):
            distancia = f"{rec.get('DISTANCIA_KM', 0):.1f} km" if 'DISTANCIA_KM' in rec else "N/A"
            similaridade = f"{rec.get('SCORE_SIMILARIDADE', 0):.3f}" if 'SCORE_SIMILARIDADE' in rec else "N/A"
            
            print(f"  {i}. {rec['TITULO_OFERTA'][:40]:40}")
            print(f"     Tipo: {rec['TIPO_INDICACAO']:20} | Unidade: {rec.get('NOME_UNIDADE', 'N/A')}")
            print(f"     Distância: {distancia:10} | Similaridade: {similaridade:8}")
        
        # Salva em arquivo se solicitado
        if output_file:
            if not output_file.endswith('.csv'):
                output_file += '.csv'
            
            # Colunas para salvar
            cols_save = [
                'TIPO_INDICACAO', 'NIVEL_MATCH', 'COD_OFERTA',
                'TITULO_OFERTA', 'AREA_OFERTA', 'MODALIDADE_OFERTA',
                'NOME_UNIDADE', 'DATA_INICIO', 'COD_ALUNO',
                'CURSO_INTERESSE', 'UNIDADE_INTERESSE'
            ]
            
            if 'DISTANCIA_KM' in recomendacoes.columns:
                cols_save.append('DISTANCIA_KM')
            
            if 'SCORE_SIMILARIDADE' in recomendacoes.columns:
                cols_save.append('SCORE_SIMILARIDADE')
            
            recomendacoes[cols_save].to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n💾 Resultados salvos em: {output_file}")
    
    except Exception as e:
        print(f"❌ Erro ao processar interesse {cod_interesse}: {e}")

def processar_batch(sistema, batch_file, output_dir=None):
    """Processa múltiplos interesses de um arquivo"""
    print(f"📦 Processando em batch: {batch_file}")
    
    try:
        # Lê a lista de interesses
        batch_df = pd.read_csv(batch_file)
        
        if 'COD_INTERESSE' not in batch_df.columns:
            print("❌ Arquivo batch deve conter coluna 'COD_INTERESSE'")
            return
        
        interesses = batch_df['COD_INTERESSE'].tolist()
        print(f"📋 {len(interesses)} interesses para processar")
        
        # Processa cada interesse
        resultados_totais = []
        
        for i, cod_interesse in enumerate(interesses, 1):
            print(f"\n[{i}/{len(interesses)}] Processando: {cod_interesse}")
            
            try:
                recomendacoes = sistema.gerar_recomendacoes(cod_interesse)
                
                if recomendacoes is not None and not recomendacoes.empty:
                    recomendacoes['COD_INTERESSE_ORIGEM'] = cod_interesse
                    resultados_totais.append(recomendacoes)
                    print(f"   ✅ {len(recomendacoes)} recomendações")
                else:
                    print(f"   ⚠️  Nenhuma recomendação")
            
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                continue
        
        # Consolida resultados
        if resultados_totais:
            resultados_consolidados = pd.concat(resultados_totais, ignore_index=True)
            
            # Salva resultados
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"recomendacoes_batch_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv")
            else:
                output_path = f"recomendacoes_batch_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            resultados_consolidados.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"\n🎉 PROCESSAMENTO BATCH CONCLUÍDO")
            print(f"   Total de interesses processados: {len(interesses)}")
            print(f"   Total de recomendações geradas: {len(resultados_consolidados)}")
            print(f"   Arquivo de saída: {output_path}")
            
            # Estatísticas do batch
            print(f"\n📊 ESTATÍSTICAS DO BATCH:")
            print(f"   Média de recomendações por interesse: {len(resultados_consolidados)/len(interesses):.1f}")
            
            dist_tipo = resultados_consolidados['TIPO_INDICACAO'].value_counts()
            for tipo, qtd in dist_tipo.items():
                percent = (qtd / len(resultados_consolidados)) * 100
                print(f"   {tipo:30} {qtd:6} ({percent:5.1f}%)")
        else:
            print("\n⚠️  Nenhuma recomendação gerada no processamento batch")
    
    except Exception as e:
        print(f"❌ Erro no processamento batch: {e}")

def modo_interativo(sistema):
    """Modo interativo da CLI"""
    print("\n" + "=" * 60)
    print("MODO INTERATIVO - SISTEMA DE RECOMENDAÇÃO")
    print("=" * 60)
    print("\nComandos disponíveis:")
    print("  [número]  - Processar interesse específico")
    print("  list      - Listar interesses disponíveis")
    print("  stats     - Mostrar estatísticas")
    print("  exit      - Sair do sistema")
    print("-" * 60)
    
    while True:
        try:
            comando = input("\n> ").strip().lower()
            
            if comando == 'exit' or comando == 'quit':
                print("\n👋 Encerrando sistema. Até logo!")
                break
            
            elif comando == 'list':
                listar_interesses(sistema)
            
            elif comando == 'stats':
                mostrar_estatisticas(sistema)
            
            elif comando.isdigit():
                cod_interesse = int(comando)
                processar_interesse(sistema, cod_interesse)
            
            else:
                print("❌ Comando inválido. Use 'list', 'stats', [número] ou 'exit'")
        
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando sistema.")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()