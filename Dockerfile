FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=pos_django_cafe.settings

EXPOSE 8000

CMD poetry run python manage.py migrate && \
    poetry run python manage.py runserver 0.0.0.0:8000


