FROM python:3.8.2

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /usr/src/app
COPY . .

RUN pip install pipenv==2020.6.2 --no-cache-dir && \
    pipenv install

CMD ["sh", "./entrypoint.sh"]
