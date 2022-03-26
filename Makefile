install:
	pip install -r requirements.txt &&\
	pip install -r requirements-dev.txt

run:
	uvicorn main:app --host 0.0.0.0 --port 8080 --reload

run-debug:
	python -m debugpy --listen 0.0.0.0:5678 -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload

code-formatting:
	black . &&\
	isort .
