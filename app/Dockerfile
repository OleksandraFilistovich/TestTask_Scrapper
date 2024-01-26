FROM python:3.10-slim
WORKDIR /code

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN echo "= Installed dependencies ="

COPY . .
CMD ["python", "-u", "app.py"]
