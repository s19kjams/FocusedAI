FROM python:3.9-slim

WORKDIR /app

COPY ./src/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python3", "-u", "src/main.py"]