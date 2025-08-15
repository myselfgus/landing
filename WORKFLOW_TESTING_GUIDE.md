# 🧪 Guia de Teste dos Workflows

## Como Verificar se os Workflows Estão Funcionando

### 1. 🔧 **Workflow de Validação** (Novo)

Adicionamos um workflow específico para testar a configuração:

```bash
# Para executar via GitHub Actions UI:
# 1. Vá para Actions > Workflow Validation Test
# 2. Clique em "Run workflow"
# 3. Escolha o tipo de teste: syntax, dependencies, ou scripts
```

### 2. 🤖 **AI Orchestrator** - Como Testar

**Status**: ✅ Pronto para usar

```bash
# Método 1: Via comentário em issue
# 1. Crie ou abra uma issue
# 2. Comente: @ai-orchestrator análise completa
# 3. O workflow será executado automaticamente

# Método 2: Execução manual
# 1. Vá para Actions > AI Site Orchestrator  
# 2. Clique em "Run workflow"
# 3. Configure os parâmetros desejados
```

**Recursos testáveis**:
- ✅ Análise de performance
- ✅ Otimização de conteúdo  
- ✅ Geração de visuais
- ✅ Análise SEO
- ✅ Insights de código

### 3. 👥 **AI Agents Collaborative** - Como Testar

**Status**: ✅ Pronto para usar

```bash
# Método 1: Via comentário em issue
# 1. Crie ou abra uma issue
# 2. Comente: @ai-agents full-pipeline
# 3. O sistema executará: Planner → Executor → Auditor

# Método 2: Execução manual
# 1. Vá para Actions > AI Agents Collaborative System
# 2. Clique em "Run workflow"
# 3. Escolha o modo de colaboração
```

**Pipeline testável**:
- ✅ Agente Planner (Claude 3.5 Sonnet)
- ✅ Agente Executor (GPT-4 Turbo)
- ✅ Agente Auditor (Llama 3.1 405B)
- ✅ Sistema de aprovação
- ✅ Deploy automático

### 4. 🗄️ **GCS Mirror & Drive Backup** - Como Configurar

**Status**: ⚠️ Requer configuração GCP

```bash
# Para que funcione, configure os secrets:
# Settings > Secrets and variables > Actions

# Secrets necessários:
GCP_WIF_PROVIDER=projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider
GCP_SA_EMAIL=github-actions@your-project.iam.gserviceaccount.com

# Opcional (para Google Drive):
RCLONE_CONF=<base64-encoded-rclone-config>
```

### 5. 📚 **Docs Sync** - Funcionando

**Status**: ✅ Funcionando

```bash
# Testa automaticamente quando:
# 1. Há mudanças no repo myselfgus/docs
# 2. Execução manual via Actions UI
```

## 🔍 Comandos de Diagnóstico

Para verificar o status local:

```bash
# 1. Validar sintaxe YAML
python3 -c "
import yaml
workflows = ['.github/workflows/gcs-mirror-drive-backup.yml', '.github/workflows/ai-orchestrator.yml', '.github/workflows/ai-agents-collaborative.yml']
for f in workflows:
    yaml.safe_load(open(f))
    print(f'{f}: ✅ OK')
"

# 2. Verificar scripts Python
find .github/scripts -name "*.py" -executable | wc -l

# 3. Testar build do projeto
npm install && npm run build

# 4. Verificar dependências Python
pip install pyyaml requests beautifulsoup4 nltk scikit-learn numpy pandas
```

## 📊 Status de Execução

### Última Verificação

| Workflow | Status | Execuções | Último Teste |
|----------|--------|-----------|--------------|
| GCS Mirror | ❌ Falhando | 8 falhas | Secrets em falta |
| AI Orchestrator | ⏳ Aguardando | 0 runs | Pronto para teste |
| AI Agents | ⏳ Aguardando | 0 runs | Pronto para teste |
| Docs Sync | ✅ OK | Funcionando | Automático |
| Validação | 🆕 Novo | 0 runs | Disponível |

## 🚀 Próximos Testes Recomendados

1. **Teste Imediato**: Execute o workflow de validação
2. **Teste AI**: Comente `@ai-orchestrator` numa issue
3. **Teste Colaborativo**: Comente `@ai-agents` numa issue  
4. **Configure GCP**: Para ativar backup GCS/Drive

## ⚡ Execução Rápida

```bash
# Teste rápido de tudo local:
npm install && npm run build && python3 -c "import yaml; [yaml.safe_load(open(f)) for f in ['.github/workflows/gcs-mirror-drive-backup.yml','.github/workflows/ai-orchestrator.yml','.github/workflows/ai-agents-collaborative.yml']] and print('✅ All workflows valid!')"
```