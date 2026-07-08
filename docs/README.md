# 💳 SimulaBank

Sistema bancário desenvolvido para fins **didáticos**, utilizando **Python**, **Django** e **PostgreSQL**.

O objetivo deste projeto é simular operações bancárias reais para praticar desenvolvimento Web, banco de dados, deploy em nuvem e boas práticas de engenharia de software.

Além do desenvolvimento da aplicação, este projeto também demonstra conhecimentos em:

- Desenvolvimento Back-end
- Banco de Dados
- Deploy Cloud
- Git e GitHub
- Testes de Software
- Automação de Testes (em desenvolvimento)

---

# 📑 Índice

- Tecnologias
- Arquitetura
- Estrutura do Projeto
- Funcionalidades
- Como executar
- Instalação do PostgreSQL
- Configuração do ambiente
- Deploy
- Objetivos do Projeto
- Roadmap
- Imagens
- Licença
- Autor

---

# 🚀 Tecnologias

- Python 3.11
- Django 4.2
- PostgreSQL
- Gunicorn
- WhiteNoise
- HTML5
- CSS3
- Bootstrap 5
- Git
- GitHub
- Render

---

# 🏗 Arquitetura

```
                Usuário
                   │
                   ▼
         Front-end (Bootstrap)
                   │
                   ▼
            Django Framework
                   │
                   ▼
             PostgreSQL Database
                   │
                   ▼
           Deploy Cloud (Render)
```

---

# 📂 Estrutura do Projeto

```
SimulaBank/

│

├── config/

├── core/

├── templates/

├── static/

├── media/

├── requirements.txt

├── manage.py

├── .env.example

└── README.md
```

---

# ✨ Funcionalidades

Atualmente o sistema possui:

- Cadastro de Clientes
- Login
- Logout
- Dashboard
- Consulta de Saldo
- Depósito
- Saque
- Transferência PIX
- Histórico de Movimentações
- Alteração dos Dados do Cliente
- Área Administrativa (Django Admin)
- Deploy em Nuvem

---

# ⚙️ Como executar o projeto

## 1 - Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/SimulaBank.git

cd SimulaBank
```

---

## 2 - Instalar o Python

Baixe a versão mais recente do Python:

https://www.python.org/downloads/

Durante a instalação marque:

```
Add Python to PATH
```

Verifique:

```bash
python --version
```

---

# 🐘 Instalação do PostgreSQL

Faça o download:

https://www.postgresql.org/download/

Durante a instalação:

- Instale também o pgAdmin
- Defina uma senha para o usuário postgres
- Utilize a porta padrão 5432

Após concluir:

Abra o pgAdmin

Crie um banco chamado:

```
simulabank
```

Ou execute:

```sql
CREATE DATABASE simulabank;
```

Caso deseje criar um usuário específico:

```sql
CREATE USER simulabank_user
WITH PASSWORD 'suasenha';

ALTER ROLE simulabank_user
SET client_encoding TO 'utf8';

ALTER ROLE simulabank_user
SET default_transaction_isolation TO 'read committed';

ALTER ROLE simulabank_user
SET timezone TO 'UTC';

GRANT ALL PRIVILEGES
ON DATABASE simulabank
TO simulabank_user;

ALTER DATABASE simulabank
OWNER TO simulabank_user;
```

---

# 🖥 Criando o ambiente virtual

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# 📦 Instalando as dependências

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configurando o ambiente

Crie um arquivo:

```
.env
```

Utilize o arquivo `.env.example` como modelo.

Exemplo:

```env
SECRET_KEY=sua-secret-key

DEBUG=True

DATABASE_URL=postgresql://simulabank_user:senha@localhost:5432/simulabank

ALLOWED_HOSTS=127.0.0.1,localhost
```

---

# 🗄 Executando as migrações

```bash
python manage.py migrate
```

---

# 👤 Criando o Superusuário

```bash
python manage.py createsuperuser
```

Informe:

- Usuário
- E-mail
- Senha

---

# ▶️ Executando o projeto

```bash
python manage.py runserver
```

Abra:

```
http://127.0.0.1:8000
```

Administração:

```
http://127.0.0.1:8000/admin
```

---

# ☁️ Deploy

O projeto encontra-se preparado para deploy utilizando:

- Render
- PostgreSQL
- Gunicorn
- WhiteNoise
- Variáveis de ambiente (.env)

Durante o deploy são executados automaticamente:

```bash
pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate
```

---

# 📸 Imagens

Em desenvolvimento.

Futuramente serão adicionadas imagens de:

- Login
- Dashboard
- Depósito
- Saque
- PIX
- Histórico
- Área Administrativa

---

# 📚 Objetivos do Projeto

Este projeto foi desenvolvido para praticar:

- Desenvolvimento Web com Django

- Banco de Dados PostgreSQL

- Deploy em Nuvem

- Git e GitHub

- Organização de Projetos

- Boas práticas de programação

- Testes de Software

- Automação de Testes

- APIs REST

---

# 🛣 Roadmap

## ✅ Concluído

- Sistema de Login

- Cadastro de Clientes

- Dashboard

- Operações Bancárias

- Histórico de Movimentações

- Área Administrativa

- Deploy em Nuvem

---

## 🚧 Em desenvolvimento

- API REST

- Testes Automatizados

- Docker

- GitHub Actions

- CI/CD

- Recuperação de Senha

- Extrato PDF

- Dashboard com gráficos

- Testes de Performance

- Cobertura de Testes

---

# 📖 Documentação

Toda a documentação do projeto será disponibilizada na pasta:

```
/docs
```

Incluindo:

- Manual de instalação

- Manual de Deploy

- Manual do Desenvolvedor

- Casos de Teste

- Evidências

- Diagramas

---

# 📄 Licença

Este projeto possui finalidade exclusivamente didática.

Licenciado sob a licença MIT.

---

# 👨‍💻 Autor

## Thiago Kosovski

Analista de Testes Sênior

Especialista em Qualidade de Software (QA)

Automação de Testes

Python • Django • PostgreSQL

Mais de **10 anos de experiência** em testes de software, sistemas financeiros, qualidade de aplicações, automação de testes e melhoria contínua.

GitHub

https://github.com/thiagokosovski
