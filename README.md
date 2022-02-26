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

Run worker server
```bash
python worker.py
```

Run application
```bash
flask run --reload
```