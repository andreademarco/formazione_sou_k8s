# syntax=docker/dockerfile:1.4

# Crea immagine chiamata builder e basata su python 3.10-apline
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

# Imposta directory di lavoro
WORKDIR /app

# Copia il file con le dipendenze Python nel container
COPY requirements.txt /app

# Installa le dipendenze elencate e usa una cache montata per evitare di riscaricare i pacchetti ogni volta (?)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
# Copia tutto il codice e lo script  ella directory del container
COPY . /app

# Quando il container parte esegue lo script che stampa hello world
ENTRYPOINT ["python3"]
CMD ["app.py"]

