FROM ubuntu:16.04

RUN apt-get update && \ 
    apt-get install -y build-essential git openjdk-8-jdk python wget

WORKDIR /opt

#Install GATK4
RUN git clone https://github.com/broadinstitute/gatk.git && \ 
    cd gatk && \
     ./gradlew localJar && \
    ln -s /opt/gatk/gatk-launch /usr/local/bin/

# Clone cedar-gwas repo
#RUN git clone https://github.com/ohsu-comp-bio/cedar-gwas.git
#ENV PATH=/opt/cedar-gwas/tools/haplotype-caller-tool:$PATH
ADD run_haplotypecaller.py /usr/local/bin/run_haplotypecaller.py
ENV PATH=/usr/local/bin:$PATH

# Run Haplotype Caller
VOLUME /work
WORKDIR /work
#ENTRYPOINT ["run_haplotypecaller.py"]
