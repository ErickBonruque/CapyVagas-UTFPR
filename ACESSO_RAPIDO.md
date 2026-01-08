# 🚀 CapyVagas - Acesso Rápido

## URLs de Acesso

### 📱 WAHA WhatsApp Dashboard
- **URL**: http://localhost:3000/dashboard/
- **Login**: admin / admin123
- **API Key**: capyvagas2024

### 🖥️ Backend Django
- **Dashboard**: http://localhost:8000/dashboard/
- **Admin**: http://localhost:8000/admin/
- **Login**: admin / changeme

### 📊 Monitoramento
- **Traefik**: http://localhost:8080
- **API Docs**: http://localhost:8000/api/docs/
- **WAHA Swagger**: http://localhost:3000/swagger (swagger/admin123)

## Comandos Úteis

```bash
# Verificar status dos containers
docker compose ps

# Verificar logs
docker compose logs -f waha
docker compose logs -f backend

# Reiniciar serviços
docker compose restart waha
docker compose restart backend

# Parar tudo
docker compose down

# Iniciar tudo
docker compose up -d
```

## Conectar WhatsApp

1. Acesse: http://localhost:3000/dashboard/
2. Login: admin / admin123
3. Escaneie o QR Code com o WhatsApp

## 📚 Documentação Completa
- [Credenciais Detalhadas](docs/guides/CREDENCIAIS.md)
- [Guia de Instalação](docs/guides/COMO_RODAR_DOCKER.md)
