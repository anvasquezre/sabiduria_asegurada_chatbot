FROM python:3.10.11 as base


ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

ENV PYTHONPATH=$PYTHONPATH:/src

#COPY --chown=app:app . /src
COPY . /data_preloader
WORKDIR /data_preloader/src


FROM base as healthcheck
ENTRYPOINT ["python3", "/data_preloader/src/health_check.py"]

FROM base as build
ENTRYPOINT ["python3", "/data_preloader/src/main.py"]

