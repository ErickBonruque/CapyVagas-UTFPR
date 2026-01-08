# 🔐 Credenciais do Sistema

## Dashboard Web (Gerenciamento de Cursos e Interações)

**URL de Acesso:** http://localhost:8000/dashboard/

**Credenciais (Configuradas no .env):**
```
Usuário: admin
Senha: changeme
```

> **Importante:** Estas credenciais são definidas no arquivo `.env` e são carregadas automaticamente.  
> Você pode visualizá-las e alterá-las em: http://localhost:8000/dashboard/bot/configuration/

---

## Django Admin (Administração do Sistema)

**URL de Acesso:** http://localhost:8000/admin/

**Credenciais:**
```
Usuário: admin
Senha: changeme
```

Estas credenciais também são configuráveis via dashboard ou podem ser alteradas pelo terminal:
```bash
docker-compose run --rm backend python manage.py changepassword admin
```

---

## WAHA Dashboard (Interface do WhatsApp)

**URL de Acesso:** http://localhost:3000/dashboard/

**Credenciais:**
```
Usuário: admin
Senha: admin123
```

**API Key para comunicação:**
```
Chave: capyvagas2024
Uso: Header "X-Api-Key: capyvagas2024"
```

**Swagger Documentation:**
- URL: http://localhost:3000/swagger
- Usuário: swagger
- Senha: admin123

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
docker-compose restart
```

### 3. Credenciais WAHA
As credenciais do WAHA estão configuradas no docker-compose.yml:
```yaml
environment:
  - WAHA_DASHBOARD_USERNAME=admin
  - WAHA_DASHBOARD_PASSWORD=admin123
  - WAHA_API_KEY=capyvagas2024
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
curl http://localhost:3000/dashboard/
```

### Testar autenticação no WAHA:
```bash
curl -u admin:admin123 http://localhost:3000/dashboard/
```

### Testar API Key do WAHA:
```bash
curl -H "X-Api-Key: capyvagas2024" http://localhost:3000/api/sessions
```

---

## Conectando o WhatsApp

1. Acesse http://localhost:3000/dashboard/
2. Faça login com admin/admin123
3. Clique em "Start Session" ou escaneie o QR Code
4. Pronto! O WhatsApp estará conectado ao CapyVagas

---

## Problemas Comuns

### "Credenciais inválidas" no Dashboard WAHA
- Use a URL correta: http://localhost:3000/dashboard/ (não esqueça da barra no final)
- Verifique as credenciais: admin/admin123

### "Não consigo acessar o WAHA"
- Verifique se o container WAHA está rodando: `docker-compose ps`
- A URL correta é http://localhost:3000/dashboard/

### "API não responde"
- Verifique se a API key está correta: capyvagas2024
- Use o header: `X-Api-Key: capyvagas2024`
