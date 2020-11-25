FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# This version builds on top of:
# - buster (debian)
# - python
# - tiangolo/uvicorn-gunicorn
# - tiangolo/uvicorn-gunicorn-fastapi

# These last 2 images are not always up to date so we do an extra update step
#  update and cleanup
RUN apt-get update && apt-get -y upgrade && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR .
COPY . /app

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r /app/requirements_dev.txt ; else pip install -r /app/requirements.txt ; fi"


ENV PYTHONPATH=/app
# See https://github.com/tiangolo/uvicorn-gunicorn-docker#advanced-usage
ENV MODULE_NAME="overstroomik_service.main"
