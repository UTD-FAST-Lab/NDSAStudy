FROM ubuntu:20.04 as opal-build
SHELL ["/bin/bash", "-c"]

USER root

## timezone \
RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

## package update
RUN apt-get update && apt-get upgrade -y && apt-get install -y apt-utils git openjdk-11-jdk maven


WORKDIR /
RUN git clone https://github.com/UTD-FAST-Lab/OPALInterface.git
WORKDIR /OPALInterface
RUN git pull 
RUN mvn compile package
WORKDIR /

FROM ecstatic/base-image

COPY --from=opal-build /OPALInterface /OPALInterface
