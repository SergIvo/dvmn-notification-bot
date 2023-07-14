FROM python:3.10-alpine

WORKDIR /notification_bot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]
