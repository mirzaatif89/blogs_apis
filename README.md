Blog API (Django + DRF)
=======================

Overview
--------
Simple blog backend with public read-only endpoints and admin CRUD, using Django REST Framework, CKEditor uploads, and CORS enabled for the frontend.

Project Layout
--------------
- manage.py
- instruction.md — request/response samples
- blogapi/ — project settings & root URLs
- blog/ — app (models, serializers, views, urls, admin, migrations)
- media/ — uploads (git-ignored)
- requirements.txt — locked dependencies
- .env — env vars (git-ignored); see .env.example

Quick Start
-----------
1) Clone & enter project  
   - `git clone <repo> && cd blogapi`
   - Switch to the working branch (example): `git switch dependencies_added` then `git pull`
2) Create/activate venv  
   - Windows: `python -m venv .venv && .venv\Scripts\activate`  
   - macOS/Linux: `python -m venv .venv && source .venv/bin/activate`
3) Install dependencies  
   - `pip install -r requirements.txt`
4) Environment variables  
   - `cp .env.example .env` (or copy manually)  
   - Set a strong `SECRET_KEY`; keep `DEBUG=False` in prod  
   - For SQLite keep defaults; for another DB set `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
5) Migrate database  
   - `python manage.py migrate`
6) Run server  
   - `python manage.py runserver`
7) Media (uploads)  
   - Served from `/media/`; directory is git-ignored and created as files are uploaded.

Key Endpoints
-------------
- GET /blogs/
- GET /blogs/<slug>/
- Admin CRUD via /admin/blogs/ (also available under /api/ prefix)

More JSON shapes: see instruction.md.
