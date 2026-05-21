#!/bin/bash
# Script para iniciar el backend de FastAPI

cd /workspaces/fastapi
source myvenv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Si el puerto 8000 está en uso, intenta con 8888
# uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
