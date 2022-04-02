install:
	pip install -r requirements.txt &&\
	pip install -r requirements-dev.txt

run:
	uvicorn main:app --host 0.0.0.0 --port 8080 --reload

run-debug:
	python -m debugpy --listen 0.0.0.0:5678 -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload

run-test:
	export PIG_INSPECTIONS_DB_HOST=localhost &&\
	export PIG_INSPECTIONS_DB_PORT=27017 &&\
	export PIG_INSPECTIONS_DB_USER=root &&\
	export PIG_INSPECTIONS_DB_PASS=password &&\
	export PIG_INSPECTIONS_DB_NAME=pig-inspections &&\
	pytest tests/

code-formatting:
	black . &&\
	isort .
