FROM python:3

COPY . .

RUN pip install pipenv

RUN pipenv install --three

CMD [ "pipenv", "run", "test" ]
