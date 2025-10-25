.PHONY: start stop clean restart test health

# Start the server
start:
	@echo "🚀 Starting Web Audit Agent..."
	@lsof -ti:9000 | xargs kill -9 2>/dev/null || true
	@export PYTHONPATH=.:src && python3 src/app/main.py

# Stop the server
stop:
	@echo "🛑 Stopping Web Audit Agent..."
	@lsof -ti:9000 | xargs kill -9 2>/dev/null || true
	@echo "✅ Server stopped"

# Clean up processes and cache
clean:
	@echo "🧹 Cleaning up..."
	@lsof -ti:9000 | xargs kill -9 2>/dev/null || true
	@rm -rf __pycache__
	@rm -rf src/__pycache__
	@rm -rf .pytest_cache
	@find . -name "*.pyc" -delete
	@echo "✅ Cleanup complete"

# Restart the server
restart: stop start

# Test the server
test:
	@echo "🔍 Testing server..."
	@curl -s http://localhost:9000/health || echo "❌ Server not responding"

# Check server health
health:
	@curl -s http://localhost:9000/health | python3 -m json.tool