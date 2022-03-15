FROM docker.io/bellsoft/liberica-openjdk-alpine:16.0.2-7
WORKDIR /app
VOLUME /output
ADD https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar buildtools.jar

ENTRYPOINT ["java", "-jar", "/app/buildtools.jar", "--output-dir", "/output", "--rev"]