FROM python:3.10.6-slim as base

# Some environment vars modifiers for Python
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=1

# Due to problems with the signature of the repos for ttf-msconrefonts we have to update twice
# and add the signature of the servers
RUN apt-get update --fix-missing --no-install-recommends && \
    apt-get install -y --no-install-recommends \
    # dependencies for compiling python libraries
    build-essential && \
    # And clean up
    apt-get autoremove -yqq --purge && \
    apt-get clean &&  \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/*


WORKDIR /src
COPY api/requirements.txt /src/api/requirements.txt
COPY tests/requirements.txt /src/tests/requirements.txt

RUN pip install --no-cache-dir \
                -r /src/api/requirements.txt \
                -r /src/tests/requirements.txt

COPY api /src/api
COPY tests /src/tests

# Install packages
RUN pip install --no-cache-dir \
                -e /src/api

WORKDIR /src
