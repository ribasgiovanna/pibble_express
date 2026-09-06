# 📦 Pibble Express

Sistema web de **gestão de entregas** feito em **Django**: cadastro de clientes,
produtos, funcionários e entregas, com autenticação e níveis de acesso.

> **Projeto em equipe.** Este é um fork do repositório original
> [`rodavio/pibble_express`](https://github.com/rodavio/pibble_express), mantido na
> conta da Giovanna para referência de portfólio.

## 👥 Equipe e papéis

| Pessoa | Contribuição |
|---|---|
| **otávio** ([@rodavio](https://github.com/rodavio)) | Criação e estrutura do projeto, views principais, base do CRUD |
| **Giovanna Ribas dos Reis** ([@ribasgiovanna](https://github.com/ribasgiovanna)) | Módulo de **Funcionários** e sua integração com **Entregas**; cadastro aceitando **CPF e CNPJ** (formulário + migração); **dashboard** com visão administrativa; padronização dos formulários dos quatro apps e botão de logout |
| **Pedro Henrique de Andrade de Moraes** ([perfil](https://github.com/pedrooh131313)) | Ajustes gerais |

## ⚙️ Funcionalidades

- **Autenticação** de usuário (login/logout) com `LOGIN_URL` na raiz
- **Níveis de acesso**: cada `Funcionario` tem `tipo_usuario` `ADM` (Administrador)
  ou `FUNC` (Funcionário), ligado a um `User` do Django por `OneToOneField`
- **CRUD** completo de Clientes, Produtos, Funcionários e Entregas
  (listar / editar / deletar)
- **Dashboard** com visão administrativa
- **Cadastro de funcionário** aceitando CPF **ou** CNPJ
- **Máscaras de formulário** no front (`static/js/form-masks.js`)
- **API REST** (Django REST Framework) exposta em `/api/` com `DefaultRouter`
  para os quatro recursos

## 🛠️ Stack

- Python 3 · Django 6 · Django REST Framework
- SQLite (desenvolvimento)
- HTML/CSS/JS nos templates

## 📁 Estrutura

```
.
├── core/              # projeto Django: settings, urls, views de login/dashboard
├── clientes/          # app: model, form, serializer, views
├── produtos/          # app
├── funcionarios/      # app (níveis de acesso ADM/FUNC)
├── entregas/          # app
├── templates/         # base, login, dashboard, telas de CRUD
├── static/            # css, js (máscaras de formulário), imagem
└── manage.py
```

## ▶️ Como executar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. O painel do Django fica em `/admin/` e a API em `/api/`.

> `DEBUG = True` e o `db.sqlite3` versionado são apropriados para trabalho acadêmico;
> em produção, mover segredos para variáveis de ambiente e desativar o debug.
