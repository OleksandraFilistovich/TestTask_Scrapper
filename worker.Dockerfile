FROM python:3.10-slim as worker
WORKDIR /worker

COPY . .

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN playwright install && \
    playwright install-deps

RUN echo "= Installed dependencies for worker ="

CMD sh -c "sleep 5 && python -m m_worker"