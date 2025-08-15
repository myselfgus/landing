# GitHub Actions: GCS Mirror & Drive Backup Setup

Este documento descreve como configurar o workflow `gcs-mirror-drive-backup.yml` que automatiza o backup e espelhamento do repositório.

## Visão Geral

O workflow executa duas operações principais:

1. **GCS Mirror**: Sincroniza o código para Google Cloud Storage
   - Cópia "latest" para uso operacional
   - Snapshots versionados (.tar.gz) para histórico imutável

2. **Drive Backup**: Envia snapshots para Google Drive
   - Backup visual e de fácil acesso
   - Armazenamento em Shared Drive

## Configuração Necessária

### 1. Google Cloud Platform (GCP)

#### Secrets Necessários:
- `GCP_WIF_PROVIDER`: Workload Identity Federation Provider
- `GCP_SA_EMAIL`: Email da Service Account

#### Setup:
1. Criar um bucket no GCS: `voither-code-mirror`
2. Configurar Workload Identity Federation
3. Criar Service Account com permissões:
   - `Storage Admin` ou `Storage Object Admin` para o bucket
4. Configurar o provider WIF para autenticar GitHub Actions

### 2. Google Drive (Opcional)

#### Secret Necessário:
- `RCLONE_CONF`: Configuração do rclone em base64

#### Setup:
1. Instalar rclone localmente
2. Configurar remote para Google Drive:
   ```bash
   rclone config
   ```
3. Codificar configuração em base64:
   ```bash
   cat ~/.config/rclone/rclone.conf | base64 -w 0
   ```
4. Adicionar como secret `RCLONE_CONF`

### 3. Variáveis de Ambiente

No arquivo workflow:
- `GCS_BUCKET`: `voither-code-mirror`
- `DRIVE_REMOTE`: `VAULT` (nome do remote no rclone)
- `DRIVE_PATH`: `artefatos/versions`

## Triggers

- **Push para main**: Execução automática
- **Manual**: Via workflow_dispatch na UI do GitHub

## Estrutura de Armazenamento

### Google Cloud Storage
```
gs://voither-code-mirror/
├── landing/
│   ├── latest/           # Código mais recente
│   │   ├── index.html
│   │   ├── package.json
│   │   └── ...
│   └── versions/         # Snapshots versionados
│       ├── landing-2025-01-20T123456Z_abc1234.tar.gz
│       └── landing-2025-01-19T123456Z_def5678.tar.gz
```

### Google Drive
```
VAULT/
├── landing/
│   └── artefatos/
│       └── versions/
│           ├── landing-2025-01-20T123456Z_abc1234.tar.gz
│           └── landing-2025-01-19T123456Z_def5678.tar.gz
```

## Formato dos Snapshots

Nomenclatura: `{repository}-{timestamp}_{short-sha}.tar.gz`

Exemplo: `landing-2025-01-20T123456Z_abc1234.tar.gz`

- **repository**: Nome do repositório
- **timestamp**: ISO 8601 format (UTC)
- **short-sha**: 7 caracteres do commit SHA

## Exclusões no Snapshot

O tar exclui automaticamente:
- Arquivos listados em `.gitignore`
- `.git/` (histórico git)
- `node_modules/` (dependências)
- `dist/` (build artifacts)
- `*.log` (arquivos de log)

## Monitoramento

### Logs do Workflow
- Verificação de acesso ao GCS
- Progresso do upload
- Validação dos snapshots
- Resumo das operações

### Outputs
- Summary com links úteis
- Detalhes do snapshot criado
- Status de cada operação

## Troubleshooting

### Problemas Comuns

1. **Erro de autenticação GCP**
   - Verificar se `GCP_WIF_PROVIDER` e `GCP_SA_EMAIL` estão corretos
   - Confirmar permissões da Service Account

2. **Bucket não encontrado**
   - Verificar se o bucket `voither-code-mirror` existe
   - Confirmar permissões de acesso

3. **Falha no rclone**
   - Verificar se `RCLONE_CONF` está em base64 válido
   - Confirmar se o remote `VAULT` está configurado

4. **Snapshot muito grande**
   - Verificar exclusões no `.gitignore`
   - Considerar adicionar mais exclusões no comando tar

### Debug

Para executar manualmente:
1. Usar `workflow_dispatch` na UI do GitHub
2. Verificar logs detalhados de cada step
3. Usar `verbose` nos comandos rclone para mais informações

## Segurança

- Secrets são mascarados nos logs
- Arquivos temporários são limpos automaticamente
- Service Account com princípio de menor privilégio
- Configuração rclone removida após uso