from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pagamento import pagamento, pagamentopix, pagamentocartao

class Cliente:
    def __init__(self, nome: str, telefone: str) -> None:
        self.__nome = nome
        self.__telefone = telefone

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def telefone(self) -> str:
        return self.__telefone


class Mesa:
    def __init__(self, numero: int, lugares: int) -> None:
        self.__numero = numero
        self.__lugares = lugares
        self.__ocupada = False

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def lugares(self) -> int:
        return self.__lugares

    @property
    def ocupada(self) -> bool:
        return self.__ocupada

    def ocupar(self) -> None:
        self.__ocupada = True

    def liberar(self) -> None:
        self.__ocupada = False


class Categoria:
    def __init__(self, nome: str) -> None:
        self.__nome = nome
        self.__itens: List[ItemMenu] = []

    @property
    def nome(self) -> str:
        return self.__nome

    def adicionar_item(self, item: "ItemMenu") -> None:
        self.__itens.append(item)

    def get_itens(self) -> List["ItemMenu"]:
        return list(self.__itens)


class ItemMenu:
    def __init__(self, categoria: Categoria, nome: str,
                 preco: float, descricao: str) -> None:
        self.__categoria = categoria
        self.__nome = nome
        self.__preco = preco
        self.__descricao = descricao
        self.__ativo = True

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def preco(self) -> float:
        return self.__preco

    @property
    def descricao(self) -> str:
        return self.__descricao

    @property
    def ativo(self) -> bool:
        return self.__ativo

    def desativar(self) -> None:
        self.__ativo = False

    def __str__(self) -> str:
        return f"{self.__nome} - R${self.__preco:.2f} ({self.__descricao})"


class ItemPedido:
    def __init__(self, item_menu: ItemMenu, quantidade: int) -> None:
        self.__item_menu = item_menu
        self.__quantidade = quantidade
        self.__preco_unit = item_menu.preco

    @property
    def item_menu(self) -> ItemMenu:
        return self.__item_menu

    @property
    def quantidade(self) -> int:
        return self.__quantidade

    @property
    def preco_unit(self) -> float:
        return self.__preco_unit

    def subtotal(self) -> float:
        return self.__preco_unit * self.__quantidade

class Pedido:
    def __init__(self, cliente: Cliente, mesa: Mesa) -> None:
        self.__cliente = cliente
        self.__mesa = mesa
        self.__itens: List[ItemPedido] = []
        self.__pagamento: Optional[Pagamento] = None
        self.__data_hora = datetime.now()
        self.__status = "aberto"

    @property
    def data_hora(self) -> datetime:
        return self.__data_hora

    @property
    def status(self) -> str:
        return self.__status

    def adicionar_item(self, item_pedido: ItemPedido) -> None:
        self.__itens.append(item_pedido)

    def total(self) -> float:
        return sum(item.subtotal() for item in self.__itens)

    def definir_pagamento(self, pagamento: Pagamento) -> None:
        self.__pagamento = pagamento

    def fechar_pedido(self) -> str:
        if not self.__pagamento:
            raise Exception("Nenhum pagamento definido!")
        self.__status = "fechado"
        return self.__pagamento.processar()

    # isso daqui é pro main
    # joga junto com pagamento
    def get_cliente(self) -> Cliente:
        return self.__cliente

    def get_mesa(self) -> Mesa:
        return self.__mesa

    def get_itens(self) -> list[ItemPedido]:
        return list(self.__itens)

    def get_pagamento(self) -> Optional[Pagamento]:
        return self.__pagamento
        def definir_pagamento(self, pagamento: Pagamento) -> None:
            self.__pagamento = pagamento