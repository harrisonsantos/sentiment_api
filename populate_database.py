"""
Script para popular o banco de dados com dados de exemplo para demonstração.
Este script cria avaliações diretamente no banco sem usar a API.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Adicionar o diretório da aplicação ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Review, SessionLocal, create_tables
from app.sentiment_service import SentimentAnalyzer

# Dados de exemplo para popular o banco
SAMPLE_REVIEWS = [
    # Avaliações positivas
    ("Maria Silva", "Excelente atendimento! Muito satisfeita com o serviço prestado."),
    ("João Santos", "Produto de alta qualidade, superou minhas expectativas!"),
    ("Ana Costa", "Equipe muito prestativa e eficiente. Recomendo!"),
    ("Pedro Oliveira", "Serviço rápido e profissional. Adorei a experiência!"),
    ("Carla Lima", "Fantástico! Tudo funcionou perfeitamente."),
    
    # Avaliações negativas
    ("Roberto Ferreira", "Péssimo atendimento, muito demorado e ineficiente."),
    ("Juliana Rocha", "Produto com defeito e suporte não resolveu o problema."),
    ("Carlos Almeida", "Experiência terrível, não recomendo para ninguém."),
    ("Fernanda Dias", "Muito insatisfeita com o serviço prestado."),
    ("Ricardo Gomes", "Atendimento ruim e produto de baixa qualidade."),
    
    # Avaliações neutras
    ("Luciana Martins", "Serviço ok, nada excepcional mas cumpriu o básico."),
    ("Marcos Barbosa", "Produto mediano, funciona mas poderia ser melhor."),
    ("Patricia Souza", "Atendimento padrão, sem grandes problemas ou elogios."),
    ("André Ribeiro", "Experiência regular, dentro do esperado."),
    ("Camila Castro", "Serviço aceitável, mas há espaço para melhorias."),
    
    # Avaliações em inglês
    ("John Smith", "Amazing service! Very satisfied with the quality."),
    ("Sarah Johnson", "Terrible experience, would not recommend."),
    ("Mike Wilson", "Average service, nothing special but okay."),
    
    # Avaliações mistas
    ("Beatriz Lopes", "O produto é bom, mas o atendimento deixou a desejar."),
    ("Gabriel Moura", "Gostei do serviço em geral, mas houve alguns problemas."),
]

def create_sample_data():
    """Cria dados de exemplo no banco de dados."""
    print("🗄️ Criando dados de exemplo no banco de dados...")
    
    # Criar tabelas se não existirem
    create_tables()
    
    # Inicializar analisador de sentimento
    analyzer = SentimentAnalyzer()
    
    # Criar sessão do banco
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        existing_count = db.query(Review).count()
        if existing_count > 0:
            print(f"⚠️ Já existem {existing_count} avaliações no banco.")
            response = input("Deseja adicionar mais dados? (s/n): ")
            if response.lower() != 's':
                print("❌ Operação cancelada.")
                return
        
        created_count = 0
        
        for customer_name, review_text in SAMPLE_REVIEWS:
            # Analisar sentimento
            sentiment, confidence = analyzer.analyze_sentiment(review_text)
            
            # Criar data aleatória nos últimos 30 dias
            days_ago = random.randint(0, 30)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            # Criar review
            review = Review(
                customer_name=customer_name,
                review_text=review_text,
                sentiment=sentiment,
                confidence_score=confidence,
                created_at=created_at
            )
            
            db.add(review)
            created_count += 1
            
            print(f"✅ {customer_name}: {sentiment} (confiança: {confidence})")
        
        # Salvar no banco
        db.commit()
        
        print(f"\n🎉 {created_count} avaliações criadas com sucesso!")
        
        # Mostrar estatísticas
        total_reviews = db.query(Review).count()
        positive_count = db.query(Review).filter(Review.sentiment == 'positiva').count()
        negative_count = db.query(Review).filter(Review.sentiment == 'negativa').count()
        neutral_count = db.query(Review).filter(Review.sentiment == 'neutra').count()
        
        print(f"\n📊 ESTATÍSTICAS DO BANCO:")
        print(f"Total de avaliações: {total_reviews}")
        print(f"Positivas: {positive_count}")
        print(f"Negativas: {negative_count}")
        print(f"Neutras: {neutral_count}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {e}")
        db.rollback()
    finally:
        db.close()

def clear_database():
    """Limpa todos os dados do banco."""
    print("🗑️ Limpando banco de dados...")
    
    db = SessionLocal()
    try:
        count = db.query(Review).count()
        if count == 0:
            print("ℹ️ Banco já está vazio.")
            return
        
        response = input(f"⚠️ Isso irá deletar {count} avaliações. Confirma? (s/n): ")
        if response.lower() == 's':
            db.query(Review).delete()
            db.commit()
            print("✅ Banco de dados limpo com sucesso!")
        else:
            print("❌ Operação cancelada.")
    except Exception as e:
        print(f"❌ Erro ao limpar banco: {e}")
        db.rollback()
    finally:
        db.close()

def show_database_stats():
    """Mostra estatísticas do banco de dados."""
    print("📊 Estatísticas do banco de dados:")
    
    db = SessionLocal()
    try:
        total = db.query(Review).count()
        if total == 0:
            print("ℹ️ Banco de dados vazio.")
            return
        
        positive = db.query(Review).filter(Review.sentiment == 'positiva').count()
        negative = db.query(Review).filter(Review.sentiment == 'negativa').count()
        neutral = db.query(Review).filter(Review.sentiment == 'neutra').count()
        
        print(f"Total de avaliações: {total}")
        print(f"Positivas: {positive} ({positive/total*100:.1f}%)")
        print(f"Negativas: {negative} ({negative/total*100:.1f}%)")
        print(f"Neutras: {neutral} ({neutral/total*100:.1f}%)")
        
        # Mostrar algumas avaliações recentes
        recent_reviews = db.query(Review).order_by(Review.created_at.desc()).limit(5).all()
        
        print(f"\n📝 Últimas 5 avaliações:")
        for review in recent_reviews:
            print(f"  {review.id}: {review.customer_name} - {review.sentiment}")
            
    except Exception as e:
        print(f"❌ Erro ao consultar banco: {e}")
    finally:
        db.close()

def main():
    """Função principal."""
    print("🗄️ GERADOR DE DADOS DE EXEMPLO - BANCO DE DADOS")
    print("=" * 60)
    
    while True:
        print("\nOpções disponíveis:")
        print("1. Criar dados de exemplo")
        print("2. Mostrar estatísticas do banco")
        print("3. Limpar banco de dados")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção (1-4): ").strip()
        
        if choice == '1':
            create_sample_data()
        elif choice == '2':
            show_database_stats()
        elif choice == '3':
            clear_database()
        elif choice == '4':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

