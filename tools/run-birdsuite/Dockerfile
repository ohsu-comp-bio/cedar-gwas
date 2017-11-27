FROM alliecreason/birdsuite:hg38

RUN apt-get update

# Clone repo
WORKDIR /opt
RUN git clone https://github.com/ohsu-comp-bio/cedar-gwas.git
ENV PATH=/opt/cedar-gwas/scripts:$PATH
 
# Run birdsuite
VOLUME /inputs
VOLUME /work
WORKDIR /work
ENTRYPOINT ["run_birdsuite.py"]
