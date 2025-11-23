# order.py
# Sistema simples de armazenamento da comanda

comanda = []  # lista de pedidos

def add_item(nome, preco, quantidade, desc=""):
    """Adiciona um item à comanda"""
    item = {
        "nome": nome,
        "preco": preco,
        "quantidade": quantidade,
        "desc": desc
    }
    comanda.append(item)


def get_items():
    """Retorna todos os itens da comanda"""
    return comanda


def clear():
    """Limpa a comanda"""
    comanda.clear()
