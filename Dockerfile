FROM --platform=linux/amd64 python:3.7
EXPOSE 8080/tcp
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]