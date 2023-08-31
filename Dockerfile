FROM python:3.11

RUN mkdir /uahexchangeapi

WORKDIR /uahexchangeapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .



WORKDIR src

CMD gunicorn app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000