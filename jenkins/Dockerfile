FROM jenkins/jenkins:lts-jdk17

USER root

RUN apt-get update && \
    apt-get install -y \
        curl \
        git \
        docker.io \
        docker-compose-plugin && \
    apt-get clean

USER jenkins