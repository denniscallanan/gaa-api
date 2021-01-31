FROM python:3.9.1-alpine3.12

RUN apk update && \
 	apk upgrade && \
    apk add --virtual build-deps gcc python3-dev musl-dev libc-dev libffi-dev libxslt-dev openssl-dev postgresql-libs postgresql-dev

ADD src/requirements.txt /usr/app/src/requirements.txt
ADD src/dev-requirements.txt /usr/app/src/dev-requirements.txt

RUN pip3 install -r /usr/app/src/requirements.txt
RUN pip3 install -r /usr/app/src/dev-requirements.txt

ADD src /usr/app/src
ADD tests /usr/app/tests
ADD .pylintrc /usr/app/.pylintrc
ADD *.py /usr/app/

WORKDIR /usr/app/
ENTRYPOINT ["python"]
CMD ["run_server.py"]
