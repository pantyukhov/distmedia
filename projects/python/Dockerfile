FROM python:3.8-slim-buster as base
ENV PYTHONUNBUFFERED 1
ENV DATABASE_CONNECTION "sqlite://:memory:"

WORKDIR /usr/src/app

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    make \
    git \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/matransfer_moneyn/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM base

ENV DATABASE_CONNECTION "sqlite://:memory:"

ADD ./pyproject.toml /usr/src/app/projects/python/pyproject.toml
ADD ./poetry.lock /usr/src/app/projects/python/poetry.lock
ADD ./install.sh /usr/src/app/projects/python/install.sh

WORKDIR /usr/src/app/projects/python

RUN BUILD_NO_DEV=true /usr/src/app/projects/python/install.sh

ADD . /usr/src/app/projects/python

RUN python manage.py collectstatic --no-input
RUN python manage.py migrate

ARG SERVICE_VERSION="undefined"
ENV SERVICE_VERSION $SERVICE_VERSION

CMD [ "python", "./manage.py runserver 0.0.0.0:8000"]
#CMD ["gunicorn", "app.wsgi", "-w", "2", "--max-requests", "1000", "-b", "0.0.0.0:8000"]

