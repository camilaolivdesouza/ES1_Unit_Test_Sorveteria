# Unit tests

import pytest
from Sorveteria import Sorvete, Cozinha, Sorveteria_do_DC

def test_Controle_Estoque():
    sorvetinho = Sorvete("Baunilha", 5.0, 100, estoque_inicial=100)
    sorvetinho.venda(30)
    assert sorvetinho.estoque_atual == 70
    assert not sorvetinho.estoque_baixo()
    sorvetinho.venda(55)
    assert sorvetinho.estoque_atual == 15
    assert sorvetinho.estoque_baixo()
    with pytest.raises(Exception, match="Estoque atual insuficiente"):
        sorvetinho.venda(20)

def test_Preparo_Cozinha():
    ingredientes = {
        'creme': 5,
        'acucar': 5,
        'essencia': {'Baunilha': 3}
    }
    cozinha = Cozinha(capacidade_freezer=2, ingredientes=ingredientes)
    sorvetinho = Sorvete("Baunilha", 5.0, 100, estoque_inicial=10)
    msg = cozinha.prepara_sorvete(sorvetinho)
    assert msg == "Sorvete de Baunilha preparado, estoque atual reestabelecido."
    assert sorvetinho.estoque_atual == 100
    assert ingredientes['creme'] == 4  # 1 unidade consumida
    assert ingredientes['acucar'] == 4
    assert ingredientes['essencia']['Baunilha'] == 2

def test_Capacidade_Freezer():
    ingredientes = {
        'creme': 5,
        'acucar': 5,
        'essencia': {'Chocolate': 3}
    }
    cozinha = Cozinha(capacidade_freezer=1, ingredientes=ingredientes)
    # Simula um job em andamento
    cozinha.sorvete_preparando = 1
    sorvetinho = Sorvete("Chocolate", 6.0, 80, estoque_inicial=10)
    with pytest.raises(Exception, match="Sem freezers disponíveis."):
        cozinha.prepara_sorvete(sorvetinho)
    # Reset
    cozinha.prepara_sorvete = 0

def test_Processar_Pedido():
    # Configura os ingredientes para permitir a preparação
    ingredientes = {
        'creme': 10,
        'acucar': 10,
        'essencia': {'Morango': 5}
    }
    cozinha = Cozinha(capacidade_freezer=2, ingredientes=ingredientes)
    estabelecimento = Sorveteria_do_DC(cozinha)
    morango = Sorvete("Morango", 4.0, 50, estoque_inicial=50)
    estabelecimento.add_sabor(morango)
    
    # Pedido que não deixa o estoque baixo (50 - 20 = 30; 30 >= 20% de 50)
    password = estabelecimento.processar_pedido("Morango", 20, 20 * 4.0)
    assert password.startswith("P")
    assert morango.estoque_atual == 30

    # Pedido que deixa o estoque abaixo de 20% (30 - 25 = 5, que é menor que 10, ou seja, 20% de 50)
    password2 = estabelecimento.processar_pedido("Morango", 25, 25 * 4.0)
    # Após a preparação, o estoque é reposto para o máximo (50)
    assert morango.estoque_atual == 50

def test_Falha_pagamento():
    ingredientes = {
        'creme': 5,
        'acucar': 5,
        'essencia': {'Baunilha': 5}
    }
    cozinha = Cozinha(capacidade_freezer=2, ingredientes=ingredientes)
    estabelecimento = Sorveteria_do_DC(cozinha)
    baunilha = Sorvete("Baunilha", 5.0, 100, estoque_inicial=100)
    estabelecimento.add_sabor(baunilha)
    # Valor de pagamento incorreto: 10 porções deveriam custar 50 (10*5.0)
    with pytest.raises(Exception, match="Valor incorreto"):
        estabelecimento.processar_pedido("Baunilha", 10, 40)
