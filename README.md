# Sentiment Analysis API

API REST em Python para classificação automática de avaliações de clientes em Positiva, Negativa ou Neutra usando análise de sentimento com LLM (Groq) e fallback híbrido.

## 📋 Descrição

Esta API foi desenvolvida para analisar automaticamente o sentimento de avaliações de clientes sobre serviços/produtos/suporte de uma empresa. Utiliza uma abordagem inteligente com LLM (Large Language Model) via Groq como método principal e fallback híbrido combinando análise lexical em português com TextBlob para textos em inglês.

## 🚀 Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **Groq** - API para LLM (Large Language Model)
- **TextBlob** - Biblioteca para processamento de linguagem natural (fallback)
- **Pydantic** - Validação de dados
- **Pytest** - Framework de testes
- **Uvicorn** - Servidor ASGI

## 📁 Estrutura do Projeto

```
sentiment_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação principal FastAPI
│   ├── config.py            # Configurações da aplicação
│   ├── models.py            # Modelos de dados SQLAlchemy
│   ├── schemas.py           # Schemas Pydantic
│   ├── routes.py            # Rotas da API
│   └── sentiment_service.py # Serviço de análise de sentimento com LLM
├── tests/
│   ├── __init__.py
│   ├── test_sentiment_service.py # Testes do serviço de sentimento
│   └── test_routes.py       # Testes das rotas da API
├── requirements.txt         # Dependências do projeto
├── .env                     # Variáveis de ambiente
└── README.md               # Este arquivo
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- PostgreSQL 14+
- pip
- Conta no Groq (para obter API key)

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd sentiment_api
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados PostgreSQL

#### Linux/macOS:

```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Iniciar o serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Criar banco de dados
sudo -u postgres psql -c "CREATE DATABASE sentiment_db;"
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

#### Windows:

1. **Baixar e instalar PostgreSQL:**
   - Acesse: https://www.postgresql.org/download/windows/
   - Baixe o instalador oficial do PostgreSQL
   - Execute o instalador como administrador
   - Durante a instalação:
     - Defina uma senha para o usuário `postgres` (recomendado: `postgres`)
     - Mantenha a porta padrão `5432`
     - Instale o pgAdmin (interface gráfica) se desejar

2. **Configurar o banco de dados:**
   
   **Opção A - Via pgAdmin (Interface Gráfica):**
   - Abra o pgAdmin
   - Conecte-se ao servidor local
   - Clique com botão direito em "Databases" → "Create" → "Database"
   - Nome: `sentiment_db`
   - Clique em "Save"

   **Opção B - Via linha de comando:**
   ```cmd
   # Abrir Command Prompt como administrador
   # Navegar até a pasta de instalação do PostgreSQL (geralmente):
   cd "C:\Program Files\PostgreSQL\14\bin"
   
   # Conectar ao PostgreSQL
   psql -U postgres
   
   # Criar o banco de dados
   CREATE DATABASE sentiment_db;
   
   # Sair
   \q
   ```

3. **Configurar variáveis de ambiente (opcional):**
   - Adicionar `C:\Program Files\PostgreSQL\14\bin` ao PATH do sistema
   - Isso permite usar `psql` de qualquer diretório

4. **Testar a conexão:**
   ```cmd
   psql -U postgres -d sentiment_db -h localhost -p 5432
   ```

### 4. Configure a API do Groq

1. **Obter API Key do Groq:**
   - Acesse: https://console.groq.com/
   - Crie uma conta gratuita
   - Vá para "API Keys" no painel
   - Clique em "Create API Key"
   - Copie a chave gerada (formato: `gsk_...`)

2. **Configurar a chave na aplicação:**
   - Edite o arquivo `.env` e substitua `gsk_YOUR_GROQ_API_KEY` pela sua chave real

### 5. Configure as variáveis de ambiente

Edite o arquivo `.env`:

```env
# Configurações do banco de dados
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sentiment_db

# Configurações da aplicação
DEBUG=True

# Configurações do Groq LLM
GROQ_API_KEY=gsk_sua_chave_real_aqui
GROQ_MODEL=llama-3.3-70b-versatile

# Configurações de análise de sentimento
USE_LLM_ANALYSIS=True
LLM_MAX_TOKENS=1024
LLM_TEMPERATURE=0.1
```

