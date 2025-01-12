FROM ubuntu:20.04 as nondex-build

## package update
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends apt-utils git maven wget gnupg

RUN wget -q -O - "https://download.bell-sw.com/pki/GPG-KEY-bellsoft" | apt-key add -
RUN echo "deb [arch=amd64] https://apt.bell-sw.com/ stable main" | tee /etc/apt/sources.list.d/bellsoft.list
RUN apt-get update && apt-get -y install bellsoft-java8-full

# Build nondex
WORKDIR /
RUN wget https://github.com/TestingResearchIllinois/NonDex/archive/refs/tags/nondex-2.1.1.tar.gz -O /nondex.tar.gz
RUN mkdir /nondex
RUN tar -xzf /nondex.tar.gz -C /nondex --strip-components=1
WORKDIR /nondex
ENV JAVA_HOME=/lib/jvm/bellsoft-java8-full-amd64
RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/bellsoft-java8-full-amd64/jre/bin/java 9999
RUN mvn clean compile package -e -DskipTests
RUN mv /nondex/nondex-common/target/nondex-common*.jar /nondex/nondex-common/target/nondex-common.jar
RUN java -jar /nondex/nondex-instrumentation/target/nondex-instrumentation*jar /nondex-rt.jar
WORKDIR /


FROM ecstatic/base-image

USER root
RUN wget -q -O - "https://download.bell-sw.com/pki/GPG-KEY-bellsoft" | apt-key add -
RUN echo "deb [arch=amd64] https://apt.bell-sw.com/ stable main" | tee /etc/apt/sources.list.d/bellsoft.list
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install git ant bellsoft-java8-full android-sdk

ENV JAVA_HOME=/lib/jvm/bellsoft-java8-full-amd64

WORKDIR /
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-8092744_latest.zip && \
    unzip commandlinetools-linux-8092744_latest.zip && \
    cd cmdline-tools && \
    yes | ./bin/sdkmanager --sdk_root=/lib/android-sdk --update && \
    ./bin/sdkmanager --sdk_root=/lib/android-sdk --install "platforms;android-25"
WORKDIR /
ENV ANDROID_SDK_HOME=/lib/android-sdk
ENV ANDROID_SDK_ROOT=/lib/android-sdk

WORKDIR /
RUN git clone https://github.com/AnnabellaM/amandroid.git && \
    cd amandroid && mkdir out
RUN ln -s /amandroid /root

WORKDIR /
RUN java -jar /amandroid/argus-saf-3.2.1-SNAPSHOT-assembly.jar t /amandroid/ActivityCommunication1.apk -o /amandroid/out
WORKDIR /


COPY --from=nondex-build /nondex /nondex
COPY --from=nondex-build /nondex-rt.jar /nondex-rt.jar
