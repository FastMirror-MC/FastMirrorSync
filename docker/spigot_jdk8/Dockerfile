FROM docker.io/bellsoft/liberica-openjdk-alpine:8u322
WORKDIR /workspace
VOLUME /workspace
COPY spigot_jdk8/info.py /workspace/info.py
COPY sync.py /workspace/sync.py
# download spigot buildtool
ADD https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar buildtools.jar

RUN cd /workspace \
# install git and python
&& apk add git \
&& apk add python3 \
# install requests and pytz
&& wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py \
&& python3 get-pip.py \
&& pip3 install requests \
&& pip3 install pytz

CMD [ "python3", "/workspace/sync.py" ]
