.PHONY: test run

# Executa os testes com pytest
test:
	pytest --maxfail=1 --disable-warnings -q

# Executa a aplicação (demonstra um exemplo de uso)
run:
	python test_sorveteria.py
