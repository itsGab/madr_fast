#!/bin/sh

# executa migracoes
poetry run alembic upgrade head

# inicia app
poetry run fastapi run ./madr_fast/app.py