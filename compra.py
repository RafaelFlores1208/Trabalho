# compra.py - Tela de visualização e edição da comanda
# Totalmente estilizado para combinar com o tema escuro + dourado do sistema

import tkinter as tk
from tkinter import messagebox
import order

# Paleta padrão do sistema
BG = "#1A1512"
DOURADO = "#F4D465"
CARD_BG = "#2A2218"
WHITE = "white"

FONT_TITULO = ("Georgia", 20, "bold")
FONT_LABEL = ("Georgia", 12)
FONT_BOTAO = ("Georgia", 12, "bold")


def create_compra_page(parent_frame):
    """Cria a tela estilizada da comanda dentro do frame principal do dashboard."""

    # Limpa conteúdo atual
    for w in parent_frame.winfo_children():
        w.destroy()

    parent_frame.configure(bg=BG)

    # Título
    tk.Label(
        parent_frame,
        text="Itens da Comanda",
        font=FONT_TITULO,
        bg=BG,
        fg=DOURADO
    ).pack(pady=(10, 4))

    # Campo Nome do cliente
    nome_frame = tk.Frame(parent_frame, bg=BG)
    nome_frame.pack(fill="x", padx=16)

    tk.Label(
        nome_frame,
        text="Nome do cliente (opcional – libera reserva):",
        bg=BG,
        fg=DOURADO,
        font=("Georgia", 10)
    ).pack(anchor="w")

    entry_cliente_nome = tk.Entry(nome_frame, width=40)
    entry_cliente_nome.pack(anchor="w", pady=4)

    # Card da lista
    card = tk.Frame(parent_frame, bg=CARD_BG, bd=2, relief="ridge")
    card.pack(fill="both", expand=True, padx=16, pady=12)

    frame_itens = tk.Frame(card, bg=CARD_BG)
    frame_itens.pack(fill="both", expand=True, padx=10, pady=10)

    # Total
    frame_total = tk.Frame(parent_frame, bg=BG)
    frame_total.pack(pady=8)

    label_total = tk.Label(
        frame_total,
        text="Total: R$ 0.00",
        font=("Georgia", 18, "bold"),
        bg=BG,
        fg=DOURADO
    )
    label_total.pack()

    # Atualizar total
    def atualizar_total():
        total = order.get_total()
        label_total.config(text=f"Total: R$ {total:.2f}")

    # Atualizar lista
    def atualizar_lista():
        for w in frame_itens.winfo_children():
            w.destroy()

        itens = order.get_items()

        if not itens:
            tk.Label(
                frame_itens,
                text="Nenhum item na comanda.",
                font=("Georgia", 12),
                bg=CARD_BG,
                fg=WHITE
            ).pack(pady=6)
            return

        for nome, preco, quantidade, desc in itens:
            linha = tk.Frame(frame_itens, bg=CARD_BG, pady=4)
            linha.pack(fill="x")

            # Nome + preço
            tk.Label(
                linha,
                text=f"{nome} - R$ {preco:.2f}",
                font=FONT_LABEL,
                bg=CARD_BG,
                fg=WHITE
            ).grid(row=0, column=0, padx=6, sticky="w")

            # Botão -
            tk.Button(
                linha,
                text="-",
                width=3,
                bg="#8B2E2E",
                fg="white",
                relief="flat",
                command=lambda n=nome, q=quantidade: alterar_quantidade(n, q - 1)
            ).grid(row=0, column=1, padx=4)

            # QTD
            tk.Label(
                linha,
                text=str(quantidade),
                width=4,
                bg=CARD_BG,
                fg=WHITE,
                font=("Georgia", 12, "bold")
            ).grid(row=0, column=2)

            # Botão +
            tk.Button(
                linha,
                text="+",
                width=3,
                bg=DOURADO,
                fg="black",
                relief="flat",
                command=lambda n=nome, q=quantidade: alterar_quantidade(n, q + 1)
            ).grid(row=0, column=3, padx=4)

            # Botão Remover
            tk.Button(
                linha,
                text="Remover",
                bg="#b03a2e",
                fg="white",
                relief="flat",
                command=lambda n=nome: remover_item(n)
            ).grid(row=0, column=4, padx=6)

    # Funções
    def alterar_quantidade(nome, nova_qtd):
        order.set_quantity(nome, nova_qtd)
        atualizar_lista()
        atualizar_total()

    def remover_item(nome):
        order.set_quantity(nome, 0)
        atualizar_lista()
        atualizar_total()

    # Finalizar pedido (vai ao pagamento)
    def ir_pagamento():
        from pagamento import abrir_tela_pagamento
        root = parent_frame.winfo_toplevel()
        cliente_nome = entry_cliente_nome.get().strip() or None
        abrir_tela_pagamento(root, cliente_nome)

    tk.Button(
        parent_frame,
        text="Finalizar Pedido",
        bg="green",
        fg="white",
        font=("Georgia", 14, "bold"),
        width=22,
        relief="flat",
        command=ir_pagamento
    ).pack(pady=10)

    # Inicialização
    atualizar_lista()
    atualizar_total()


