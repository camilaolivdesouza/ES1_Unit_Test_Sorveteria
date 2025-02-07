.PHONY: test run

# Executa os testes com pytest
test:
	pytest --maxfail=1 --disable-warnings -q

# Executa a aplicação 
run:
	python test_sorveteria.py
