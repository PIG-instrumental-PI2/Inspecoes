install:
	pip install -r requirements.txt

run:
	uvicorn main:app --host 0.0.0.0 --port 8080 --reload

code-formatting:
	black . &&\
	isort .
