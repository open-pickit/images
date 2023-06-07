FROM python:3

# install aws
RUN pip install awscli
RUN apt-get update
RUN apt-get install -y groff

COPY docker-images/bitbucket-build/pipe.py requirements.txt 
RUN pip install -r requirements.txt 

ENTRYPOINT ["python3", "pipe.py"]