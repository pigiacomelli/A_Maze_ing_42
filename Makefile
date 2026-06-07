install:
	pip install -r requirements.txt

run:
	PYTHONPATH=src python3 a_maze_ing.py config.txt

debug:
	PYTHONPATH=src python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache dist build *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

validate-output:
	python3 tools/output_validator.py maze.txt
