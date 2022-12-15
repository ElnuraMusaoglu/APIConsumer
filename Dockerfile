FROM python:3.10.9

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
COPY requirements.txt .
RUN pip install -r /usr/app/requirements.txt

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

