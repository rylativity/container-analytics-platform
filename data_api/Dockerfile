FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY * ./
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0"]