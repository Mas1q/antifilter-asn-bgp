FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

LABEL maintainer="Dmitry Chistyakov <dk@k4f.ru>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 179

CMD ["python", "app.py"]