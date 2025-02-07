# Aplicação para o gerenciamento de uma sorveteria
# Camila Oliveira de Souza, 800361

class Sorvete:
    def __init__(self, sabor, preco, estoque_max, estoque_inicial=None):
        # Inicializa um sorvete com sabor, preço por porção, estoque total, estoque_inicial
        self.sabor = sabor
        self.preco = preco
        self.estoque_max = estoque_max
        self.estoque_atual = estoque_inicial if estoque_inicial is not None else estoque_max
        self.preparando = False

    def venda(self, quantidade):
        # Verifica se o estoque é suficiente para a venda
        if quantidade > self.estoque_atual:
            raise Exception("Estoque atual insuficiente")
        self.estoque_atual -= quantidade

    def estoque_baixo(self):
        # Estoque baixo = resta apenas 20% ou menos do estoque máximo
        return self.estoque_atual < 0.2 * self.estoque_max

    def restaura_estoque(self):
        self.estoque_atual = self.estoque_max

    def em_preparo(self):
        self.preparando = True

    def preparo_finalizado(self):
        self.preparando = False

    def __repr__(self):
        return f"<Sorvete {self.sabor}: {self.estoque_atual}/{self.estoque_max}>"

class Cozinha:
    def __init__(self, capacidade_freezer, ingredientes):
        # O importante para a cozinha é controlar a capacidade para fabricar sorvetes
        self.freezers = capacidade_freezer
        self.sorvete_preparando = 0
        self.ingredientes = ingredientes

    def prepara_sorvete(self, sorvetinho):
        # Prepara um novo lote do sorvete informado, se houver freezers disponíveis e ingredientes suficientes. 
        # Durante a produção, consome 1 unidade de creme, 1 de açúcar e 1 da essência do sabor.
        # Ao final, o estoque do sorvete é reposto para o máximo.
    
        if self.sorvete_preparando >= self.freezers:
            raise Exception("Sem freezers disponíveis.")
        if self.ingredientes.get('creme', 0) < 1:
            raise Exception("Sem creme!")
        if self.ingredientes.get('acucar', 0) < 1:
            raise Exception("Sem açúcar!")
        if self.ingredientes.get('essencia', {}).get(sorvetinho.sabor, 0) < 1:
            raise Exception(f"Sem essencia para o sabor: {sorvetinho.sabor}")

        # Consome os ingredientes
        self.ingredientes['creme'] -= 1
        self.ingredientes['acucar'] -= 1
        self.ingredientes['essencia'][sorvetinho.sabor] -= 1

        self.sorvete_preparando += 1
        sorvetinho.em_preparo()
        # Simula a produção: repõe o estoque para o valor máximo
        sorvetinho.estoque_atual = sorvetinho.estoque_max
        sorvetinho.preparo_finalizado()
        self.sorvete_preparando -= 1
        return f"Sorvete de {sorvetinho.sabor} preparado, estoque atual reestabelecido."

class Sorveteria_do_DC:
    def __init__(self, Cozinha):
        # Inicializa a sorveteria com a cozinha, um dicionário para os sorvetes e o contador de senhas
        self.sorvetes = {}  # chave: sabor, valor: instância de 'Sorvete'
        self.Cozinha = Cozinha
        self.senha_counter = 0

    def add_sabor(self, sorvetinho):
        self.sorvetes[sorvetinho.sabor] = sorvetinho

    def gerar_senha(self):
        self.senha_counter += 1
        return f"P{self.senha_counter:04d}"

    def processar_pedido(self, sabor, quantidade, valor_pago):
        # Processa o pedido de um cliente para um determinado sabor e quantidade:
        # Verifica se o sabor está disponível
        # Calcula o preço total e confere o valor do pagamento
        # Efetua a venda (reduz o estoque)
        # Gera uma senha para o cliente
        # Aciona a cozinha se o estoque ficar abaixo de 20% do máximo e o sorvete não estiver em preparação

        if sabor not in self.sorvetes:
            raise Exception("Este sabor não está disponível.")
        sorvetinho = self.sorvetes[sabor]
        total_preco = sorvetinho.preco * quantidade
        if valor_pago != total_preco:
            raise Exception("Valor incorreto") # Apenas para simplificar, preferi não incluir a opção de troco
        if quantidade > sorvetinho.estoque_atual:
            raise Exception("Sem estoque para esse pedido")

        # Efetua a venda
        sorvetinho.venda(quantidade)

        # Verifica se o estoque ficou baixo e aciona a cozinha, se necessário
        if sorvetinho.estoque_baixo() and not sorvetinho.preparando:
            self.Cozinha.prepara_sorvete(sorvetinho)
        
        senha = self.gerar_senha()
        return senha

# Execução:
if __name__ == "__main__":
    # Define o estoque de ingredientes da cozinha
    ingredientes = {
        'creme': 10,
        'acucar': 10,
        'essencia': {
            'Baunilha': 5,
            'Chocolate': 5,
            'Morango': 5
        }
    }
    Cozinha = Cozinha(capacidade_freezer=2, ingredientes=ingredientes)
    estabelecimento = Sorveteria_do_DC(Cozinha)
    
    # Adiciona alguns sabores
    baunilha = Sorvete("Baunilha", 5.0, 100)
    chocolate = Sorvete("Chocolate", 6.0, 80)
    estabelecimento.add_sabor(baunilha)
    estabelecimento.add_sabor(chocolate)
    
    # Processa um pedido de 5 porções de sorvete de Baunilha (100 - 5 = 95, que é acima de 20% de 100)
    try:
        print("Processando pedido de 5 porções de Baunilha...")
        senha = estabelecimento.processar_pedido("Baunilha", 5, 5 * 5.0)
        print("Pedido processado. Senha para o cliente:", senha)
        print("Estoque atual de Baunilha:", baunilha.estoque_atual) # O retorno será 95
    except Exception as e:
        print("Falha no pedido:", str(e))

        # Processa um pedido de mais 25 porções de sorvete de Baunilha (100 - 5 - 25 = 70)
    try:
        print("Processando pedido de 85 porções de Baunilha...")
        senha = estabelecimento.processar_pedido("Baunilha", 25, 25 * 5.0)
        print("Pedido processado. Senha para o cliente:", senha)
        print("Estoque atual de Baunilha:", baunilha.estoque_atual) # O retorno será 70
    except Exception as e:
        print("Falha no pedido:", str(e))
    
        # Processa um pedido de 60 porções de sorvete de Baunilha (100 - 30 -55 = 15, que é abaixo de 20% de 100)
    try:
        print("Processando pedido de 85 porções de Baunilha...")
        senha = estabelecimento.processar_pedido("Baunilha", 60, 60 * 5.0)
        print("Pedido processado. Senha para o cliente:", senha)
        print("Estoque atual de Baunilha:", baunilha.estoque_atual) # O retorno será 100 pois o estoque teve que ser restaurado 
    except Exception as e:
        print("Falha no pedido:", str(e))
