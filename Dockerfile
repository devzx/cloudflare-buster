FROM alpine:3.7
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

COPY ./src /src

RUN pip3 install -r /src/requirements.txt

ENV PYTHONPATH=/ \
    SECRET_KEY= \
    CF_API_EMAIL= \
    CF_API_KEY=

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--config", "/src/gunicorn.py", "--chdir", "/src", "run:app"]
