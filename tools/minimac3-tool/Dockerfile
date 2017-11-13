FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y git make build-essential gcc libboost-all-dev zlib1g-dev

WORKDIR /opt
RUN git clone https://github.com/ohsu-comp-bio/Minimac3.git && \
    cd Minimac3 && \
    make && \
    make install
