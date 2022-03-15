FROM docker.io/bellsoft/liberica-openjdk-alpine:8u322
WORKDIR /app
VOLUME /output
ADD https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar buildtools.jar

RUN apk update && apk add git

ENTRYPOINT ["java", "-jar", "/app/buildtools.jar", "--output-dir", "/output", "--rev"]