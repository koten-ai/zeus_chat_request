# Optional image: scan catalogs then serve on 3333.
FROM python:3.12-alpine
WORKDIR /srv
COPY . /srv
RUN python scripts/scan_catalogs.py
EXPOSE 3333
CMD ["python", "-m", "http.server", "3333", "--bind", "0.0.0.0"]
