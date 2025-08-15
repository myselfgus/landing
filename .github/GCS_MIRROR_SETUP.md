# GitHub Actions: GCS Mirror & Drive Backup Setup

Este documento descreve como configurar o workflow `gcs-mirror-drive-backup.yml` que automatiza o backup e espelhamento do repositório para o Google Cloud Storage e Google Drive.

## Visão Geral

O workflow executa duas operações principais a cada `push` na branch `main`:

1.  **GCS Mirror**: Sincroniza o código-fonte para um bucket no Google Cloud Storage.
    -   **Cópia "latest"**: Uma cópia sempre atualizada para uso operacional por outras ferramentas e serviços.
    -   **Snapshots versionados**: Arquivos `.tar.gz` imutáveis, nomeados com timestamp e hash do commit, para um histórico seguro.

2.  **Drive Backup (Opcional)**: Envia os mesmos snapshots para um Shared Drive no Google Drive.
    -   Serve como um backup visual, de fácil acesso para humanos e integrado ao ecossistema Google.


## Configuração Necessária

Para que o workflow funcione, você precisa configurar os seguintes segredos no seu repositório GitHub em `Settings > Secrets and variables > Actions`.

### 1. Google Cloud Platform (GCP)

#### Secrets Necessários:

-   `GCP_WIF_PROVIDER`: O identificador completo do seu Workload Identity Federation Provider.
    -   **Formato**: `projects/YOUR_PROJECT_NUMBER/locations/global/workloadIdentityPools/YOUR_POOL_ID/providers/YOUR_PROVIDER_ID`
-   `GCP_SA_EMAIL`: O e-mail da Service Account do GCP que o GitHub usará para se autenticar.
    -   **Formato**: `your-service-account@your-project-id.iam.gserviceaccount.com`

#### Setup no GCP:

1.  **Criar um bucket no GCS**: Se ainda não existir, crie o bucket (ex: `voither-code-mirror`).
2.  **Configurar Workload Identity Federation**: Siga o guia do Google para permitir que o GitHub se autentique no GCP sem chaves.
3.  **Criar Service Account**: Crie uma Service Account e conceda a ela as permissões necessárias no bucket GCS (ex: `Storage Object Admin` - `roles/storage.objectAdmin`).
4.  **Vincular SA ao WIF**: Vincule a Service Account ao provedor WIF, permitindo que repositórios específicos do GitHub a personifiquem.

### 2. Google Drive (Opcional)

Esta etapa só é necessária se você quiser o backup no Google Drive.

#### Secret Necessário:

-   `RCLONE_CONF`: O conteúdo do seu arquivo de configuração do `rclone`, codificado em Base64.

#### Setup do Rclone:

1.  **Instale o rclone** na sua máquina local ou no Cloud Shell (`sudo apt-get install rclone`).
2.  **Configure um remote** para o Google Drive executando `rclone config`. Siga os passos, autentique-se com sua conta Google e dê um nome ao seu remote (ex: `VAULT`). Certifique-se de configurar o acesso a um Shared Drive (Team Drive) se for o caso.
3.  **Codifique a configuração** para Base64. Este comando lê o arquivo de configuração e o imprime no terminal, pronto para ser copiado.
    ```bash
    # No Linux / macOS / Cloud Shell
    base64 -w 0 ~/.config/rclone/rclone.conf
    ```
4.  **Adicione o secret**: Copie a longa string gerada e cole-a como o valor do segredo `RCLONE_CONF` no GitHub.

### 3. Variáveis de Ambiente

As seguintes variáveis são definidas no topo do arquivo de workflow e podem ser ajustadas se necessário:

-   `GCS_BUCKET`: `voither-code-mirror`
-   `DRIVE_REMOTE`: `VAULT` (deve corresponder ao nome do remote que você configurou no rclone)
-   `DRIVE_PATH`: `artefatos/versions` (a subpasta de destino dentro do seu Drive)

## Estrutura de Armazenamento Resultante

### Google Cloud Storage
```
gs://voither-code-mirror/
└── <repository-name>/
    ├── latest/           # Código mais recente, espelhado
    │   ├── index.html
    │   └── ...
    └── versions/         # Snapshots versionados e imutáveis
        └── <repo-name>-2025-01-20T123456Z_abc1234.tar.gz
```

### Google Drive
```
VAULT (Shared Drive)/
└── <repository-name>/
    └── artefatos/
        └── versions/
            └── <repo-name>-2025-01-20T123456Z_abc1234.tar.gz
```

## Troubleshooting

1.  **Erro de autenticação GCP**:
    -   Verifique se os segredos `GCP_WIF_PROVIDER` e `GCP_SA_EMAIL` estão corretos e não contêm espaços extras.
    -   Confirme se a Service Account tem as permissões `Storage Object Admin` no bucket.
    -   Verifique se a política do WIF permite o seu repositório (`repo:your-org/your-repo:ref:refs/heads/main`).

2.  **Falha no rclone**:
    -   Verifique se o segredo `RCLONE_CONF` foi copiado corretamente e é um Base64 válido.
    -   Confirme se o nome em `DRIVE_REMOTE` corresponde exatamente ao nome do remote no seu `rclone.conf`.

3.  **Workflow não é acionado**:
    -   Verifique se o arquivo está no caminho correto: `.github/workflows/gcs-mirror-drive-backup.yml`.
    -   Confirme se você está fazendo push para a branch `main`.
