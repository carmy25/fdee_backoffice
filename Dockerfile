ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

EXPOSE 5432
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:5432 --workers 2 foodee_backoffice.wsgi"]
