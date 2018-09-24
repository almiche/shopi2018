FROM ubuntu:bionic

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY Pipfile .
COPY Pipfile.lock  .

RUN apt-get update &&\
    apt-get -y install python3 &&\
    apt-get -y install python3-pip &&\
    pip3 install pipenv &&\
    which python3 &&\ 
    pipenv --python /usr/bin/python3 install --deploy --system
    
CMD ["python3","/repo/controller.py"]