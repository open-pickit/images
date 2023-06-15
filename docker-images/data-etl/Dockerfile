FROM python:3

# install aws
RUN pip install awscli
RUN apt-get update
RUN apt-get install -y groff

# install zip
RUN apk add zip

ENTRYPOINT ["/bin/bash"]