# ==========================================================================================
# FUNÇÃO LEGADA – MANTIDA PARA COMPATIBILIDADE (estilizada também)
# ==========================================================================================
def abrir_tela_compra(tela_anterior):
    tela_anterior.withdraw()

    janela = tk.Toplevel()
    janela.title("Comanda")
    janela.geometry("450x600")
    janela.configure(bg=BG)

    tk.Label(
        janela, text="Itens da Comanda",
        font=FONT_TITULO, bg=BG, fg=DOURADO
    ).pack(pady=12)

    # Nome cliente
    tk.Label(janela, text="Nome do cliente (opcional):",
             bg=BG, fg=DOURADO).pack()
    entry_cliente = tk.Entry(janela, width=35)
    entry_cliente.pack(pady=6)

    card = tk.Frame(janela, bg=CARD_BG, bd=2, relief="ridge")
    card.pack(fill="both", expand=True, padx=12, pady=12)

    frame_itens = tk.Frame(card, bg=CARD_BG)
    frame_itens.pack(fill="both", expand=True, padx=10, pady=10)

    def atualizar_lista():
        for w in frame_itens.winfo_children():
            w.destroy()

        itens = order.get_items()

        if not itens:
            tk.Label(frame_itens, text="Nenhum item na comanda.",
                     bg=CARD_BG, fg=WHITE).pack()
            return

        for nome, preco, quantidade, desc in itens:
            linha = tk.Frame(frame_itens, bg=CARD_BG, pady=4)
            linha.pack(fill="x")

            tk.Label(linha, text=f"{nome} - R$ {preco:.2f}",
                     bg=CARD_BG, fg=WHITE).grid(row=0, column=0, padx=6, sticky="w")

            tk.Button(linha, text="-", width=3,
                      bg="#8B2E2E", fg="white", relief="flat",
                      command=lambda n=nome, q=quantidade: alterar_quantidade(n, q - 1)).grid(row=0, column=1)

            tk.Label(linha, text=str(quantidade),
                     bg=CARD_BG, fg=WHITE, width=3).grid(row=0, column=2)

            tk.Button(linha, text="+", width=3,
                      bg=DOURADO, fg="black", relief="flat",
                      command=lambda n=nome, q=quantidade: alterar_quantidade(n, q + 1)).grid(row=0, column=3)

            tk.Button(linha, text="Remover",
                      bg="#b03a2e", fg="white", relief="flat",
                      command=lambda n=nome: remover_item(n)).grid(row=0, column=4, padx=4)

    label_total = tk.Label(janela, text="Total: R$ 0.00",
                           font=("Georgia", 16, "bold"),
                           bg=BG, fg=DOURADO)
    label_total.pack(pady=8)

    def atualizar_total():
        total = order.get_total()
        label_total.config(text=f"Total: R$ {total:.2f}")

    def alterar_quantidade(nome, nova_qtd):
        order.set_quantity(nome, nova_qtd)
        atualizar_lista()
        atualizar_total()

    def remover_item(nome):
        order.set_quantity(nome, 0)
        atualizar_lista()
        atualizar_total()

    def ir_pagamento():
        from pagamento import abrir_tela_pagamento
        cliente_nome = entry_cliente.get().strip() or None
        abrir_tela_pagamento(janela, cliente_nome)

    tk.Button(
        janela, text="Finalizar Pedido",
        font=FONT_BOTAO, bg="green", fg="white",
        width=20, relief="flat",
        command=ir_pagamento
    ).pack(pady=10)

    tk.Button(
        janela, text="Voltar",
        font=("Georgia", 12),
        width=15,
        command=lambda: (janela.destroy(), tela_anterior.deiconify())
    ).pack(pady=6)

    atualizar_lista()
    atualizar_total()

    janela.mainloop()
