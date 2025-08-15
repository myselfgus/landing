# Webhook Configuration for Docs Repository

Para configurar a sincronização automática entre o repositório `myselfgus/docs` e `myselfgus/voither_landing`, você precisa adicionar este workflow no repositório docs:

## 1. Arquivo `.github/workflows/trigger-landing-sync.yml` no repositório docs:

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