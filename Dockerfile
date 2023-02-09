FROM python:3.11-slim-buster

RUN mkdir /app
WORKDIR /app

ENV LISTEN_PORT=5000
EXPOSE 5000

ADD requirements.txt /app
ADD models.py /app

RUN pip install -r /app/requirements.txt
COPY . /app

# ENTRYPOINT [ "python" ]

CMD ["python", "models.py" ]