FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PORT=8080
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY game.py app.py ./
COPY static ./static
CMD gunicorn -b 0.0.0.0:$PORT --workers 2 app:app
