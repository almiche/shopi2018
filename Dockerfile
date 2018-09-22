FROM ubuntu:bionic

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY Pipfile .
COPY Pipfile.lock  .

RUN apt-get update &&\
     apt-get -y install python3 &&\
    apt-get -y install python3-pip &&\
    apt-get -y install git &&\
    pip3 install pipenv &&\
    pipenv --python /usr/bin/python3 install --deploy --system  &&\
    git clone https://github.com/almiche/shopi2018 &&\
    apt-get -y purge git

WORKDIR /shopi2018

CMD ["python3","controller.py"]