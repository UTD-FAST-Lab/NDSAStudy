FROM ubuntu:20.04 as nondex-build

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y &&\
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

## package update
RUN  apt-get install -y --no-install-recommends openjdk-8-jdk && \
     apt-get install -y --no-install-recommends apt-utils git maven wget gnupg



# Build nondex
WORKDIR /
RUN wget https://github.com/TestingResearchIllinois/NonDex/archive/refs/tags/nondex-2.1.1.tar.gz -O /nondex.tar.gz
RUN mkdir /nondex
RUN tar -xzf /nondex.tar.gz -C /nondex --strip-components=1
WORKDIR /nondex
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java 9999
RUN mvn clean compile package -e -DskipTests
RUN mv /nondex/nondex-common/target/nondex-common*.jar /nondex/nondex-common/target/nondex-common.jar
RUN java -jar /nondex/nondex-instrumentation/target/nondex-instrumentation*jar /nondex-rt.jar
WORKDIR /




FROM ecstatic/base-image

USER root

RUN apt-get -y update && apt-get -y install openjdk-8-jdk git ant nodejs npm

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java 9999

WORKDIR /
RUN git clone https://github.com/egsch/TAJS.git
WORKDIR /TAJS/
RUN git submodule update --init --recursive && ant
WORKDIR /

COPY --from=nondex-build /nondex /nondex
COPY --from=nondex-build /nondex-rt.jar /nondex-rt.jar
