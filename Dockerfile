FROM python:2.7.13

ADD . /code
WORKDIR /code

RUN pip install Flask MySQL-python PyMySQL

CMD ["python", "app.py"]