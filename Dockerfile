FROM python:2.7.13

ADD . /code
WORKDIR /code

RUN pip install Flask MySQL-python PyMySQL --proxy=http://emea-proxy.uk.oracle.com:80

CMD ["python", "app.py"]