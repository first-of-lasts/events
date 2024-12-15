## Run project:
```sh
uvicorn events.main.web:app --reload
```
---

## Internationalization
### Generate
```sh
python manage.py generate_translations
```
### Compile:
```sh
python manage.py compile_translations
```
---

## Migrations
### Create migration
```sh
alembic revision --autogenerate -m "migration name"
```
### Upgrade db 
```sh
alembic upgrade head
```
### Downgrade db
```sh
alembic downgrade -1
```
---
