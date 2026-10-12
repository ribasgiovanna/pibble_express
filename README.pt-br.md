# Pibble Express

[English](README.md) · Português

Aplicação web em Django para gestão de entregas: cadastro de clientes, produtos,
funcionários e entregas, com autenticação e níveis de acesso.

Projeto em equipe. Este é um fork do repositório original
[`rodavio/pibble_express`](https://github.com/rodavio/pibble_express), mantido na conta
da Giovanna como referência de portfólio.

| Dashboard | Módulo de funcionários |
|---|---|
| ![Dashboard](docs/dashboard.png) | ![Cadastro de funcionários](docs/funcionarios.png) |

## Equipe e responsabilidades

| Pessoa | Contribuição |
|---|---|
| Otávio ([@rodavio](https://github.com/rodavio)) | Criação e estrutura do projeto, views principais, base do CRUD |
| Giovanna Ribas dos Reis ([@ribasgiovanna](https://github.com/ribasgiovanna)) | Proposta do Django como framework; módulo de Funcionários e sua integração com Entregas; cadastro aceitando CPF e CNPJ (formulário + migration); dashboard administrativo; padronização dos formulários nos quatro apps e botão de logout |
| Pedro Henrique de Andrade de Moraes ([perfil](https://github.com/pedrooh131313)) | Ajustes gerais |

## Funcionalidades

- Autenticação de usuários (login / logout), com `LOGIN_URL` na raiz
- Níveis de acesso: cada `Funcionario` tem `tipo_usuario` `ADM` (administrador) ou `FUNC`
  (funcionário), ligado a um `User` do Django por um `OneToOneField`
- CRUD completo de Clientes, Produtos, Funcionários e Entregas (listar / editar / excluir)
- Dashboard administrativo
- Cadastro de funcionário aceitando CPF ou CNPJ
- Máscaras nos campos dos formulários (`static/js/form-masks.js`)
- API REST (Django REST Framework) em `/api/`, via `DefaultRouter`, para os quatro recursos

## Tecnologias

- Python 3, Django 6, Django REST Framework
- SQLite (desenvolvimento)
- HTML / CSS / JS nos templates

## Estrutura

```
.
├── core/              # projeto Django: settings, urls, views de login e dashboard
├── clientes/          # app: model, form, serializer, views
├── produtos/          # app
├── funcionarios/      # app (níveis de acesso ADM/FUNC)
├── entregas/          # app
├── templates/         # base, login, dashboard, telas de CRUD
├── static/            # css, js (máscaras de formulário), imagem
└── manage.py
```

## Como executar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # defina DJANGO_SECRET_KEY e DJANGO_DEBUG

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. O admin do Django fica em `/admin/` e a API em `/api/`.
O `db.sqlite3` é criado localmente pelo `migrate` e não é versionado.

`SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` são lidos das variáveis de ambiente (com valores
padrão para desenvolvimento). Em produção, defina-os no `.env` e use `DJANGO_DEBUG=False`.
