FROM python:3.8-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./lkweb/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./lkweb /app

EXPOSE 5000

#CMD ["python", "app.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "-t", "2400", "wsgi:app"]