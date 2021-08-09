FROM python:3.9.6-alpine3.14

WORKDIR /usr/src/app

COPY . .

CMD ["python", "-m", "test_jw_dius_shopping"]