### 6. Baixe os dados necessários para análise de sentimento (fallback)

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
python -m textblob.download_corpora
```

## 🏃‍♂️ Executando a Aplicação

### Desenvolvimento

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Produção

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### Swagger UI
Acesse: `http://localhost:8000/docs`

### ReDoc
Acesse: `http://localhost:8000/redoc`

## 🛠 Endpoints da API

### 1. POST /api/v1/reviews
Classifica uma avaliação de cliente usando análise de sentimento.

**Request Body:**
```json
{
  "customer_name": "João Silva",
  "review_text": "Excelente atendimento, muito satisfeito com o serviço!"
}
```

**Response:**
```json
{
  "id": 1,
  "sentiment": "positiva",
  "confidence_score": "0.50",
  "message": "Análise de sentimento realizada com sucesso"
}
```

### 2. GET /api/v1/reviews
Retorna uma lista de todas as avaliações analisadas.

**Query Parameters:**
- `skip` (opcional): Número de registros a pular (padrão: 0)
- `limit` (opcional): Número máximo de registros (padrão: 100)

**Response:**
```json
[
  {
    "id": 1,
    "customer_name": "João Silva",
    "review_text": "Excelente atendimento, muito satisfeito com o serviço!",
    "sentiment": "positiva",
    "confidence_score": "0.50",
    "created_at": "2024-09-17T10:30:00"
  }
]
```

### 3. GET /api/v1/reviews/{id}
Busca uma avaliação específica pelo ID.

**Response:**
```json
{
  "id": 1,
  "customer_name": "João Silva",
  "review_text": "Excelente atendimento, muito satisfeito com o serviço!",
  "sentiment": "positiva",
  "confidence_score": "0.50",
  "created_at": "2024-09-17T10:30:00"
}
```

### 4. GET /api/v1/reviews/report
Retorna um relatório das avaliações em um período específico.

**Query Parameters:**
- `start_date`: Data inicial no formato YYYY-MM-DD
- `end_date`: Data final no formato YYYY-MM-DD

**Exemplo:**
```
GET /api/v1/reviews/report?start_date=2024-09-01&end_date=2024-09-17
```

**Response:**
```json
{
  "start_date": "2024-09-01",
  "end_date": "2024-09-17",
  "total_reviews": 10,
  "positive_count": 4,
  "negative_count": 3,
  "neutral_count": 3
}
```

## 🧪 Executando os Testes

### Testes unitários

```bash
python -m pytest tests/ -v
```

### Testes específicos

```bash
# Testar apenas o serviço de sentimento
python -m pytest tests/test_sentiment_service.py -v

# Testar apenas as rotas
python -m pytest tests/test_routes.py -v
```

## 🔍 Análise de Sentimento

A API utiliza uma abordagem inteligente em camadas para análise de sentimento:

### 1. **Análise com LLM (Groq) - Método Principal**
- Utiliza modelos de linguagem avançados via API do Groq
- Modelo padrão: `llama-3.3-70b-versatile`
- Análise contextual profunda e precisa
- Suporte nativo para português e outros idiomas
- Retorna classificação e nível de confiança

### 2. **Fallback Híbrido - Método Secundário**
- **Análise Lexical em Português**: Utiliza dicionários de palavras positivas e negativas em português para classificação inicial
- **TextBlob como Backup**: Para textos em inglês ou quando a análise lexical não é conclusiva

### 3. **Classificação**:
- **Positiva**: Sentimentos favoráveis, satisfação, elogios
- **Negativa**: Sentimentos desfavoráveis, insatisfação, reclamações
- **Neutra**: Sentimentos neutros, mistos ou informativos

### 4. **Configurações Disponíveis**:
- `USE_LLM_ANALYSIS`: Habilitar/desabilitar análise com LLM
- `GROQ_MODEL`: Modelo do Groq a ser utilizado
- `LLM_TEMPERATURE`: Controle de criatividade (0.0-1.0)
- `LLM_MAX_TOKENS`: Limite de tokens na resposta

## 📊 Exemplos de Uso

### Criar uma avaliação

