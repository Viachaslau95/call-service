FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y make

WORKDIR /code/
COPY Pipfile /code/
COPY Pipfile.lock /code/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . /code/
EXPOSE 8000
