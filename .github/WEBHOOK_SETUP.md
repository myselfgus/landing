# Configuração do Sistema de Sincronização Incremental

Este sistema implementa sincronização automática e **incremental** entre o repositório `myselfgus/docs` e `myselfgus/voither_landing`. O agente atualiza apenas o que mudou, preservando todo o conhecimento acumulado.

## 🔄 Como Funciona o Sistema Incremental

O sistema **nunca substitui** conteúdo existente. Em vez disso:
- ✅ **Adiciona** novos documentos
- ✅ **Atualiza** documentos modificados
- ✅ **Preserva** todo o histórico de sincronização 
- ✅ **Enriquece** continuamente o background knowledge
- ✅ **Gera** visualizações dinâmicas de conceitos

## 🌳 Funcionalidades Visuais Geradas

O sistema gera automaticamente:
- **Árvores de Conceitos** (`/background/ontologies/concept_tree.html`)
- **Organogramas Hierárquicos** (`/background/ontologies/orgchart.html`)
- **Grafos de Conhecimento** (`/background/graphs/knowledge_graph.json`)
- **Representações SVG** (`/background/ontologies/concept_tree.svg`)

## 1. Configuração no Repositório Docs

Crie o arquivo `.github/workflows/trigger-landing-sync.yml` no repositório `myselfgus/docs`:

```yaml
name: Trigger Landing Page Sync

on:
  push:
    branches: [ main ]
  pull_request:
    types: [ closed ]
    branches: [ main ]

jobs:
  trigger-sync:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' || (github.event.pull_request.merged == true)
    
    steps:
      - name: Trigger voither_landing sync
        uses: peter-evans/repository-dispatch@v2
        with:
          token: ${{ secrets.REPO_DISPATCH_TOKEN }}
          repository: myselfgus/voither_landing
          event-type: docs-updated
          client-payload: |
            {
              "docs_repo": "${{ github.repository }}",
              "commit_sha": "${{ github.sha }}",
              "ref": "${{ github.ref }}",
              "pusher": "${{ github.actor }}"
            }
```

## 2. Configuração de Secrets

No repositório docs (`myselfgus/docs`), adicione o secret:

- **REPO_DISPATCH_TOKEN**: Personal Access Token com permissões de `repo` e `workflow`

### Como criar o token:
1. Vá para GitHub → Settings → Developer settings → Personal access tokens
2. Clique em "Generate new token (classic)"
3. Selecione os scopes: `repo`, `workflow`
4. Copie o token e adicione como secret no repositório docs

## 3. Teste Manual

Você pode testar o workflow manualmente executando:

```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/myselfgus/voither_landing/dispatches \
  -d '{"event_type":"docs-updated","client_payload":{"docs_repo":"myselfgus/docs"}}'
```

## 4. Monitoramento

- Verifique o status dos workflows em Actions tab
- Logs detalhados estão disponíveis em cada execução
- Metadados de sincronização são salvos em `background/metadata.json`

## 5. Estrutura Esperada no Repositório Docs

```
docs/
├── README.md
├── concepts/
│   ├── voither-overview.md
│   ├── brre-engine.md
│   └── technologies.md
├── frameworks/
│   ├── compliance.md
│   └── architecture.md
├── processes/
│   ├── workflows.md
│   └── automation.md
└── config/
    ├── products.yml
    └── standards.yml
```

A estrutura é flexível - qualquer arquivo `.md`, `.yml`, `.yaml`, ou `.txt` será processado e organizado nos 4 eixos invariantes do sistema de background.

## 6. Benefícios do Sistema Incremental

### 📈 Crescimento Contínuo
- Cada sincronização **enriquece** o conhecimento existente
- Histórico completo de mudanças preservado
- Metadados evolutivos com estatísticas de crescimento

### 🎯 Inteligência Contextual  
- Detecção automática de conceitos novos vs. existentes
- Construção incremental de grafos de conhecimento
- Atualização inteligente de embeddings semânticos

### 🖼️ Visualizações Automáticas
- **Concept Trees**: Hierarquias navegáveis de todos os conceitos
- **Organization Charts**: Estrutura visual do ecossistema Voither
- **Knowledge Graphs**: Relações entre entidades e conceitos
- **Interactive HTML**: Visualizações prontas para integração

### ⚡ Performance Otimizada
- Processa apenas arquivos modificados
- Detecção inteligente de mudanças via hash
- Reutilização de processamentos anteriores

## 7. Próximos Passos Recomendados

1. **Crie o repositório docs** se ainda não existir
2. **Configure o trigger workflow** usando as instruções acima
3. **Adicione o token** `REPO_DISPATCH_TOKEN` nos secrets
4. **Teste com conteúdo real** - o sistema se adaptará automaticamente
5. **Explore as visualizações** geradas em `/background/ontologies/`

## 8. Integração com Landing Page

As visualizações geradas podem ser facilmente integradas:

```html
<!-- Concept Tree -->
<iframe src="/background/ontologies/concept_tree.html" 
        width="100%" height="500px"></iframe>

<!-- Organization Chart -->
<iframe src="/background/ontologies/orgchart.html" 
        width="100%" height="400px"></iframe>
```

O sistema mantém **fidedignidade conceitual** constante enquanto evolui organicamente com sua documentação.