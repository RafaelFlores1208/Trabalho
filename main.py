from sistema import Cliente, Mesa
from servicos import Cardapio, PedidoService

cardapio_service = Cardapio()
pedido_service = PedidoService()

# cardápio
bebidas = cardapio_service.criar_categoria("Bebidas")
pratos = cardapio_service.criar_categoria("Pratos")

suco = cardapio_service.adicionar_item(
    bebidas, "Suco Natural", 8.0, "Copo 300ml"
)
agua = cardapio_service.adicionar_item(
    bebidas, "Água Mineral", 5.0, "Garrafa 500ml"
)
burger = cardapio_service.adicionar_item(
    pratos, "Hambúrguer Artesanal", 22.0, "Pão brioche e queijo"
)

cardapio_service.listar_cardapio()

# criando cliente e mesa
cliente = Cliente("Rafael", "99999-9999")
mesa = Mesa(1, 4)

pedido = pedido_service.criar_pedido(cliente, mesa)

# adicionando item ao pedido
pedido_service.adicionar_item(pedido, suco, 2)
pedido_service.adicionar_item(pedido, agua, 1)
pedido_service.adicionar_item(pedido, burger, 1)

# output
print("===== RESUMO DO PEDIDO =====")
print(f"Cliente: {cliente.nome}")
print(f"Mesa: {mesa.numero}")
print("Itens:")
for item in pedido.get_itens():
    print(
        f" - {item.item_menu.nome} x{item.quantidade} "
        f"= R${item.subtotal():.2f}"
    )
print(f"Total: R${pedido.total():.2f}")
print("=============================\n")

# pagamento, abstração.
print("Processando pagamento (PIX)...")
resultado = pedido_service.pagar_pix(pedido, "rafael@email.com")
print(resultado)
