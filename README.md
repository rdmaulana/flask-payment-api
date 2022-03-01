## flask-payment-api

#How to running project locally

Create virtualenv
```bash
python3 -m venv venv && source venv/bin/activate
```

Install Requirements
```bash
pip install -r requirements.txt
```

Create .env file and setup the requirements based on .env.example

Run celery worker
```bash
celery --app app.tasks worker --loglevel=info -E
```

Run celery dashboard (task monitor)
```bash
celery --app app.tasks.celery flower --port=5555 --broker=redis://redis:6379/0
```

Run application
```bash
flask run --reload
```