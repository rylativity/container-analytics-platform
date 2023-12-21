FROM python:3.10-bullseye

RUN pip install mlflow && pip cache purge

CMD ["mlflow", "ui", "-h", "0.0.0.0", "-p", "5000"]
