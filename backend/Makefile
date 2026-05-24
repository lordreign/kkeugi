.PHONY: help setup db-up db-down db-reset install migrate run test lint fmt clean

help:
	@echo "Kkeugi Backend — Local Dev Commands"
	@echo ""
	@echo "  make setup     — first-time setup (env + db + install + migrate)"
	@echo "  make db-up     — start postgres container"
	@echo "  make db-down   — stop postgres container"
	@echo "  make db-reset  — drop volumes + restart (DESTROYS LOCAL DATA)"
	@echo "  make install   — uv sync dependencies"
	@echo "  make migrate   — alembic upgrade head"
	@echo "  make run       — uvicorn with reload (port 8080)"
	@echo "  make test      — pytest with coverage"
	@echo "  make lint      — ruff check"
	@echo "  make fmt       — ruff format"
	@echo "  make clean     — remove caches"

setup: db-up install migrate
	@echo ""
	@echo "✓ Setup complete. Run 'make run' to start the server."
	@echo "  Docs:   http://localhost:8080/docs"
	@echo "  Health: http://localhost:8080/health"
	@echo ""
	@echo "Quick dev login (no Google OAuth needed):"
	@echo "  curl -X POST http://localhost:8080/v1/auth/dev/login \\"
	@echo "    -H 'Content-Type: application/json' \\"
	@echo "    -d '{\"email\":\"me@test.com\",\"name\":\"Test User\"}'"

db-up:
	@if [ ! -f .env ]; then cp .env.example .env && echo "✓ .env created from .env.example"; fi
	docker compose up -d
	@echo "Waiting for Postgres..."
	@until docker compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do sleep 1; done
	@echo "✓ Postgres ready (port 5432)"

db-down:
	docker compose down

db-reset:
	docker compose down -v
	@$(MAKE) db-up

install:
	uv sync
	@echo "✓ Dependencies installed"

migrate:
	uv run alembic upgrade head
	@echo "✓ Migrations applied"

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

test:
	uv run pytest --cov=app --cov-report=term-missing

lint:
	uv run ruff check app tests

fmt:
	uv run ruff format app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info
