# order.py - Sistema de armazenamento e cálculo da comanda

# Armazena a comanda como um dicionário. 
# CHAVE: nome do item (string)
# VALOR: Dicionário do item (preco, quantidade, desc)
_current_order = {} 

def add_item(nome, preco, quantidade, desc=""):
    """
    Adiciona um item à comanda.
    Se o item já existe, apenas incrementa a quantidade.
    """
    if nome in _current_order:
        # Item já existe: apenas incrementa a quantidade
        _current_order[nome]['quantidade'] += quantidade
    else:
        # Novo item: adiciona o registro completo
        _current_order[nome] = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade,
            'desc': desc
        }

def set_quantity(nome, nova_quantidade):
    """
    Define uma nova quantidade para um item.
    Usado pelos botões +/- na tela da comanda.
    Remove o item se a quantidade for menor ou igual a zero.
    """
    if nome in _current_order:
        if nova_quantidade > 0:
            _current_order[nome]['quantidade'] = nova_quantidade
        else:
            # Remove o item da comanda
            del _current_order[nome]

def get_items():
    """
    Retorna a lista de itens da comanda no formato de tupla (nome, preco, qtd, desc),
    necessário para a exibição na tela de compra.
    """
    return [
        (item['nome'], item['preco'], item['quantidade'], item['desc'])
        for item in _current_order.values()
    ]

def get_total():
    """
    Calcula o valor total da comanda somando (preço * quantidade) de todos os itens.
    """
    total = 0.0
    for item in _current_order.values():
        total += item['preco'] * item['quantidade']
    return total

def clear_order():
    """Limpa toda a comanda."""
    global _current_order
    _current_order = {}