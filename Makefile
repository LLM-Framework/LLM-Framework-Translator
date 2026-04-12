.PHONY: run build test docker-run docker-build clean lint

# Run locally
run:
	uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# Run with Docker
docker-build:
	docker build -t llm-translator .

docker-run:
	docker run -p 8001:8001 --env-file .env llm-translator

docker-compose-up:
	docker-compose up

# Testing
test:
	pytest tests/ -v --cov=src --cov-report=html

test-watch:
	pytest-watch -- -v

# Linting
lint:
	ruff check src/
	black --check src/

format:
	black src/

# Clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Load testing with Locust
load-test:
	locust -f scripts/load_test.py --host=http://localhost:8001