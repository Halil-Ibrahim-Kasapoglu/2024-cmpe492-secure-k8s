# Docker file for flask backend
FROM python:3.8-slim

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD ["python", "app.py"]