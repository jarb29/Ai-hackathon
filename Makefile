# Web Audit Agent - Development Makefile

.PHONY: help venv install run stop clean test docker-build docker-up docker-down docker-clean docker-logs

# Default target
help:
	@echo "Available commands:"
	@echo "  make venv         - Create virtual environment"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Start the application"
	@echo "  make stop         - Kill processes on port 9000"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make test         - Run tests (if available)"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make docker-clean - Remove containers and images"
	@echo "  make docker-logs  - Show container logs"

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv .venv1
	@echo "✓ Virtual environment created"
	@echo "Activate with: source .venv1/bin/activate"

# Install dependencies
install:
	@if [ ! -d ".venv1" ]; then \
		echo "Virtual environment not found. Creating..."; \
		make venv; \
	fi
	@echo "Installing dependencies..."
	.venv1/bin/pip install --upgrade pip
	.venv1/bin/pip install -r requirements.txt
	@echo "✓ Dependencies installed"

# Start the application
run:
	@if [ ! -d ".venv1" ]; then \
		echo "Setting up environment..."; \
		make install; \
	fi
	@echo "Starting Web Audit Agent..."
	@PYTHONPATH=. .venv1/bin/python src/app/main.py

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf __pycache__ .pytest_cache *.pyc
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "✓ Cleaned"

# Stop application (kill processes on port 9000)
stop:
	@echo "Stopping Web Audit Agent..."
	@lsof -ti:9000 | xargs kill -9 2>/dev/null || echo "No processes found on port 9000"
	@echo "✓ Stopped"

# Run tests
test:
	@echo "Running tests..."
	@if [ -d "tests" ]; then \
		.venv1/bin/python -m pytest tests/; \
	else \
		echo "No tests directory found"; \
	fi

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker-compose -f docker-compose.dev.yml build
	@echo "✓ Docker images built"

docker-up:
	@echo "Starting Docker containers..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✓ Containers started"
	@echo "API: http://localhost:9000"
	@echo "MCP: http://localhost:3001"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose -f docker-compose.dev.yml down
	@echo "✓ Containers stopped"

docker-clean:
	@echo "Cleaning Docker containers and images..."
	docker-compose -f docker-compose.dev.yml down
	docker rmi aihackanton-web-audit-api aihackanton-chrome-mcp 2>/dev/null || true
	@echo "✓ Cleaned"

docker-logs:
	@echo "Showing container logs..."
	docker-compose -f docker-compose.dev.yml logs -f