FROM ubuntu:16.04

ENV PBWT_VERSION 3.1
ENV HTSLIB_VERSION 1.3.2


RUN apt-get update  && \
    apt-get install -y build-essential gcc git libboost-all-dev libopenblas-dev liblzma-dev libbz2-dev make wget zlib1g-dev

ENV LD_LIBRARY_PATH /usr/local/lib:/usr/lib

#Install htslib
WORKDIR /opt/
RUN wget https://github.com/samtools/htslib/archive/${HTSLIB_VERSION}.tar.gz -O htslib-${HTSLIB_VERSION}.tar.gz && \
    tar -zxvf htslib-${HTSLIB_VERSION}.tar.gz && \
    mv htslib-${HTSLIB_VERSION} htslib && \
    cd htslib && \
    make && \
    make install
    
#Install pbwt
WORKDIR /opt/
RUN wget https://github.com/VertebrateResequencing/pbwt/archive/v3.1.tar.gz -O pbwt_${PBWT_VERSION}.tar.gz && \
    tar -zxvf pbwt_${PBWT_VERSION}.tar.gz && \ 
    cd pbwt-${PBWT_VERSION} && \ 
    make && \
    cp pbwt /usr/local/bin/

WORKDIR /opt/
ENTRYPOINT ["pbwt"]
