FROM python:3.10.11 as base


ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

ENV PYTHONPATH=$PYTHONPATH:/src

#COPY --chown=app:app . /src
COPY . /sentiment_service
WORKDIR /sentiment_service/src


# FROM base as test
# RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["python3", "/sentiment_service/src/main.py"]

