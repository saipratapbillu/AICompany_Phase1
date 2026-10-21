@echo off
if not exist .env copy .env.example .env
python -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
