# 🐳 Como Rodar o Projeto com Docker

## 📋 Pré-requisitos

- Docker instalado e rodando
- Docker Compose instalado
- Terminal aberto na pasta do projeto

---

## 🚀 Como Subir o Projeto pela Primeira Vez

### 1. Parar todos os containers (se houver algo rodando)

```bash
docker-compose down
```

### 2. Fazer o build das imagens

```bash
docker-compose build
```

**ou usar o Makefile:**

```bash
make build
```

### 3. Subir os containers

```bash
docker-compose up
```

**Para rodar em background (modo daemon):**

```bash
docker-compose up -d
```

**ou usar o Makefile:**

```bash
make up
```

### 4. Aplicar migrações do banco de dados

```bash
docker-compose exec backend python manage.py migrate
```

**ou usar o Makefile:**

```bash
make migrate
```

### 5. Verificar se está rodando

```bash
docker-compose ps
```

Você deve ver algo assim:

```
NAME                      IMAGE                   STATUS
waha_capyvaga-backend-1   waha_capyvaga-backend   Up
waha_capyvaga-waha-1      devlikeapro/waha        Up
```

---

## 🔄 Como Aplicar Alterações no Docker

### Cenário 1: Alterou arquivos Python (.py)

**Não precisa rebuildar!** O código é montado via volume.

Basta reiniciar o serviço:

```bash
docker-compose restart backend
```

**ou parar e subir novamente:**

```bash
docker-compose down
docker-compose up -d
```

---

### Cenário 2: Alterou requirements.txt (novas dependências)

**Precisa rebuildar a imagem:**

```bash
# 1. Parar os containers
docker-compose down

# 2. Rebuildar a imagem do backend
docker-compose build backend

# 3. Subir novamente
docker-compose up -d
```

**ou usar o Makefile:**

```bash
make build
make up
```

---

### Cenário 3: Alterou models.py (banco de dados)

**Precisa criar e aplicar migrações:**

```bash
# 1. Criar as migrações
docker-compose exec backend python manage.py makemigrations

# 2. Aplicar as migrações
docker-compose exec backend python manage.py migrate
```

**ou usar o Makefile:**

```bash
make makemigrations
make migrate
```

---

### Cenário 4: Alterou docker-compose.yml ou Dockerfile

**Precisa rebuildar tudo:**

```bash
# 1. Parar e remover containers
docker-compose down

# 2. Rebuildar tudo
docker-compose build

# 3. Subir novamente
docker-compose up -d
```

---

## 📦 Comandos Úteis do Makefile

O projeto já tem um Makefile com atalhos:

```bash
make build          # Constrói as imagens Docker
make up             # Sobe os containers (foreground)
make down           # Para e remove os containers
make migrate        # Aplica migrações do Django
make makemigrations # Cria novas migrações
make shell          # Abre shell do Django
```

---

## 🛠️ Workflow Completo (Start do Zero)

Execute os comandos na ordem:

```bash
# 1. Parar tudo (se houver algo rodando)
docker-compose down

# 2. Construir as imagens
make build

# 3. Subir os containers em background
docker-compose up -d

# 4. Aplicar migrações do banco
make migrate

# 5. Verificar se está rodando
docker-compose ps

# 6. Ver logs (opcional)
docker-compose logs -f backend
```

---

## 📊 Verificar se Está Funcionando

### 1. Verificar containers rodando

```bash
docker-compose ps
```

### 2. Ver logs do backend

```bash
docker-compose logs -f backend
```

### 3. Ver logs do WAHA

```bash
docker-compose logs -f waha
```

### 4. Acessar no navegador

- **Dashboard:** http://localhost:8000/dashboard/
- **API:** http://localhost:8000/api/
- **Admin:** http://localhost:8000/admin/
- **WAHA Swagger:** http://localhost:3000/

---

## 🐛 Resolução de Problemas

### Problema: "Port already in use" (porta já em uso)

```bash
# Parar tudo
docker-compose down

# Verificar o que está usando a porta
sudo lsof -i :8000
sudo lsof -i :3000

# Matar o processo (se necessário)
sudo kill -9 <PID>

# Subir novamente
docker-compose up -d
```

---

### Problema: "Permission denied" ao fazer build

```bash
# Limpar tudo e reconstruir
docker-compose down -v
docker system prune -a
make build
docker-compose up -d
```

---

### Problema: Backend não está respondendo

```bash
# Ver logs
docker-compose logs backend

# Reiniciar o serviço
docker-compose restart backend

# Se persistir, rebuildar
make build
docker-compose up -d
```

---

### Problema: Sessão do WAHA foi perdida

**A sessão está persistida em `./waha-sessions/`**

Se você deletou essa pasta por acidente:
1. Será necessário escanear o QR Code novamente
2. Acesse http://localhost:3000/ e siga as instruções

**Para preservar a sessão:**
- ✅ **Nunca delete** a pasta `waha-sessions/`
- ✅ Ela está no `.dockerignore` para não ser copiada no build
- ✅ Está mapeada como volume no `docker-compose.yml`

---

## 🔄 Workflow de Desenvolvimento Diário

### Ao começar a trabalhar:

```bash
# Subir os containers
docker-compose up -d

# Ver logs (opcional)
docker-compose logs -f backend
```

### Durante o desenvolvimento:

- **Alterou código Python?** → Arquivo é montado via volume, mudanças são automáticas
- **Adicionou dependência?** → `make build` + `docker-compose up -d`
- **Alterou model?** → `make makemigrations` + `make migrate`

### Ao terminar:

```bash
# Parar os containers (mas manter volumes)
docker-compose stop

# OU parar e remover (mas preserva volumes)
docker-compose down
```

---

## 📝 Resumo dos Comandos Principais

| Ação | Comando |
|------|---------|
| **Subir pela primeira vez** | `make build && docker-compose up -d && make migrate` |
| **Subir no dia a dia** | `docker-compose up -d` |
| **Ver logs** | `docker-compose logs -f backend` |
| **Parar tudo** | `docker-compose down` |
| **Reiniciar** | `docker-compose restart backend` |
| **Rebuildar** | `make build && docker-compose up -d` |
| **Aplicar migrações** | `make migrate` |
| **Criar migrações** | `make makemigrations` |
| **Shell Django** | `make shell` |

---

## 🎯 Comandos para Rodar Agora

**Cole isso no terminal:**

```bash
# Parar tudo
docker-compose down

# Rebuildar (inclui as novas dependências: DRF, django-filter)
docker-compose build

# Subir em background
docker-compose up -d

# Aplicar migrações (se ainda não aplicou)
docker-compose exec backend python manage.py migrate

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f backend
```

**Depois de rodar, acesse:**
- http://localhost:8000/dashboard/

---

## ✅ Checklist de Funcionamento

Após rodar os comandos, verifique:

- [ ] Containers estão rodando: `docker-compose ps`
- [ ] Backend está acessível: http://localhost:8000/
- [ ] Dashboard carrega: http://localhost:8000/dashboard/
- [ ] API funciona: http://localhost:8000/api/
- [ ] WAHA está online: http://localhost:3000/

---

## 📚 Referências

- **Docker Compose:** https://docs.docker.com/compose/
- **Django com Docker:** https://docs.djangoproject.com/en/5.2/howto/deployment/
- **WAHA Docs:** https://waha.devlike.pro/

---

🎉 **Pronto! Seu ambiente Docker está configurado e rodando!**
