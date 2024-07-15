FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y openjdk-11-jdk

COPY ./requirements.txt .

RUN pip install -r requirements.txt --upgrade

WORKDIR /notebooks

CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--NotebookApp.token=''", "--NotebookApp.password=''", "--no-browser", "--allow-root"]