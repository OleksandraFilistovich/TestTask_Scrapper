#FROM postgres:latest as base

#ENV POSTGRES_PASSWORD=password
#ENV POSTGRES_USER=username
#ENV POSTGRES_DB=database

#COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql
#RUN echo "== Created DB.."


FROM python:3.10-slim as orchestrator
WORKDIR /orchestrator

COPY . .

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN echo "= Installed dependencies for orchestrator ="

#CMD ["python", "-u", "utils/rs.py"]
CMD sh -c "sleep 5 && python -m m_orchestrator"


