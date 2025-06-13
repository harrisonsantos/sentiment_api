"""
Script para gerar dados de teste para a API de análise de sentimento.
"""
import requests
import json
import time
from datetime import datetime, timedelta
import random

# Configurações
API_BASE_URL = "http://localhost:8000/api/v1"

# Dados de teste com diferentes sentimentos
TEST_REVIEWS = [
    # Avaliações POSITIVAS em português
    {
        "customer_name": "Ana Silva",
        "review_text": "Excelente atendimento! A equipe foi muito prestativa e resolveu meu problema rapidamente. Superou minhas expectativas!",
        "expected_sentiment": "positiva"
    },
    {
        "customer_name": "Bruno Santos",
        "review_text": "Estou extremamente satisfeito com o serviço. Qualidade incrível e atendimento dedicado. Recomendo para todos!",
        "expected_sentiment": "positiva"
    },
    {
        "customer_name": "Carla Oliveira",
        "review_text": "Fantástico! O produto funcionou perfeitamente e o suporte foi ágil. Adorei a experiência!",
        "expected_sentiment": "positiva"
    },
    {
        "customer_name": "Daniel Costa",
        "review_text": "Serviço de alta qualidade. A equipe é muito eficiente e atenciosa. Estou muito feliz com o resultado.",
        "expected_sentiment": "positiva"
    },
    {
        "customer_name": "Eduarda Lima",
        "review_text": "Maravilhoso! Tudo funcionou como esperado. O atendimento foi rápido e profissional.",
        "expected_sentiment": "positiva"
    },
    
    # Avaliações NEGATIVAS em português
    {
        "customer_name": "Fernando Rocha",
        "review_text": "Péssimo atendimento! Demorou muito para resolver meu problema e ainda ficou mal resolvido. Muito insatisfeito.",
        "expected_sentiment": "negativa"
    },
    {
        "customer_name": "Gabriela Martins",
        "review_text": "Terrível experiência. O produto não funcionou e o suporte foi despreparado. Não recomendo!",
        "expected_sentiment": "negativa"
    },
    {
        "customer_name": "Henrique Alves",
        "review_text": "Muito ruim! Tive vários problemas e ninguém conseguiu me ajudar adequadamente. Decepcionante.",
        "expected_sentiment": "negativa"
    },
    {
        "customer_name": "Isabela Ferreira",
        "review_text": "Horrível! O serviço foi lento, ineficiente e o atendente foi grosseiro. Experiência frustrante.",
        "expected_sentiment": "negativa"
    },
    {
        "customer_name": "João Pereira",
        "review_text": "Insatisfeito com o serviço. Muitos erros, demora excessiva e falta de profissionalismo.",
        "expected_sentiment": "negativa"
    },
    
    # Avaliações NEUTRAS em português
    {
        "customer_name": "Karina Souza",
        "review_text": "O atendimento foi ok, nada excepcional. Resolveu o problema básico, mas poderia ser melhor.",
        "expected_sentiment": "neutra"
    },
    {
        "customer_name": "Lucas Barbosa",
        "review_text": "Serviço mediano. Funcionou, mas não impressionou. Atendimento dentro do esperado.",
        "expected_sentiment": "neutra"
    },
    {
        "customer_name": "Mariana Dias",
        "review_text": "Experiência regular. Algumas coisas boas, outras nem tanto. No geral, foi aceitável.",
        "expected_sentiment": "neutra"
    },
    {
        "customer_name": "Nicolas Ribeiro",
        "review_text": "O produto funciona conforme descrito. Nada de especial, mas cumpre o que promete.",
        "expected_sentiment": "neutra"
    },
    {
        "customer_name": "Olivia Castro",
        "review_text": "Atendimento padrão. Não tive problemas, mas também não foi nada extraordinário.",
        "expected_sentiment": "neutra"
    },
    
    # Avaliações em INGLÊS (para testar fallback)
    {
        "customer_name": "Peter Johnson",
        "review_text": "Amazing service! The team was incredibly helpful and solved my issue quickly. Highly recommended!",
        "expected_sentiment": "positiva"
    },
    {
        "customer_name": "Sarah Williams",
        "review_text": "Terrible experience. The product didn't work and customer support was unhelpful. Very disappointed.",
        "expected_sentiment": "negativa"
    },
    {
        "customer_name": "Mike Davis",
        "review_text": "The service was okay. Nothing special, but it got the job done. Average experience overall.",
        "expected_sentiment": "neutra"
    },
    
    # Avaliações MISTAS/COMPLEXAS
    {
        "customer_name": "Patricia Gomes",
        "review_text": "O produto é bom, mas o atendimento deixou a desejar. Resolvi meu problema, porém demorou mais que o esperado.",
        "expected_sentiment": "neutra"
    },
    {
        "customer_name": "Roberto Silva",
        "review_text": "Gostei do serviço em geral, mas houve alguns problemas técnicos no início. Depois foi tudo bem.",
        "expected_sentiment": "neutra"
    },
    
    # Avaliações com EMOJIS e linguagem informal
    {
        "customer_name": "Tatiana Lopes",
        "review_text": "Top demais! 😍 Adorei o atendimento, super rápido e eficiente. Nota 10! 👏",
        "expected_sentiment": "positiva"
    },
    {
        "customer_name": "Vinicius Moura",
        "review_text": "Que decepção... 😞 Esperava muito mais. O serviço foi bem fraco mesmo.",
        "expected_sentiment": "negativa"
    }
]


