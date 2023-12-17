FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

COPY ./monitoring ./monitoring

COPY ./test ./test

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]