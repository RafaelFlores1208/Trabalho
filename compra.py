# compra.py - Tela de visualização e edição da comanda
# Ajustado para funcionar com order.py e integrado ao Dashboard
# Agora pede opcionalmente o Nome do Cliente para liberar reserva ao pagar.

import tkinter as tk
from tkinter import messagebox, simpledialog
import order

def create_compra_page(parent_frame):
    """
    Esta função é chamada pelo Dashboard.
    Ela destrói os widgets da tela atual e monta a tela da comanda
    dentro do próprio frame de conteúdo do Dashboard.
    Agora inclui um campo opcional 'Nome do cliente' que será enviado
    à tela de pagamento para, se necessário, liberar reservas.
    """
    # Limpa a tela atual
    for w in parent_frame.winfo_children():
        w.destroy()

    # Título
    tk.Label(
        parent_frame, text="Itens da Comanda",
        font=("Arial", 18, "bold"),
        bg="#1A1512", fg="white"
    ).pack(pady=8)

    # Campo opcional: nome do cliente (usado para liberar reserva)
    nome_frame = tk.Frame(parent_frame, bg="#1A1512")
    nome_frame.pack(pady=(0,8), fill="x", padx=12)
    tk.Label(nome_frame, text="Nome do cliente (opcional, se tiver reserva):",
             bg="#1A1512", fg="#F4D465", font=("Arial", 10)).pack(anchor="w")
    entry_cliente_nome = tk.Entry(nome_frame, width=40)
    entry_cliente_nome.pack(anchor="w", pady=4)

    # Frame dos itens
    frame_itens = tk.Frame(parent_frame, bg="#1A1512")
    frame_itens.pack(pady=6, fill="both", expand=False, padx=12)

    # Frame total
    frame_total = tk.Frame(parent_frame, bg="#1A1512")
    frame_total.pack(pady=6)

    label_total = tk.Label(
        frame_total, text="Total: R$ 0.00",
        font=("Arial", 16, "bold"),
        bg="#1A1512", fg="#F4D465"
    )
    label_total.pack()

    # Atualizar total
    def atualizar_total():
        total = order.get_total()
        label_total.config(text=f"Total: R$ {total:.2f}")

    # Funções internas
    def atualizar_lista():
        for w in frame_itens.winfo_children():
            w.destroy()

        itens = order.get_items()

        if not itens:
            tk.Label(frame_itens, text="Nenhum item na comanda.",
                     bg="#1A1512", fg="white", font=("Arial", 12)).pack()
            return

        for nome, preco, quantidade, desc in itens:
            row = tk.Frame(frame_itens, bg="#1A1512")
            row.pack(fill="x", pady=4)

            tk.Label(row, text=f"{nome} - R$ {preco:.2f}",
                     font=("Arial", 12), bg="#1A1512", fg="white").grid(row=0, column=0, padx=5)

            tk.Button(row, text="-", width=2,
                      command=lambda n=nome, q=quantidade: alterar_quantidade(n, q-1)).grid(row=0, column=1)

            tk.Label(row, text=str(quantidade),
                     width=3, bg="#1A1512", fg="white").grid(row=0, column=2)

            tk.Button(row, text="+", width=2,
                      command=lambda n=nome, q=quantidade: alterar_quantidade(n, q+1)).grid(row=0, column=3)

            tk.Button(row, text="Remover", fg="red",
                      command=lambda n=nome: remover_item(n)).grid(row=0, column=4, padx=5)

    def alterar_quantidade(nome, nova_qtd):
        order.set_quantity(nome, nova_qtd)
        atualizar_lista()
        atualizar_total()

    def remover_item(nome):
        order.set_quantity(nome, 0)
        atualizar_lista()
        atualizar_total()

    # Botão pagamento -> abre a tela de pagamento passando o nome do cliente (se houver)
    def ir_pagamento():
        from pagamento import abrir_tela_pagamento
        root = parent_frame.winfo_toplevel()
        cliente_nome = entry_cliente_nome.get().strip()
        # se vazio, passamos None
        if cliente_nome == "":
            cliente_nome = None
        abrir_tela_pagamento(root, cliente_nome)

    tk.Button(
        parent_frame, text="Finalizar Pedido",
        bg="green", fg="white",
        font=("Arial", 14, "bold"),
        width=20,
        command=ir_pagamento
    ).pack(pady=12)

    # Primeiro carregamento
    atualizar_lista()
    atualizar_total()


