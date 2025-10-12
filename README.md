# Jornada Finanças Pessoais

Este projeto implementa um pipeline de dados para processar e analisar informações financeiras pessoais, incluindo cotações históricas da B3 e controle de ativos.

## Estrutura do Projeto

```
Jornada_financas_pessoais/
├── data/                    # Diretório de dados
│   ├── delta/              # Tabelas Delta Lake
│   │   ├── bronze/         # Dados brutos
│   │   └── silver/         # Dados transformados
│   └── source/             # Arquivos fonte (COTAHIST, planilhas)
├── pipeline/               # Notebooks de processamento
├── modelo_dados/          # Modelagem do banco de dados
├── sql/                   # Scripts SQL
└── especificacao/         # Documentação técnica
```

## Pipeline de Dados

### Camada Bronze
- **Ingestão de Cotações (B3)**: 
  - Notebook: `ingestao_bronze_cotahist.ipynb`
  - Fonte: Arquivos COTAHIST da B3
  - Formato: Delta Lake
  - Escopo: Dados brutos das cotações históricas

### Camada Silver
- **Cotações Históricas**: 
  - Notebook: `carga_silver_cotacao_historica.ipynb`
  - Transformações: Tipagem adequada, conversão de valores
  - Formato: Delta Lake

## Tecnologias Utilizadas

- **Apache Spark**: Processamento de dados
- **Delta Lake**: Armazenamento e versionamento
- **Python**: Linguagem principal
- **DuckDB**: Banco de dados analítico

## Configuração do Ambiente

1. Criar ambiente virtual Python:
```bash
python -m venv .venv
```

2. Ativar ambiente:
```bash
# Windows
.venv\Scripts\activate
```

3. Instalar dependências:
```bash
pip install -r requirements.txt
```

## Estrutura dos Dados

### Cotações Históricas (Silver)
```sql
CREATE TABLE cotacao_historica (
  tipo_registro STRING,
  data_pregao DATE,
  codigo_bdi STRING,
  codigo_negociacao STRING,
  tipo_mercado STRING,
  nome_resumido_empresa STRING,
  especificacao_papel STRING,
  prazo_dias_mercado STRING,
  moeda_referencia STRING,
  preco_abertura_papel DECIMAL(11,2),
  preco_maximo_papel DECIMAL(11,2),
  preco_minimo_papel DECIMAL(11,2),
  preco_medio_papel DECIMAL(11,2),
  preco_ultimo_negocio DECIMAL(11,2),
  preco_melhor_oferta_compra DECIMAL(11,2),
  preco_melhor_oferta_venda DECIMAL(11,2),
  numero_negocios_efetuados INT,
  quantidade_total_titulos INT,
  volume_total_titulos DECIMAL(16,2),
  preco_exercicio_opcoes DECIMAL(11,2),
  indicador_correcao_precos STRING,
  data_vencimento_opcoes DATE,
  fator_cotacao_papel STRING,
  preco_exercicio_pontos DECIMAL(7,6),
  codigo_papel_sistema STRING,
  numero_distribuicao_papel STRING,
  data_insercao TIMESTAMP
)
```

## Contribuição

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Commit suas mudanças (`git commit -am 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/nome-da-feature`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença MIT.
