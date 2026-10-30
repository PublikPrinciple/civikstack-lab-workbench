FROM python:3.12-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends git curl ca-certificates openssh-client procps && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --shell /bin/bash --uid 1000 coder
USER coder
WORKDIR /home/coder