def test_api_connection():
    """Testa se a API está funcionando."""
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}/health")
        if response.status_code == 200:
            print("✅ API está funcionando!")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que ela está rodando.")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {e}")
        return False


def create_review(review_data):
    """Cria uma avaliação via API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/reviews",
            json={
                "customer_name": review_data["customer_name"],
                "review_text": review_data["review_text"]
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            return result
        else:
            print(f"❌ Erro ao criar avaliação: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None


def generate_test_data():
    """Gera dados de teste na API."""
    print("🚀 Iniciando geração de dados de teste...")
    print(f"📊 Total de avaliações a serem criadas: {len(TEST_REVIEWS)}")
    print()
    
    # Testar conexão primeiro
    if not test_api_connection():
        return
    
    results = []
    correct_predictions = 0
    total_predictions = 0
    
    print("📝 Criando avaliações de teste...")
    print("-" * 80)
    
    for i, review_data in enumerate(TEST_REVIEWS, 1):
        print(f"[{i:2d}/{len(TEST_REVIEWS)}] {review_data['customer_name']}")
        
        # Criar avaliação
        result = create_review(review_data)
        
        if result:
            predicted_sentiment = result["sentiment"]
            expected_sentiment = review_data["expected_sentiment"]
            confidence = result["confidence_score"]
            
            # Verificar se a predição está correta
            is_correct = predicted_sentiment == expected_sentiment
            if is_correct:
                correct_predictions += 1
            total_predictions += 1
            
            # Mostrar resultado
            status_icon = "✅" if is_correct else "❌"
            print(f"    {status_icon} Esperado: {expected_sentiment} | Predito: {predicted_sentiment} | Confiança: {confidence}")
            
            # Armazenar resultado
            results.append({
                "id": result["id"],
                "customer_name": review_data["customer_name"],
                "review_text": review_data["review_text"],
                "expected_sentiment": expected_sentiment,
                "predicted_sentiment": predicted_sentiment,
                "confidence_score": confidence,
                "is_correct": is_correct
            })
            
        else:
            print("    ❌ Falha ao criar avaliação")
        
        # Pequena pausa para não sobrecarregar a API
        time.sleep(0.5)
    
    print("-" * 80)
    print("📊 RESUMO DOS RESULTADOS:")
    print(f"Total de avaliações criadas: {total_predictions}")
    print(f"Predições corretas: {correct_predictions}")
    print(f"Predições incorretas: {total_predictions - correct_predictions}")
    
    if total_predictions > 0:
        accuracy = (correct_predictions / total_predictions) * 100
        print(f"Acurácia: {accuracy:.1f}%")
    
    # Mostrar estatísticas por sentimento
    print("\n📈 ESTATÍSTICAS POR SENTIMENTO:")
    sentiments = ["positiva", "negativa", "neutra"]
    
    for sentiment in sentiments:
        expected_count = len([r for r in results if r["expected_sentiment"] == sentiment])
        predicted_count = len([r for r in results if r["predicted_sentiment"] == sentiment])
        correct_count = len([r for r in results if r["expected_sentiment"] == sentiment and r["is_correct"]])
        
        if expected_count > 0:
            sentiment_accuracy = (correct_count / expected_count) * 100
            print(f"  {sentiment.capitalize()}: {correct_count}/{expected_count} corretas ({sentiment_accuracy:.1f}%)")
    
    return results


def show_examples():
    """Mostra exemplos de como usar a API."""
    print("\n🔧 EXEMPLOS DE USO DA API:")
    print("-" * 50)
    
    print("1. Criar uma avaliação:")
    print("""
curl -X POST "http://localhost:8000/api/v1/reviews" \\
  -H "Content-Type: application/json" \\
  -d '{
    "customer_name": "Teste Usuario",
    "review_text": "Excelente serviço, muito satisfeito!"
  }'
""")
    
    print("2. Listar todas as avaliações:")
    print("""
curl -X GET "http://localhost:8000/api/v1/reviews"
""")
    
    print("3. Buscar avaliação por ID:")
    print("""
curl -X GET "http://localhost:8000/api/v1/reviews/1"
""")
    
    print("4. Gerar relatório:")
    print("""
curl -X GET "http://localhost:8000/api/v1/reviews/report?start_date=2024-01-01&end_date=2024-12-31"
""")


def main():
    """Função principal."""
    print("=" * 80)
    print("🧪 GERADOR DE DADOS DE TESTE - SENTIMENT ANALYSIS API")
    print("=" * 80)
    
    # Gerar dados de teste
    results = generate_test_data()
    
    if results:
        # Salvar resultados em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Resultados salvos em: {filename}")
    
    # Mostrar exemplos de uso
    show_examples()
    
    print("\n✨ Geração de dados de teste concluída!")


if __name__ == "__main__":
    main()

