FROM python:3

COPY . .

RUN pip install pipenv

RUN pipenv install --three --system --deploy

CMD [ "pipenv", "run", "test" ]
