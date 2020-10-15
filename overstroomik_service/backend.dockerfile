FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR .

RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r requirements_dev.txt ; else pip install -r requirements.txt ; fi"

COPY . /app
ENV PYTHONPATH=/app