```bash
curl -X POST "http://localhost:8000/api/v1/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Maria Santos",
    "review_text": "Péssimo atendimento, muito insatisfeito!"
  }'
```

### Buscar todas as avaliações

```bash
curl -X GET "http://localhost:8000/api/v1/reviews"
```

### Gerar relatório

```bash
curl -X GET "http://localhost:8000/api/v1/reviews/report?start_date=2024-09-01&end_date=2024-09-30"
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

- `DATABASE_URL`: URL de conexão com o PostgreSQL
- `DEBUG`: Modo de debug (True/False)
- `GROQ_API_KEY`: Chave da API do Groq para LLM
- `GROQ_MODEL`: Modelo do Groq a ser utilizado
- `USE_LLM_ANALYSIS`: Habilitar análise com LLM (True/False)
- `LLM_MAX_TOKENS`: Limite de tokens na resposta do LLM
- `LLM_TEMPERATURE`: Controle de criatividade do LLM (0.0-1.0)
- `API_TITLE`: Título da API
- `API_DESCRIPTION`: Descrição da API
- `API_VERSION`: Versão da API

### Personalização da Análise de Sentimento

Para adicionar novas palavras aos dicionários de sentimento, edite o arquivo `app/sentiment_service.py`:

```python
POSITIVE_WORDS = {
    'excelente', 'ótimo', 'bom', 'satisfeito', 'feliz',
    # Adicione suas palavras aqui
}

NEGATIVE_WORDS = {
    'péssimo', 'ruim', 'insatisfeito', 'decepcionado',
    # Adicione suas palavras aqui
}
```

## 🚀 Deploy

### Usando Docker (Recomendado)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy em Produção

1. Configure um servidor PostgreSQL dedicado
2. Use um servidor web como Nginx como proxy reverso
3. Configure variáveis de ambiente de produção
4. Use um gerenciador de processos como Supervisor ou systemd

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autor

Desenvolvido como parte do teste técnico para Desenvolvedor Back-End Python.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através do email: gente@weon.com.br



## 🧪 Dados de Teste

O projeto inclui scripts para gerar e analisar dados de teste:

### 1. Geração de Dados via API

```bash
# Executar o gerador de dados de teste
python generate_test_data.py
```

Este script:
- Testa a conexão com a API
- Cria 22 avaliações de exemplo com diferentes sentimentos
- Inclui textos em português e inglês
- Avalia a acurácia das predições
- Gera relatório em JSON

### 2. População Direta do Banco

```bash
# Popular banco com dados de exemplo
python populate_database.py
```

Este script oferece opções para:
- Criar dados de exemplo diretamente no banco
- Mostrar estatísticas do banco de dados
- Limpar todos os dados

### 3. Análise dos Resultados

```bash
# Instalar dependências para análise (se necessário)
pip install matplotlib seaborn

# Analisar resultados dos testes
python analyze_test_results.py
```

Este script:
- Carrega resultados dos testes
- Gera gráficos de performance
- Cria matriz de confusão
- Analisa distribuição de confiança
- Gera relatório detalhado

### Tipos de Dados de Teste

Os dados incluem:

**Avaliações Positivas:**
- "Excelente atendimento! Superou minhas expectativas!"
- "Fantástico! O produto funcionou perfeitamente."

**Avaliações Negativas:**
- "Péssimo atendimento! Muito insatisfeito."
- "Terrível experiência. Não recomendo!"

**Avaliações Neutras:**
- "O atendimento foi ok, nada excepcional."
- "Serviço mediano, dentro do esperado."

**Avaliações em Inglês:**
- "Amazing service! Highly recommended!"
- "Terrible experience, very disappointed."

**Avaliações Mistas/Complexas:**
- "O produto é bom, mas o atendimento deixou a desejar."
- "Gostei em geral, mas houve alguns problemas."

### Métricas de Avaliação

Os scripts calculam:
- **Acurácia geral**: Percentual de predições corretas
- **Acurácia por sentimento**: Performance específica para cada classe
- **Matriz de confusão**: Visualização dos erros de classificação
- **Análise de confiança**: Distribuição dos scores de confiança
- **Comparação LLM vs Fallback**: Performance de cada método

