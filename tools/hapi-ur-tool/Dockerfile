FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y git gcc g++ libboost-dev make

WORKDIR /opt

RUN git clone https://github.com/ohsu-comp-bio/hapi-ur.git && \
    cd hapi-ur && \
    make && \
    cp src/hapi-ur /usr/local/bin && \
    cp src/vote-phase /usr/local/bin
