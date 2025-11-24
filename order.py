# order.py – Sistema de armazenamento e cálculo da comanda
# Agora com persistência em JSON e registro de pedidos finalizados

import json
import os
from datetime import datetime

# Arquivo onde a comanda será salva
ORDER_FILE = "current_order.json"

# Arquivo de log de pedidos finalizados
LOG_FILE = "pedidos_log.txt"

# -------------------------------
# Carregar comanda salva (persistência)
# -------------------------------

def _load_order():
    """Carrega a comanda salva do JSON, se existir."""
    if os.path.exists(ORDER_FILE):
        try:
            with open(ORDER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}  # Se der erro no arquivo, evita travar o sistema
    return {}

# Dicionário que guarda a comanda do usuário
_current_order = _load_order()


# -------------------------------
# Funções da comanda
# -------------------------------

def _save_order():
    """Salva a comanda atual no arquivo JSON."""
    try:
        with open(ORDER_FILE, "w", encoding="utf-8") as f:
            json.dump(_current_order, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Erro ao salvar comanda:", e)


def add_item(nome, preco, quantidade, desc=""):
    """Adiciona itens à comanda."""
    if nome in _current_order:
        _current_order[nome]["quantidade"] += quantidade
    else:
        _current_order[nome] = {
            "nome": nome,
            "preco": preco,
            "quantidade": quantidade,
            "desc": desc
        }
    _save_order()


def set_quantity(nome, nova_quantidade):
    """Atualiza a quantidade de um item ou remove se for <= 0."""
    if nome in _current_order:
        if nova_quantidade > 0:
            _current_order[nome]["quantidade"] = nova_quantidade
        else:
            del _current_order[nome]

    _save_order()


def get_items():
    """Retorna todos os itens na comanda."""
    return [
        (item["nome"], item["preco"], item["quantidade"], item["desc"])
        for item in _current_order.values()
    ]


def get_total():
    """Calcula o total da comanda."""
    total = 0.0
    for item in _current_order.values():
        total += item["preco"] * item["quantidade"]
    return total


def clear_order():
    """Limpa a comanda e remove o arquivo JSON."""
    global _current_order
    _current_order = {}
    if os.path.exists(ORDER_FILE):
        os.remove(ORDER_FILE)


# -------------------------------
# LOG de pedidos finalizados
# -------------------------------

def registrar_pedido(itens, total, metodo="PIX", email=None):
    """
    Adiciona um registro completo no arquivo de log.
    Chame essa função dentro do finalizar pedido.
    """
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:

            f.write("\n==============================\n")
            f.write(f"DATA: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"MÉTODO DE PAGAMENTO: {metodo}\n")

            if email:
                f.write(f"EMAIL PIX: {email}\n")

            f.write("ITENS:\n")
            for nome, preco, qtd, desc in itens:
                f.write(f"  - {nome} x{qtd} = R$ {preco*qtd:.2f}\n")

            f.write(f"TOTAL DO PEDIDO: R$ {total:.2f}\n")
            f.write("==============================\n")

    except Exception as e:
        print("Erro ao registrar pedido:", e)
