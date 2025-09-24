types:
	mypy . | mypy-baseline filter

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade head

migrations:
	@if [ -z "$$m" ]; then \
		echo "Error: Migration message is required. Use 'make migrations m=\"Your message\"'"; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$$m"

install-pre-commit:
	pre-commit install -t pre-commit -t commit-msg -t pre-push

style:
	pre-commit run style --all-files
	pre-commit run ruff --all-files

extra_style:
	pre-commit run python-check-blanket-noqa --all-files
	pre-commit run expr-complexity --all-files
	pre-commit run test-naming --all-files
	pre-commit run line-count --all-files
	pre-commit run api-annotated --all-files
	pre-commit run old-style-annotations --all-files

structure:
	@pre-commit run package-structure --all-files

validate-ci:
	make -j$(N_JOBS) style extra_style structure

migrations-check:
	alembic upgrade head;
	alembic downgrade -5;
	while true; do \
  		output=$$(alembic upgrade +1 2>&1 | tee /dev/stderr); \
		if echo "$$output" | grep -q "Relative revision +1 didn't produce 1 migrations"; then \
			echo "SUCCESS: All migrations are backward-compatible."; \
			exit 0; \
		elif echo "$$output" | grep -E -q "Traceback|ERROR|FAILED|raise|exception"; then \
		  	echo "FAILED: Migrations chain have mistakes."; \
		    exit 1; \
		fi; \
		alembic downgrade -1; \
  		output=$$(alembic upgrade +1 2>&1 | tee /dev/stderr); \
		if echo "$$output" | grep -q "Relative revision +1 didn't produce 1 migrations"; then \
			echo "SUCCESS: All migrations are backward-compatible."; \
			exit 0; \
		elif echo "$$output" | grep -E -q "Traceback|ERROR|FAILED|raise|exception"; then \
		  	echo "FAILED: Migrations chain have mistakes."; \
		    exit 1; \
		fi; \
	done

POSTGRES_NAME ?= test

