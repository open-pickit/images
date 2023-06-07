FROM python:3

# install aws
RUN pip install awscli
RUN apt-get update
RUN apt-get install -y groff

COPY pipe.py pipe.py
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt 

ENTRYPOINT ["python3", "pipe.py"]