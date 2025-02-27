# POS Django Cafe - Installation Guide

## Prerequisites

Ensure you have the following installed on your system:
- [Pyenv](https://github.com/pyenv/pyenv) (for managing Python versions)
- [Poetry](https://python-poetry.org/) (for dependency management)
- A PostgreSQL server

---
## Running with Docker

### 1. Create the database (if it does not exist)
```sh
psql -U postgres -c "CREATE DATABASE your_db_name;"
```

### 2. Create a `.env` for Docker Usage

Create a specific `.env` for docker 

Example:
```env
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=host.docker.internal       # This allows Docker containers to access your local machine's PostgreSQL server
DB_PORT=5432
```

### 3. **Pull the image**:
   ```sh
   docker pull ilyagreen/pos-django-cafe:latest
```
### 4. **Run the image**:
   ```sh
   docker run --env-file pos_django_cafe\.env -p 8000:8000 --name django_app ilyagreen/pos-django-cafe:latest
```

## Local Setup

### 1. Install Python 3.12 using Pyenv
If Python 3.12 is not installed:
```sh
pyenv install 3.12
pyenv global 3.12
```

### 2. Install Poetry
If Poetry is not installed:
```sh
python -m pip install poetry
```

### 3. Install project dependencies
Navigate to the project directory and run:
```sh
poetry install
```

### 4. Create a `.env` file for configuration

Create a `.env` file in the project's root directory if it does not exist. This file will store environment variables such as database credentials.

Example `.env` file:
```env
# app/.env
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

Replace `your_db_name`, `your_db_user`, and `your_db_password` with your actual database credentials.

### 5. Create the database (if it does not exist)
```sh
psql -U postgres -c "CREATE DATABASE your_db_name;"
```

### 6. Apply database migrations

Run the following command to create the necessary tables:
```sh
poetry run python manage.py migrate
```

### 7. Run Tests
To ensure everything is working correctly, run the test suite:
```sh
poetry run python manage.py test
```
```sh
poetry run mypy .
```

### 8. Start the development server

Once everything is set up, start the Django server:
```sh
poetry run python manage.py runserver
```

---


