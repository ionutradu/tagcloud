FROM python:2-onbuild
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
