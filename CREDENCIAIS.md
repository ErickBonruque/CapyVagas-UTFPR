# 🔐 Credenciais do Sistema

## Dashboard Web (Gerenciamento de Cursos e Interações)

**URL de Acesso:** http://localhost:8000/dashboard/

**Credenciais (Configuradas no .env):**
```
Usuário: admin
Senha: waha_strong_password_123!
```

> **Importante:** Estas credenciais são definidas no arquivo `.env` e são carregadas automaticamente.  
> Você pode visualizá-las e alterá-las em: http://localhost:8000/dashboard/bot/configuration/

Estas credenciais são configuráveis na página de **Configuração WAHA** do próprio dashboard.

---

## Django Admin (Administração do Sistema)

**URL de Acesso:** http://localhost:8000/admin/

**Credenciais:**
```
Usuário: admin
Senha: waha_strong_password_123!
```

Estas credenciais também são configuráveis via dashboard ou podem ser alteradas pelo terminal:
```bash
docker-compose run --rm backend python manage.py changepassword admin
```

---

## WAHA Dashboard (Interface do WhatsApp)

**URL de Acesso:** http://localhost:3000/dashboard/

**Credenciais:**
- Configuradas através do arquivo `.env`
- API Key: `waha_secret_key`
- Session: `default`

---

## Como Alterar as Credenciais

### 1. Pelo Dashboard Web
Acesse: http://localhost:8000/dashboard/ → **Configuração WAHA**

### 2. Pelo arquivo .env
Edite o arquivo `.env` na raiz do projeto:
```bash
BOT_DASHBOARD_USERNAME=seu_usuario
BOT_DASHBOARD_PASSWORD=sua_senha_segura
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_PASSWORD=sua_senha_admin
```

Após alterar, execute:
```bash
make restart
```

---

## Endpoints da API REST

**Base URL:** http://localhost:8000/api/

### Endpoints principais:
- `/api/courses/` - Gerenciar cursos
- `/api/terms/` - Gerenciar termos de busca
- `/api/interactions/` - Visualizar histórico de interações
- `/api/bot/status/` - Status do bot WAHA
- `/api/bot/configuration/` - Configurações do bot

**Documentação completa:** http://localhost:8000/api/

---

## Testes de Conectividade

### Verificar se o backend está rodando:
```bash
curl http://localhost:8000/api/
```

### Verificar se o WAHA está rodando:
```bash
curl http://localhost:3000/
```

### Testar autenticação no Django Admin:
```bash
curl -X POST http://localhost:8000/admin/login/ \
  -d "username=admin&password=waha_strong_password_123!"
```

---

## Problemas Comuns

### "Credenciais inválidas" no Dashboard
- Verifique se o arquivo `.env` está correto
- Execute `make restart` para recriar os containers
- Acesse a página de Configuração WAHA para ver as credenciais atuais

### "Não consigo acessar o WAHA"
- Verifique se o container WAHA está rodando: `docker-compose ps`
- O link clicável no dashboard aponta para: http://localhost:3000/dashboard/
