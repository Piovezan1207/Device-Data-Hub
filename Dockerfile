FROM python:3.13-alpine

RUN apk add --virtual .build-dependencies \
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            pcre-dev

RUN apk add --no-cache pcre

WORKDIR /app

COPY /app /app
COPY entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /app


ENV APP_KEY=reIKRuG0PjcV40tDzhr5HDbzuUggzr5lFAMnrQsV4mM=
ENV DEBUG=1


RUN pip install -r /app/requirements.txt

RUN apk del .build-dependencies && rm -rf /var/cache/apk/*

# Dá permissão de execução ao entrypoint
RUN chmod +x /entrypoint.sh

# Define o volume onde o banco será armazenado
VOLUME /app/infra/database

# Define o entrypoint
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 5000

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]
