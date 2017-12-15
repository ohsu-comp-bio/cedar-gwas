FROM ubuntu:16.06

RUN apt-get update && \ 
    apt-get install -y build-essential git openjdk-8-jdk python wget

WORKDIR /opt

#Install GATK4
RUN git clone https://github.com/broadinstitute/gatk.git 
    cd gatk && \
     ./gradlew localJar

# Clone repo
RUN git clone https://github.com/ohsu-comp-bio/cedar-gwas.git
ENV PATH=/opt/cedar-gwas/tools/haplotype-caller-tool:$PATH
 
# Run Haplotype Caller
VOLUME /work
WORKDIR /work
ENTRYPOINT ["run_haplotypecaller.py"]