# -------------------------------------------------------------------------
# FUNÇÃO LEGADA: manter compatibilidade com chamadas que abrem nova janela
# -------------------------------------------------------------------------
def abrir_tela_compra(tela_anterior):
    tela_anterior.withdraw()

    janela = tk.Toplevel()
    janela.title("Comanda / Itens selecionados")
    janela.geometry("450x600")
    janela.configure(bg="#1A1512")

    # ------- TÍTULO -------
    tk.Label(janela, text="Itens da Comanda", font=("Arial", 16, "bold"), bg="#1A1512", fg="white").pack(pady=10)

    # Campo nome cliente opcional (quando abrir em janela separada)
    tk.Label(janela, text="Nome do cliente (opcional, se tiver reserva):", bg="#1A1512", fg="#F4D465").pack()
    entry_cliente = tk.Entry(janela, width=35)
    entry_cliente.pack(pady=(0,8))

    # Frame da lista de itens
    frame_itens = tk.Frame(janela, bg="#1A1512")
    frame_itens.pack(pady=10, fill="both", expand=True)

    def atualizar_lista():
        for widget in frame_itens.winfo_children():
            widget.destroy()

        itens = order.get_items()

        if not itens:
            tk.Label(frame_itens, text="Nenhum item na comanda.", bg="#1A1512", fg="white").pack()
            return

        for nome, preco, quantidade, desc in itens:
            item_frame = tk.Frame(frame_itens, pady=5, bg="#1A1512")
            item_frame.pack(fill="x")

            tk.Label(item_frame, text=f"{nome} - R$ {preco:.2f}", font=("Arial", 12), bg="#1A1512", fg="white").grid(row=0, column=0, padx=5)

            tk.Button(item_frame, text="-", width=2,
                      command=lambda n=nome, q=quantidade: alterar_quantidade(n, q - 1)).grid(row=0, column=1)

            tk.Label(item_frame, text=str(quantidade), width=3, bg="#1A1512", fg="white").grid(row=0, column=2)

            tk.Button(item_frame, text="+", width=2,
                      command=lambda n=nome, q=quantidade: alterar_quantidade(n, q + 1)).grid(row=0, column=3)

            tk.Button(item_frame, text="Remover", fg="red",
                      command=lambda n=nome: remover_item(n)).grid(row=0, column=4, padx=5)

    def alterar_quantidade(nome, nova_qtd):
        order.set_quantity(nome, nova_qtd)
        atualizar_lista()
        atualizar_total()

    def remover_item(nome):
        order.set_quantity(nome, 0)
        atualizar_lista()
        atualizar_total()

    label_total = tk.Label(janela, text="Total: R$ 0.00", font=("Arial", 14, "bold"), bg="#1A1512", fg="#F4D465")
    label_total.pack(pady=12)

    def atualizar_total():
        total = order.get_total()
        label_total.config(text=f"Total: R$ {total:.2f}")

    def ir_pagamento():
        from pagamento import abrir_tela_pagamento
        root = janela
        cliente_nome = entry_cliente.get().strip()
        if cliente_nome == "":
            cliente_nome = None
        abrir_tela_pagamento(root, cliente_nome)

    tk.Button(janela, text="Finalizar Pedido", font=("Arial", 12, "bold"),
              bg="green", fg="white", width=20, command=ir_pagamento).pack(pady=10)

    def voltar():
        janela.destroy()
        tela_anterior.deiconify()

    tk.Button(janela, text="Voltar", font=("Arial", 12), width=15,
              command=voltar).pack(pady=10)

    atualizar_lista()
    atualizar_total()

    janela.mainloop()
