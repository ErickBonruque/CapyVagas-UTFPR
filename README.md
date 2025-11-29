# CapyVagas-UTFPR

Bot de WhatsApp integrado ao WAHA com dashboard administrativo em Django/DRF.

## Visão geral da arquitetura
- **config/**: carregamento de variáveis de ambiente e objetos de configuração reutilizáveis (WAHA, credenciais do dashboard, flags de debug).
- **apps/**: aplicativos Django separados por domínio (bot, courses, users, dashboard). Serviços do bot usam injeção de dependências para facilitar testes e colaboração com IAs de código.
- **infra/**: integrações externas (WAHA e JobSpy) encapsuladas em clientes e serviços.
- **waha_bot/**: configuração do projeto Django.

## Fluxo de autenticação do bot
- Credenciais de RA/senha são fornecidas pelo usuário via WhatsApp e validadas por `UTFPRAuthService`.
- O vínculo entre telefone e RA é persistido em `UserProfile`.
- O dashboard pode definir URLs, tokens e sessão do WAHA via endpoint `/api/bot/configuration/`, armazenando-as em `BotConfiguration` para uso pelo `BotService`.

## Variáveis de ambiente
Copie `.env.example` para `.env` e ajuste se necessário:

```
DJANGO_SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
WAHA_URL=http://localhost:3000
WAHA_API_KEY=dev-api-key
WAHA_SESSION_NAME=dev-session
WAHA_TIMEOUT_SECONDS=5
BOT_DASHBOARD_USERNAME=admin
BOT_DASHBOARD_PASSWORD=password
```

## Comandos de instalação e execução
1. Instale dependências Python (use ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```
2. Aplique migrações e rode o servidor:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```
3. Para executar o bot/dash em Docker:
   ```bash
   make up
   ```

## Testes e qualidade de código
- Testes Django:
  ```bash
  python manage.py test
  ```
- Lint/format (Black e Ruff configurados em `pyproject.toml`):
  ```bash
  ruff check .
  black --check .
  ```

## Pontos de melhoria futura
- Implementar autenticação real no dashboard e rotas protegidas.
- Conectar JobSpy real em `JobSearchService` com credenciais apropriadas.
- Adicionar cache/filas para mensagens WAHA e monitoramento ativo de sessão.
- Criar frontend React dedicado para o dashboard.
