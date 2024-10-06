FROM python:latest
WORKDIR /myapp
RUN pip install tornado redis
COPY . .
ENV ENVIRONMENT=DEV
ENV HOST=localhost
ENV REDIS_HOST=database
ENV REDIS_PORT=6379
ENV REDIS_DB=0
EXPOSE 8000
CMD [ "python" , "hello.py" ]
