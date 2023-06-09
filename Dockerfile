FROM python:3.11.2-slim

RUN apt-get -y update

RUN apt-get -y install curl

# To avoid running the application as ROOT,
# we'll create an unpriviledged user that will run the application.
ENV RUNNER=phoenix
ENV APPDIR=/app
ENV PYTHONPATH=${APPDIR}
ENV PATH="${PATH}:${APPDIR}/.local/bin"

# Provisioning new user with home directory and
# granting ownership over their home directory.
RUN groupadd -r ${RUNNER} && \
    useradd -r -g ${RUNNER} -d ${APPDIR} -s /bin/bash ${RUNNER} && \
    mkdir -p ${APPDIR} && \
    chown -R ${RUNNER}:${RUNNER} ${APPDIR}

# From now on the docker commands will run as user ${RUNNER}
# not ROOT.
USER ${RUNNER}
WORKDIR ${APPDIR}

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ${APPDIR}/

CMD ["poetry", "run", "python", "main.py"]
