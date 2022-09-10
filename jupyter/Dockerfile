FROM python:3

RUN apt-get update && apt-get install -y openjdk-11-jdk &&\
    pip install jupyterlab

COPY ./requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /notebooks

CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--NotebookApp.token=''", "--NotebookApp.password=''", "--no-browser", "--allow-root"]