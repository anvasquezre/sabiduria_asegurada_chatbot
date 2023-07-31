FROM python:3.10.12 as base


ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/data_preloader

#COPY --chown=app:app . /src
COPY . /data_preloader
WORKDIR /data_preloader/


FROM base as healthcheck
ENTRYPOINT ["python3", "/data_preloader/health_check.py"]

FROM base as build
ENTRYPOINT ["python3", "/data_preloader/main.py"]

