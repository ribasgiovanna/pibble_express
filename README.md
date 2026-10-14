# Pibble Express

English · [Português](README.pt-br.md)

[![Tests](https://github.com/ribasgiovanna/pibble_express/actions/workflows/tests.yml/badge.svg)](https://github.com/ribasgiovanna/pibble_express/actions/workflows/tests.yml)

A Django web application for delivery management: registration of clients, products,
employees and deliveries, with authentication and access levels.

Team project. This is a fork of the original repository
[`rodavio/pibble_express`](https://github.com/rodavio/pibble_express), kept on
Giovanna's account for portfolio reference.

| Dashboard | Employees module |
|---|---|
| ![Dashboard](docs/dashboard.png) | ![Employee registration](docs/funcionarios.png) |

## Team and roles

| Person | Contribution |
|---|---|
| Otávio ([@rodavio](https://github.com/rodavio)) | Project creation and structure, main views, CRUD base |
| Giovanna Ribas dos Reis ([@ribasgiovanna](https://github.com/ribasgiovanna)) | Proposed Django as the framework; Employees module and its integration with Deliveries; registration accepting CPF and CNPJ (form + migration); administrative dashboard; form standardization across the four apps and the logout button |
| Pedro Henrique de Andrade de Moraes ([profile](https://github.com/pedrooh131313)) | General adjustments |

## Features

- User authentication (login / logout) with `LOGIN_URL` at the root
- Access levels: each `Funcionario` has `tipo_usuario` `ADM` (administrator) or `FUNC`
  (employee), linked to a Django `User` through a `OneToOneField`. The dashboard and employee
  management are restricted to administrators on the server, not only hidden in the menu
- Full CRUD for Clients, Products, Employees and Deliveries (list / edit / delete)
- Administrative dashboard
- Employee registration accepting either CPF or CNPJ
- Form input masks on the front end (`static/js/form-masks.js`)
- REST API (Django REST Framework) exposed at `/api/` via `DefaultRouter` for the four resources;
  it requires login, and employee data (CPF, address) is available to administrators only

## Tech

- Python 3, Django 6, Django REST Framework
- SQLite (development)
- HTML / CSS / JS in the templates

## Structure

```
.
├── core/              # Django project: settings, urls, login/dashboard views
├── clientes/          # app: model, form, serializer, views
├── produtos/          # app
├── funcionarios/      # app (ADM/FUNC access levels)
├── entregas/          # app
├── templates/         # base, login, dashboard, CRUD screens
├── static/            # css, js (form masks), image
└── manage.py
```

## Running

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # set DJANGO_SECRET_KEY and DJANGO_DEBUG

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The Django admin is at `/admin/` and the API at `/api/`.
`db.sqlite3` is created locally by `migrate` and is not version-controlled.

`SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` are read from the environment (with a
development fallback). For production, set them in `.env` and use `DJANGO_DEBUG=False`.

## Security and tests

A review of the fork found three access-control gaps, now fixed and covered by tests:

| Issue | Fix |
|---|---|
| The REST API accepted requests without login (DRF's default permission is `AllowAny`) | `IsAuthenticated` by default; the employees endpoint is admin-only |
| `FUNC` users could open employee management by typing the URL, since the restriction was only in the menu | `admin_obrigatorio` decorator on the dashboard and employee views; each profile lands on its own start page after login |
| Records were deleted through plain links (GET), which another site could trigger on behalf of a logged-in user (CSRF) | Deletes accept POST only, through forms with a CSRF token |

```bash
python manage.py test
```

The suite also runs on every push and pull request (GitHub Actions).

21 tests cover form formatting (CPF/CNPJ, phone), login and logout, access levels, POST-only
deletes with CSRF protection and API permissions. The access-control tests were checked
against the previous code, where they fail.
