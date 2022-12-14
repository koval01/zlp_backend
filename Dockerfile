FROM python:3.10.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "main:app", "--workers", "8", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]
