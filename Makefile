.PHONY: help install run stop clean docker-up docker-down docker-clean docker-logs docker-fix

help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  run          - Start application"
	@echo "  stop         - Stop application"
	@echo "  clean        - Clean build artifacts"
	@echo "  docker-up    - Build and start containers"
	@echo "  docker-down  - Stop containers"
	@echo "  docker-clean - Remove containers and images"
	@echo "  docker-logs  - Show container logs"
	@echo "  docker-fix   - Fix Docker issues"

install:
	@[ ! -d ".venv1" ] && python3 -m venv .venv1 || true
	@.venv1/bin/pip install --upgrade pip -q
	@.venv1/bin/pip install -r requirements.txt -q
	@echo "✓ Dependencies installed"

run:
	@[ ! -d ".venv1" ] && make install || true
	@PYTHONPATH=. .venv1/bin/python src/app/main.py

stop:
	@lsof -ti:9000 | xargs kill -9 2>/dev/null || echo "No processes on port 9000"

clean:
	@rm -rf __pycache__ .pytest_cache *.pyc
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "__pycache__" -delete 2>/dev/null || true
	@echo "✓ Cleaned"

docker-up:
	@docker-compose -f docker-compose.dev.yml up -d --build
	@echo "✓ Running at http://localhost:9000"

docker-down:
	@docker-compose -f docker-compose.dev.yml down

docker-clean:
	@docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans 2>/dev/null || true
	@docker rmi ai-hackathon-web-audit-api ai-hackathon-chrome-mcp 2>/dev/null || true
	@docker system prune -f --volumes 2>/dev/null || true
	@echo "✓ Cleaned"

docker-logs:
	@docker-compose -f docker-compose.dev.yml logs -f

docker-fix:
	@docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans 2>/dev/null || true
	@docker system prune -af --volumes 2>/dev/null || true
	@make docker-up