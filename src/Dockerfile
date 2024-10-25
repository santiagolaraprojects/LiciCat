FROM python:3.11.2-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /code


COPY ./requirements.txt .
COPY ./.env .
RUN pip install -r requirements.txt

COPY . .
