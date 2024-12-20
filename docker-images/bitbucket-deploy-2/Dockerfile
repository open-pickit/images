FROM python:3

# install aws
RUN pip install awscli
RUN apt-get update
RUN apt-get install -y groff docker-buildx-plugin

# install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /bin/kubectl

WORKDIR /

COPY pipe.py /pipe.py
COPY requirements.txt /requirements.txt 
RUN pip install -r requirements.txt 

ENTRYPOINT ["python3", "/pipe.py"]