FROM python:3.10.3

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python manage.py migrate ; gunicorn -b 0.0.0.0:8000 joinclub.wsgi

