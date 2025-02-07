# Sorveteria do DC

Este trabalho foi desenvolvido no âmbito da disciplina de Engenharia de Software 1, oferecida pela Universidade Federal de São Carlos. O objetivo do mesmo é forncer entendimento sobre o uso e importancia de Unit Tests. Trata-se de uma aplicação simples em Python para gerenciamento de uma sorveteria, incluindo controle de estoque, processamento de pedidos e acionamento da cozinha para repor o estoque quando necessário.

## Descrição

Este projeto implementa um sistema para gerenciamento de uma sorveteria. O sistema permite:
- **Gerenciar Sorvetes:** Cada sorvete possui sabor, preço por porção, estoque máximo e estoque atual.  
- **Controle de Estoque:** Verifica se o estoque está abaixo de 20% do valor máximo e, se necessário, aciona a cozinha para repor o estoque. 
- **Cozinha:** Responsável pela preparação dos sorvetes. A cozinha possui capacidade de produção (freezers disponíveis) e consome ingredientes (creme, açúcar e essência) para restaurar o estoque.  
- **Processamento de Pedidos:** Valida o pagamento, processa a venda e gera uma senha para o cliente.


## Pré-requisitos

- **Python 3**  
- **pytest** (para rodar os testes)  
- **make** (para utilizar o Makefile; no Windows, recomenda-se usar o Git Bash ou instalar o make via Chocolatey ou MSYS2)

## Executando a Aplicação
Para executar a aplicação, você pode usar o comando: make run
Isso irá executar o arquivo Sorveteria.py. 
Alternativamente, você pode rodar: python Sorveteria.py

# Executando os Testes
Os testes unitários são escritos utilizando o pytest e estão no arquivo test_Sorveteria.py. Para executá-los, use: make test


