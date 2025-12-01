# Correção do Problema de Autenticação do WAHA

## 📋 Resumo do Problema

O WAHA não estava funcionando corretamente devido a **inconsistências na configuração de autenticação** no arquivo `docker-compose.yml`. As senhas definidas tanto no Docker quanto no `.env` não estavam sendo respeitadas.

## 🔍 Problemas Identificados

### 1. Conflito entre Valores Hardcoded e Secrets

**Antes:**
```yaml
environment:
  - WAHA_API_KEY=GEZyp7uOrKBm4T7N30P4ekCgMPF03lsL0Yam2oO5TAo=
  - WAHA_DASHBOARD_PASSWORD=GEZyp7uOrKBm4T7N30P4ekCgMPF03lsL0Yam2oO5TAo=
```

O problema aqui era que as credenciais estavam **hardcoded** diretamente no arquivo Docker Compose, ignorando completamente os secrets configurados.

### 2. Falta do Secret waha_dashboard_password

O arquivo `docker-compose.yml` referenciava secrets que não existiam:
- ✅ `waha_api_key` - existia
- ❌ `waha_dashboard_password` - **NÃO existia**
- ✅ `waha_swagger_password` - existia

### 3. Inconsistência no Uso de Variáveis

Algumas credenciais usavam `_FILE` (para ler de secrets) e outras não, causando confusão sobre qual método estava sendo usado.

## ✅ Soluções Implementadas

### 1. Padronização do Uso de Secrets

**Depois:**
```yaml
environment:
  - WAHA_API_KEY_FILE=/run/secrets/waha_api_key
  - WAHA_DASHBOARD_PASSWORD_FILE=/run/secrets/waha_dashboard_password
  - WHATSAPP_SWAGGER_PASSWORD_FILE=/run/secrets/waha_swagger_password
```

Agora **todas** as credenciais sensíveis usam o padrão `_FILE` para ler valores dos secrets do Docker.

### 2. Adição do Secret Faltante

```yaml
secrets:
  - waha_api_key
  - waha_dashboard_password  # ← ADICIONADO
  - waha_swagger_password
```

E na seção de definição de secrets:

```yaml
secrets:
  waha_dashboard_password:
    file: ./secrets/waha_dashboard_password.txt
```

### 3. Script de Configuração Automática

Criado o script `setup_secrets.sh` que:
- Gera automaticamente todos os arquivos de secrets necessários
- Usa valores criptograficamente seguros (via `openssl rand -base64 32`)
- Verifica se os arquivos já existem antes de sobrescrever
- Fornece feedback claro sobre o processo

## 🚀 Como Usar

### Passo 1: Executar o Script de Configuração

```bash
cd /caminho/para/CapyVagas-UTFPR
./setup_secrets.sh
```

Este script criará automaticamente todos os arquivos necessários no diretório `secrets/`:
- `django_secret_key.txt`
- `postgres_password.txt`
- `waha_api_key.txt`
- `waha_dashboard_password.txt`
- `waha_swagger_password.txt`

### Passo 2: (Opcional) Personalizar as Senhas

Se você quiser usar senhas específicas em vez das geradas automaticamente, edite os arquivos manualmente:

```bash
# Exemplo: definir senha personalizada para o dashboard do WAHA
echo "MinhaSenh@Segur@123" > secrets/waha_dashboard_password.txt
```

### Passo 3: Configurar o Arquivo .env

Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp .env.example .env
nano .env  # ou use seu editor preferido
```

**Importante:** As senhas do WAHA **não** vão no `.env`, elas ficam nos arquivos de secrets!

### Passo 4: Iniciar os Serviços

```bash
docker-compose up -d
```

### Passo 5: Verificar os Logs

```bash
# Ver logs do WAHA
docker-compose logs -f waha

# Ver logs de todos os serviços
docker-compose logs -f
```

## 🔐 Estrutura de Autenticação do WAHA

Após a correção, o WAHA possui três níveis de autenticação:

### 1. API Key (para requisições programáticas)
- **Variável:** `WAHA_API_KEY_FILE`
- **Secret:** `secrets/waha_api_key.txt`
- **Uso:** Autenticação de API via header `X-Api-Key`

### 2. Dashboard (interface web administrativa)
- **Username:** Definido em `.env` como `WAHA_DASHBOARD_USERNAME` (padrão: `admin`)
- **Password:** Lido de `secrets/waha_dashboard_password.txt`
- **Acesso:** `http://waha.seu-dominio.com` ou `http://localhost:3000`

### 3. Swagger (documentação interativa da API)
- **Username:** Definido em `.env` como `WHATSAPP_SWAGGER_USERNAME` (padrão: `swagger`)
- **Password:** Lido de `secrets/waha_swagger_password.txt`
- **Acesso:** `http://waha.seu-dominio.com/swagger` ou `http://localhost:3000/swagger`

## 🔄 Mudanças nos Arquivos

### docker-compose.yml
- ✅ Removidos valores hardcoded de `WAHA_API_KEY` e `WAHA_DASHBOARD_PASSWORD`
- ✅ Adicionado uso de `_FILE` para todas as credenciais sensíveis
- ✅ Adicionado secret `waha_dashboard_password` na lista de secrets do serviço
- ✅ Adicionada definição do secret `waha_dashboard_password` na seção global

### .env.example
- ✅ Mantido como referência (já estava correto)

### Novos Arquivos
- ✅ `setup_secrets.sh` - Script de configuração automática
- ✅ `WAHA_FIX_DOCUMENTATION.md` - Esta documentação

## ⚠️ Notas Importantes

### Segurança
- **NUNCA** commite os arquivos `.txt` do diretório `secrets/` no Git
- Os arquivos de secrets já estão no `.gitignore`
- Use senhas fortes e únicas para produção

### Compatibilidade
- Esta configuração usa Docker Secrets (file-based)
- Funciona em Docker Compose e Docker Swarm
- Não requer Docker Swarm mode para funcionar

### Troubleshooting

#### Problema: "Permission denied" ao executar setup_secrets.sh
```bash
chmod +x setup_secrets.sh
./setup_secrets.sh
```

#### Problema: WAHA ainda não aceita a senha
1. Verifique se os arquivos de secrets existem:
   ```bash
   ls -la secrets/*.txt
   ```

2. Verifique se não há espaços em branco ou quebras de linha extras:
   ```bash
   cat secrets/waha_dashboard_password.txt | od -c
   ```

3. Recrie os containers:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

#### Problema: "secret not found"
Certifique-se de que está executando o Docker Compose no diretório correto (onde está o `docker-compose.yml`).

## 📚 Referências

- [Documentação oficial do WAHA](https://waha.devlike.pro/)
- [Docker Secrets Documentation](https://docs.docker.com/engine/swarm/secrets/)
- [Docker Compose Secrets](https://docs.docker.com/compose/use-secrets/)

## 🎯 Resultado Esperado

Após aplicar essas correções:
- ✅ As senhas definidas nos arquivos de secrets serão respeitadas
- ✅ Você poderá personalizar cada senha individualmente
- ✅ A autenticação do WAHA funcionará de forma consistente
- ✅ Não haverá mais conflitos entre valores hardcoded e secrets
- ✅ O sistema seguirá as melhores práticas de segurança do Docker
