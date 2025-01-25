# Books library

Setup project

## Prerequisites

- Python 3.11
- PostgreSQL
- pip

## 1. CLone repository

```bash
git clone https://github.com/your-username/your-project.git
```
cd your_project

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

Remove the comment from the line in main.py
```python
asyncio.run(init_users_db())
asyncio.run(init_books_db())
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
