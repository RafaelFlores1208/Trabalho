from sistema import (
    Categoria, ItemMenu, Cliente, Mesa,
    ItemPedido, Pedido, PagamentoPix, PagamentoCartao
)


class Cardapio:
    def __init__(self) -> None:
        self._categorias: list[Categoria] = []

    def criar_categoria(self, nome: str) -> Categoria:
        categoria = Categoria(nome)
        self._categorias.append(categoria)
        return categoria

    def adicionar_item(
        self,
        categoria: Categoria,
        nome: str,
        preco: float,
        descricao: str,
    ) -> ItemMenu:
        item = ItemMenu(categoria, nome, preco, descricao)
        categoria.adicionar_item(item)
        return item

    def listar_cardapio(self) -> None:
        print("===== CARDÁPIO =====")
        for categoria in self._categorias:
            print(f"--- {categoria.nome} ---")
            for item in categoria.get_itens():
                print(f" - {item}")
        print("====================\n")


class PedidoService:
    """Serviço de alto nível para criação e pagamento de pedidos."""

    def criar_pedido(self, cliente: Cliente, mesa: Mesa) -> Pedido:
        mesa.ocupar()
        return Pedido(cliente, mesa)

    def adicionar_item(
        self,
        pedido: Pedido,
        item_menu: ItemMenu,
        quantidade: int,
    ) -> None:
        item = ItemPedido(item_menu, quantidade)
        pedido.adicionar_item(item)

    def pagar_pix(self, pedido: Pedido, chave: str) -> str:
        pagamento = PagamentoPix(pedido.total(), chave)
        pedido.definir_pagamento(pagamento)
        return pedido.fechar_pedido()

    def pagar_cartao(self, pedido: Pedido, numero: str) -> str:
        pagamento = PagamentoCartao(pedido.total(), numero)
        pedido.definir_pagamento(pagamento)
        return pedido.fechar_pedido()