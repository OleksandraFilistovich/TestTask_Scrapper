FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install pipenv

RUN pipenv install --system --ignore-pipfile

RUN echo "Installed dependencies.."

CMD ["python","-u","scrapper.py"]
RUN echo "Code run done."