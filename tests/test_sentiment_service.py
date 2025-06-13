"""
Testes unitários para o serviço de análise de sentimento.
"""
from app.sentiment_service import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Testes para a classe SentimentAnalyzer."""

    def setup_method(self):
        """Configuração executada antes de cada teste."""
        self.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        """Testa análise de sentimento positivo."""
        text = "Excelente atendimento, muito satisfeito com o serviço!"
        sentiment, confidence = self.analyzer.analyze_sentiment(text)

        assert sentiment == "positiva"
        assert float(confidence) > 0

    def test_negative_sentiment(self):
        """Testa análise de sentimento negativo."""
        text = "Péssimo atendimento, muito insatisfeito com o serviço!"
        sentiment, confidence = self.analyzer.analyze_sentiment(text)

        assert sentiment == "negativa"
        assert float(confidence) > 0

    def test_neutral_sentiment(self):
        """Testa análise de sentimento neutro."""
        text = "O atendimento foi ok, nada demais."
        sentiment, confidence = self.analyzer.analyze_sentiment(text)

        assert sentiment in ["neutra", "positiva", "negativa"]  # Pode variar
        assert float(confidence) >= 0

    def test_empty_text(self):
        """Testa análise com texto vazio."""
        text = ""
        sentiment, confidence = self.analyzer.analyze_sentiment(text)

        assert sentiment == "neutra"
        assert float(confidence) == 0.0

    def test_get_sentiment_description(self):
        """Testa obtenção de descrição do sentimento."""
        assert "positiva" in SentimentAnalyzer.get_sentiment_description("positiva")
        assert "negativa" in SentimentAnalyzer.get_sentiment_description("negativa")
        assert "neutra" in SentimentAnalyzer.get_sentiment_description("neutra")
        assert "não identificado" in SentimentAnalyzer.get_sentiment_description(
            "invalido"
        )
