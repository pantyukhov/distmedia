#! /bin/sh

# exit if a command fails
set -e

if [ -n "$BUILD_NO_DEV" ]; then
  BUILD_NO_DEV="--no-dev"
else
  BUILD_NO_DEV=""
fi

echo $BUILD_NO_DEV

BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    libcurl4-openssl-dev \
    libssl-dev
    "

apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS

pip install --upgrade poetry pip setuptools wheel
poetry config virtualenvs.create false
poetry install -vv ${BUILD_NO_DEV}

apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS
rm -rf /var/lib/apt/lists/*
