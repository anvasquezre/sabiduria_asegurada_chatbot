FROM python:3.10.12 as base


ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

#COPY --chown=app:app . /src
COPY . /app
WORKDIR /app/

EXPOSE 8000

FROM base as build
ENTRYPOINT ["chainlit","run","app.py","-w"]

