FROM ubuntu:20.04 as python-build
SHELL ["/bin/bash", "-c"]
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y software-properties-common gcc apt-transport-https && \
    add-apt-repository -y ppa:deadsnakes/ppa &&  \
    apt-get install -y cmake z3 python3.10 python3-distutils python3-pip python3-apt python3.10-venv  \
    openjdk-8-jdk git maven wget && \
    DEBIAN_FRONTEND=noninteractive  \
    apt-get install -y --no-install-recommends --assume-yes build-essential libpq-dev unzip libcairo2-dev pkg-config python3.10-dev
RUN apt-get update && apt-get install -y nodejs npm
RUN apt-get update && apt-get install -y libcairo2-dev pkg-config python3.10-dev

FROM python-build AS ecstatic-build

WORKDIR /
RUN python3.10 -m venv /venv
ENV PATH=/venv/bin:$PATH
ADD . /ND_Detector
RUN mv /ND_Detector /ECSTATIC
WORKDIR ECSTATIC
RUN source /venv/bin/activate
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install -e .
