# Using Ubuntu 20.04
FROM ubuntu:20.04 AS builder-image

# Avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential netcat locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/*/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

# Create and activate virtual environment
# Using final folder name to avoid path issues with packages
RUN python3.9 -m venv /home/link/venv
ENV PATH="/home/link/venv/bin:$PATH"

# Install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:20.04 AS runner-image

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-venv netcat locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN useradd --create-home link
COPY --from=builder-image /home/link/venv /home/link/venv

USER link
RUN mkdir /home/link/code
WORKDIR /home/link/code
COPY /app .

# activate virtual environment
ENV VIRTUAL_ENV=/home/link/venv \
    PATH="/home/link/venv/bin:$PATH" \
    LANG=en_US.utf8

EXPOSE 8000

CMD [ "python3.9", "navi-generate-report.py" ]
