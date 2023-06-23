FROM python:3.8-slim

# set work directory
WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc 
# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .
RUN ls -l app
RUN ls -l
RUN ls / -l