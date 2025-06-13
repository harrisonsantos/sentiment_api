"""
Serviço de análise de sentimento usando LLM (Groq).
"""
import logging
import time
from textblob import TextBlob
from typing import Tuple, Optional
import re
from groq import Groq, RateLimitError
from app.config import settings

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Classe para análise de sentimento de textos usando LLM (Groq)."""
    
    def __init__(self):
        """Inicializa o analisador de sentimento."""
        self.groq_client = None
        self.use_llm = settings.USE_LLM_ANALYSIS

        if self.use_llm and settings.GROQ_API_KEY != "gsk_YOUR_GROQ_API_KEY":
            try:
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info(f"Groq client initialized with model: {settings.GROQ_MODEL}")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.use_llm = False
        else:
            logger.info("LLM disabled or API key not configured")
            self.use_llm = False

    def _analyze_with_llm(self, text: str) -> Optional[Tuple[str, str]]:
        """
        Analisa sentimento usando LLM (Groq).
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            Optional[Tuple[str, str]]: (sentimento, confiança) ou None se falhar
        """
        if not self.groq_client:
            return None
        
        prompt = f"""Analise o sentimento da seguinte avaliação de cliente e classifique como:
- "positiva" para sentimentos favoráveis, satisfação, elogios
- "negativa" para sentimentos desfavoráveis, insatisfação, reclamações  
- "neutra" para sentimentos neutros, mistos ou informativos

Avaliação: "{text}"

Responda APENAS com o formato JSON:
{{"sentiment": "positiva|negativa|neutra", "confidence": "0.XX"}}

Onde confidence é um valor entre 0.00 e 1.00 indicando sua confiança na classificação."""

        try:
            response = self.groq_client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é um especialista em análise de sentimento. Responda sempre no formato JSON solicitado."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.LLM_MAX_TOKENS,
                temperature=settings.LLM_TEMPERATURE,
                top_p=0.9
            )
            
            response_text = response.choices[0].message.content.strip()
            logger.debug(f"LLM response: {response_text}")
            
            # Extrair JSON da resposta
            import json
            try:
                # Tentar extrair JSON da resposta
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                    
                    sentiment = result.get('sentiment', '').lower()
                    confidence = str(result.get('confidence', '0.50'))
                    
                    # Validar sentimento
                    if sentiment in ['positiva', 'negativa', 'neutra']:
                        logger.debug(f"LLM analysis successful: {sentiment}, {confidence}")
                        return sentiment, confidence
                    else:
                        logger.warning(f"Invalid sentiment from LLM: {sentiment}")
                        return None
                else:
                    logger.warning("No JSON found in LLM response")
                    return None
                    
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse LLM JSON response: {e}")
                return None
                
        except RateLimitError as e:
            logger.warning(f"Groq rate limit exceeded: {e}")
            time.sleep(1)  # Aguardar antes de tentar novamente
            return None
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return None
    
    def analyze_sentiment(self, text: str) -> Tuple[str, str]:
        """
        Analisa o sentimento de um texto usando LLM.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            Tuple[str, str]: Tupla contendo (sentimento, score_confiança)
                sentimento: 'positiva', 'negativa' ou 'neutra'
                score_confiança: valor de confiança da análise
        """
        if not text or text.strip() == "":
            return "neutra", "0.00"
        
        # Tentar análise com LLM primeiro
        if self.use_llm:
            llm_result = self._analyze_with_llm(text)
            if llm_result:
                logger.debug("Used LLM analysis")
                return llm_result
        return "neutra", "0.00"
    
    @staticmethod
    def get_sentiment_description(sentiment: str) -> str:
        """
        Retorna uma descrição do sentimento.
        
        Args:
            sentiment (str): Sentimento classificado
            
        Returns:
            str: Descrição do sentimento
        """
        descriptions = {
            "positiva": "Avaliação positiva - cliente satisfeito",
            "negativa": "Avaliação negativa - cliente insatisfeito", 
            "neutra": "Avaliação neutra - sentimento neutro ou misto"
        }
        return descriptions.get(sentiment, "Sentimento não identificado")
