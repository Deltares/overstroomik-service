FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR .
COPY . /app

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r /app/requirements_dev.txt ; else pip install -r /app/requirements.txt ; fi"


ENV PYTHONPATH=/app
# See https://github.com/tiangolo/uvicorn-gunicorn-docker#advanced-usage
ENV MODULE_NAME="overstroomik_service.main"
