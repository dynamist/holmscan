FROM alpine:latest

WORKDIR /opt/holmscan
COPY setup.py /opt/holmscan/setup.py
COPY *.md /opt/holmscan/
COPY holmscan/ /opt/holmscan/holmscan/

RUN apk update
RUN apk add python3 py3-pip
RUN pip3 install -e .

ENTRYPOINT ["/usr/bin/holmscan"]
CMD ["$1"]

