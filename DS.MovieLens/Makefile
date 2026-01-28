.PHONY: all format check lint check-all test test-cov test-html j

CHECK_SRC = src tests

all: test-cov

format:
	@echo "💅 Formatting and sorting imports with Ruff..."
	uv run ruff check --select I --fix $(CHECK_SRC)
	uv run ruff format $(CHECK_SRC)

check:
	@echo "🔍 Linting code with Ruff..."
	uv run ruff check $(CHECK_SRC) --fix
	@echo

lint:
	@echo "🧠 Running deep code analysis with Pylint..."
	uv run pylint $(CHECK_SRC)

check-all: format lint
	@echo "✅ Code quality checks passed!"
	@echo

test: check-all
	@echo "🧪 Running tests..."
	uv run pytest -v --no-header

test-cov: check-all
	@echo "📊 Generating test coverage report..."
	uv run pytest -v --no-header --cov

test-html: check-all
	@echo "📊 Generating HTML test coverage report..."
	uv run pytest -v --no-header --cov --cov-report=html
	@echo
	@echo "📄 See coverage report in htmlcov/index.html"

j: check
	@echo "📓 Запуск Jupyter Notebook..."
	@echo "   Откроется в браузере. Работайте в src/movielens_report.ipynb"
	@echo ""
	uv run jupyter notebook