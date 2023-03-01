FROM python:3.9-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "migrate", "--fake", "sessions", "zero"]
CMD ["python3","manage.py","migrate"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]


