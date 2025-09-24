FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y make ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy

COPY . /code/
EXPOSE 8000
