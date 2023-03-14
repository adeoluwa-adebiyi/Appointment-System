FROM python:3.11

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python","manage.py", "runserver"]