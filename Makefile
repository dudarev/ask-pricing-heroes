requirements:
	pip install pip-tools
	pip-compile requirements.in --resolver=backtracking -o requirements.txt --verbose

requirements-upgrade:
	pip install pip-tools
	pip-compile requirements.in --upgrade --resolver=backtracking -o requirements.txt --verbose

install:
	pip install pip-tools
	pip-sync requirements.txt

run:
	streamlit run src/app.py

embeddings:
	python src/embeddings.py