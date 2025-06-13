"""
Script para análise e visualização dos resultados dos testes de sentimento.
"""
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import os
import glob

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_test_results():
    """Carrega os resultados mais recentes dos testes."""
    # Procurar pelo arquivo de resultados mais recente
    result_files = glob.glob("test_results_*.json")
    
    if not result_files:
        print("❌ Nenhum arquivo de resultados encontrado.")
        print("Execute primeiro o script generate_test_data.py")
        return None
    
    # Pegar o arquivo mais recente
    latest_file = max(result_files, key=os.path.getctime)
    print(f"📂 Carregando resultados de: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        return results
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        return None

def analyze_results(results):
    """Analisa os resultados dos testes."""
    if not results:
        return
    
    df = pd.DataFrame(results)
    
    print("\n📊 ANÁLISE DETALHADA DOS RESULTADOS")
    print("=" * 60)
    
    # Estatísticas gerais
    total = len(df)
    correct = df['is_correct'].sum()
    accuracy = (correct / total) * 100
    
    print(f"Total de testes: {total}")
    print(f"Acertos: {correct}")
    print(f"Erros: {total - correct}")
    print(f"Acurácia geral: {accuracy:.1f}%")
    
    # Análise por sentimento esperado
    print("\n📈 PERFORMANCE POR SENTIMENTO:")
    print("-" * 40)
    
    for sentiment in ['positiva', 'negativa', 'neutra']:
        sentiment_df = df[df['expected_sentiment'] == sentiment]
        if len(sentiment_df) > 0:
            sentiment_correct = sentiment_df['is_correct'].sum()
            sentiment_total = len(sentiment_df)
            sentiment_accuracy = (sentiment_correct / sentiment_total) * 100
            
            print(f"{sentiment.capitalize():10}: {sentiment_correct:2d}/{sentiment_total:2d} ({sentiment_accuracy:5.1f}%)")
    
    # Matriz de confusão
    print("\n🔄 MATRIZ DE CONFUSÃO:")
    print("-" * 40)
    confusion_matrix = pd.crosstab(
        df['expected_sentiment'], 
        df['predicted_sentiment'], 
        margins=True
    )
    print(confusion_matrix)
    
    # Análise de confiança
    print("\n🎯 ANÁLISE DE CONFIANÇA:")
    print("-" * 40)
    df['confidence_float'] = df['confidence_score'].astype(float)
    
    print(f"Confiança média: {df['confidence_float'].mean():.3f}")
    print(f"Confiança mediana: {df['confidence_float'].median():.3f}")
    print(f"Confiança mínima: {df['confidence_float'].min():.3f}")
    print(f"Confiança máxima: {df['confidence_float'].max():.3f}")
    
    # Confiança por acerto/erro
    correct_confidence = df[df['is_correct']]['confidence_float'].mean()
    incorrect_confidence = df[~df['is_correct']]['confidence_float'].mean()
    
    print(f"Confiança média (acertos): {correct_confidence:.3f}")
    print(f"Confiança média (erros): {incorrect_confidence:.3f}")
    
    return df

def create_visualizations(df):
    """Cria visualizações dos resultados."""
    if df is None or len(df) == 0:
        return
    
    # Configurar figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Análise de Performance - Sentiment Analysis API', fontsize=16, fontweight='bold')
    
    # 1. Gráfico de acurácia por sentimento
    sentiment_stats = []
    for sentiment in ['positiva', 'negativa', 'neutra']:
        sentiment_df = df[df['expected_sentiment'] == sentiment]
        if len(sentiment_df) > 0:
            accuracy = (sentiment_df['is_correct'].sum() / len(sentiment_df)) * 100
            sentiment_stats.append({'Sentimento': sentiment.capitalize(), 'Acurácia': accuracy})
    
    sentiment_df_plot = pd.DataFrame(sentiment_stats)
    bars = axes[0, 0].bar(sentiment_df_plot['Sentimento'], sentiment_df_plot['Acurácia'], 
                         color=['#2ecc71', '#e74c3c', '#f39c12'])
    axes[0, 0].set_title('Acurácia por Sentimento')
    axes[0, 0].set_ylabel('Acurácia (%)')
    axes[0, 0].set_ylim(0, 100)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.1f}%', ha='center', va='bottom')
    
    # 2. Matriz de confusão como heatmap
    confusion_matrix = pd.crosstab(df['expected_sentiment'], df['predicted_sentiment'])
    sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', ax=axes[0, 1])
    axes[0, 1].set_title('Matriz de Confusão')
    axes[0, 1].set_xlabel('Sentimento Predito')
    axes[0, 1].set_ylabel('Sentimento Esperado')
    
    # 3. Distribuição de confiança
    df['confidence_float'] = df['confidence_score'].astype(float)
    axes[1, 0].hist(df['confidence_float'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[1, 0].set_title('Distribuição dos Scores de Confiança')
    axes[1, 0].set_xlabel('Score de Confiança')
    axes[1, 0].set_ylabel('Frequência')
    
    # 4. Confiança por acerto/erro
    correct_conf = df[df['is_correct']]['confidence_float']
    incorrect_conf = df[~df['is_correct']]['confidence_float']
    
    axes[1, 1].boxplot([correct_conf, incorrect_conf], labels=['Acertos', 'Erros'])
    axes[1, 1].set_title('Confiança: Acertos vs Erros')
    axes[1, 1].set_ylabel('Score de Confiança')
    
    plt.tight_layout()
    
    # Salvar gráfico
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sentiment_analysis_report_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n📊 Gráficos salvos em: {filename}")
    
    plt.show()

def generate_detailed_report(df):
    """Gera relatório detalhado em texto."""
    if df is None:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_filename = f"sentiment_analysis_detailed_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DETALHADO - ANÁLISE DE SENTIMENTO\n")
        f.write("=" * 60 + "\n")
        f.write(f"Data/Hora: {timestamp}\n")
        f.write(f"Total de testes: {len(df)}\n\n")
        
        # Estatísticas gerais
        total = len(df)
        correct = df['is_correct'].sum()
        accuracy = (correct / total) * 100
        
        f.write("ESTATÍSTICAS GERAIS:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Acurácia geral: {accuracy:.1f}%\n")
        f.write(f"Acertos: {correct}/{total}\n")
        f.write(f"Erros: {total - correct}/{total}\n\n")
        
        # Performance por sentimento
        f.write("PERFORMANCE POR SENTIMENTO:\n")
        f.write("-" * 30 + "\n")
        
        for sentiment in ['positiva', 'negativa', 'neutra']:
            sentiment_df = df[df['expected_sentiment'] == sentiment]
            if len(sentiment_df) > 0:
                sentiment_correct = sentiment_df['is_correct'].sum()
                sentiment_total = len(sentiment_df)
                sentiment_accuracy = (sentiment_correct / sentiment_total) * 100
                
                f.write(f"{sentiment.capitalize()}: {sentiment_accuracy:.1f}% ({sentiment_correct}/{sentiment_total})\n")
        
        # Casos de erro
        f.write("\nCASOS DE ERRO:\n")
        f.write("-" * 30 + "\n")
        
        errors = df[~df['is_correct']]
        for _, row in errors.iterrows():
            f.write(f"Cliente: {row['customer_name']}\n")
            f.write(f"Texto: {row['review_text'][:100]}...\n")
            f.write(f"Esperado: {row['expected_sentiment']} | Predito: {row['predicted_sentiment']}\n")
            f.write(f"Confiança: {row['confidence_score']}\n")
            f.write("-" * 50 + "\n")
    
    print(f"📄 Relatório detalhado salvo em: {report_filename}")

def main():
    """Função principal."""
    print("📊 ANALISADOR DE RESULTADOS - SENTIMENT ANALYSIS API")
    print("=" * 60)
    
    # Carregar resultados
    results = load_test_results()
    
    if not results:
        return
    
    # Analisar resultados
    df = analyze_results(results)
    
    if df is not None:
        # Criar visualizações
        create_visualizations(df)
        
        # Gerar relatório detalhado
        generate_detailed_report(df)
        
        print("\n✨ Análise concluída!")
        print("📁 Arquivos gerados:")
        print("  - Gráficos: sentiment_analysis_report_*.png")
        print("  - Relatório: sentiment_analysis_detailed_report_*.txt")

if __name__ == "__main__":
    main()

