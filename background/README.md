# Background Knowledge Base

Este diretório contém o conhecimento de base organizado e contextualizado da Voither, sincronizado automaticamente a partir do repositório de documentação.

## Estrutura dos 4 Eixos Invariantes

### 📚 Ontologias (`./ontologies/`)
Frameworks conceituais, taxonomias e estruturas de conhecimento que definem os conceitos fundamentais da Voither:
- Terminologias médicas e clínicas
- Arquiteturas de sistema (BRRE, E2E Pipeline, etc.)
- Compliance e regulamentações
- Definições de produtos e funcionalidades

### 🔍 Parsings (`./parsings/`)
Análise estruturada de conteúdo e processamento de dados:
- Análise de texto e documentação
- Estruturação de informações não-estruturadas
- Extração de entidades e relacionamentos
- Formatação padronizada de conteúdo

### 🧮 Vectors/Embeddings (`./vectors/`)
Representações semânticas e numéricas do conhecimento:
- Embeddings de texto para busca semântica
- Representações vetoriais de conceitos
- Índices de similaridade
- Modelos de linguagem contextual

### 🕸️ Graphs (`./graphs/`)
Relacionamentos e conexões do conhecimento:
- Grafos de conhecimento
- Mapas conceituais
- Relacionamentos entre entidades
- Redes de dependências

## Sincronização Automática

O conteúdo deste diretório é atualizado automaticamente sempre que há mudanças no repositório `myselfgus/docs` através do workflow GitHub Actions `docs-sync.yml`.

### Processo de Sincronização:
1. **Trigger**: Mudanças no repositório docs
2. **Processamento**: Análise e estruturação do conteúdo
3. **Organização**: Distribuição pelos 4 eixos invariantes
4. **Vetorização**: Geração de embeddings e representações semânticas
5. **Grafos**: Criação/atualização de relacionamentos
6. **Commit**: Atualização automática do repositório voither_landing

## Uso no Contexto da Landing Page

Este conhecimento de base serve para:
- Contextualização de conteúdo dinâmico
- Suporte a funcionalidades de busca
- Enriquecimento semântico de interfaces
- Base para chatbots e assistentes IA
- Manutenção de fidedignidade conceitual
- Consistência terminológica

## Metadados

Veja `metadata.json` para informações sobre a última sincronização e estatísticas do conteúdo.