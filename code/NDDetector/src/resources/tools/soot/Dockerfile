FROM ubuntu:20.04 as soot-build
SHELL ["/bin/bash", "-c"]

USER root

## timezone \
RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

## package update
RUN  apt-get install -y --no-install-recommends openjdk-8-jdk && \
     apt-get install -y --no-install-recommends apt-utils git maven wget

# Build Soot
WORKDIR /
RUN git clone https://github.com/ICSE2025/SootInterface.git --depth 1
WORKDIR /SootInterface
RUN git pull 
RUN mvn compile package
WORKDIR /

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

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java 9999
COPY --from=soot-build /SootInterface /SootInterface
COPY --from=soot-build /nondex /nondex
COPY --from=soot-build /nondex-rt.jar /nondex-rt.jar