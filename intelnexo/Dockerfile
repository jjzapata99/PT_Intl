FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

EXPOSE 8000

#CMD ["gunicorn", "main:app", "--workers","5","--timeout","99990","--worker-class","uvicorn.workers.UvicornWorker", "--bind","0.0.0.0:8000"]
CMD ["uvicorn", "main:app", "--reload", "--env-file",".env", "--host", "0.0.0.0", "--port","8000"]