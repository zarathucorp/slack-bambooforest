FROM python:3.10-alpine
EXPOSE 3000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
COPY ./src /app/src
COPY .env /app

RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "src/app.py"] 