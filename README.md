# Books library

Setup project

## Prerequisites

- Python 3.11
- PostgreSQL
- pip

## 1. CLone repository

```bash
git clone https://github.com/vladlevkovich/book-library.git
```
cd book-library

## 2. Create and activate virtual environment
```bash
python -m venv venv

\venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Setup database

```bash
psql -U postgres -c "CREATE DATABASE books;"
```

Execute command
```bash
uvicorn app.main:app
```
If there are no tables, they will be created, and if there are, the request to create tables will not be executed.

## 5. Running tests

```bash
pytest
```
