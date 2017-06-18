FROM jupyter/base-notebook

WORKDIR /home/jovyan/work
COPY requirements.txt /home/jovyan/work
RUN pip install -r requirements.txt
