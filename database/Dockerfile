FROM postgres:latest

ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=username
ENV POSTGRES_DB=database

COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql
RUN echo "== Created DB.."