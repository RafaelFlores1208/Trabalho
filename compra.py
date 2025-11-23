# compra.py
from tkinter import *
import order
from tkinter import messagebox

def create_compra_page(parent):
    """Cria a página de comanda dentro do frame parent."""
    for w in parent.winfo_children():
        w.destroy()

    page = Frame(parent, bg="#1A1512")
    page.pack(fill="both", expand=True)

    Label(page, text="Comanda (Compra)", font=("Georgia", 20, "bold"),
          fg="white", bg="#1A1512").pack(anchor="w", padx=16, pady=(12,6))

    body = Frame(page, bg="#1A1512")
    body.pack(fill="both", expand=True, padx=12, pady=10)

    # Cabeçalho da tabela
    hdr = Frame(body, bg="#1A1512")
    hdr.pack(fill="x")
    Label(hdr, text="Item", width=40, anchor="w", bg="#1A1512", fg="white", font=("Georgia", 11, "bold")).pack(side="left")
    Label(hdr, text="Qtd", width=6, anchor="center", bg="#1A1512", fg="white", font=("Georgia", 11, "bold")).pack(side="left")
    Label(hdr, text="Subtotal", width=12, anchor="e", bg="#1A1512", fg="white", font=("Georgia", 11, "bold")).pack(side="right", padx=(0,12))

    # Frame dos itens (scroll se necessário)
    items_frame = Frame(body, bg="#1A1512")
    items_frame.pack(fill="both", expand=True, pady=(6,12))

    # função para recarregar lista de itens
    def refresh_items():
        for w in items_frame.winfo_children():
            w.destroy()

        items = order.get_items()
        for name, preco, qtd, desc in items:
            row = Frame(items_frame, bg="white")
            row.pack(fill="x", padx=12, pady=6)

            left = Frame(row, bg="white")
            left.pack(side="left", fill="both", expand=True)
            Label(left, text=name, bg="white", fg="#222", font=("Georgia", 12, "bold")).pack(anchor="w")
            if desc:
                Label(left, text=desc, bg="white", fg="#555", font=("Georgia", 10), wraplength=420).pack(anchor="w")

            # quantidade com botões + / -
            qty_frame = Frame(row, bg="white", width=80)
            qty_frame.pack(side="left")
            def make_inc_dec(nm):
                def inc():
                    # aumenta 1
                    current = 0
                    items_map = {it[0]: it for it in order.get_items()}
                    if nm in items_map:
                        current = items_map[nm][2]
                    order.set_quantity(nm, current+1)
                    refresh_items()
                def dec():
                    items_map = {it[0]: it for it in order.get_items()}
                    current = items_map[nm][2] if nm in items_map else 0
                    order.set_quantity(nm, current-1)
                    refresh_items()
                return inc, dec

            inc, dec = make_inc_dec(name)
            Button(qty_frame, text="+", width=3, command=inc).pack(side="left", padx=(6,2), pady=6)
            Label(qty_frame, text=str(qtd), width=4, bg="white").pack(side="left", padx=2)
            Button(qty_frame, text="-", width=3, command=dec).pack(side="left", padx=(2,6), pady=6)

            # subtotal
            subtotal = preco * qtd
            Label(row, text=f"R$ {subtotal:.2f}", bg="white", fg="#222", font=("Georgia", 12)).pack(side="right", padx=(0,12))

        # total
        total_frame = Frame(body, bg="#1A1512")
        total_frame.pack(fill="x", padx=12, pady=(6,12))
        total = order.get_total()
        Label(total_frame, text=f"Total: R$ {total:.2f}", bg="#1A1512", fg="#F4D465", font=("Georgia", 16, "bold")).pack(side="right", padx=12)

    refresh_items()

    # Ações: limpar e finalizar
    actions = Frame(page, bg="#1A1512")
    actions.pack(fill="x", padx=12, pady=(0,12))

    def on_clear():
        if messagebox.askyesno("Limpar comanda", "Deseja limpar toda a comanda?"):
            order.clear_order()
            create_compra_page(parent)  # recarrega

    def on_finalize():
        total = order.get_total()
        if total <= 0:
            messagebox.showwarning("Comanda vazia", "Adicione itens antes de finalizar.")
            return
        # aqui você pode integrar com sistema de pagamento / salvar em BD
        messagebox.showinfo("Pedido finalizado", f"Pedido finalizado. Total: R$ {total:.2f}")
        order.clear_order()
        create_compra_page(parent)

    Button(actions, text="Limpar Comanda", bg="#333", fg="white", command=on_clear).pack(side="left", padx=8)
    Button(actions, text="Finalizar Pedido", bg="#F4D465", fg="#141107", command=on_finalize).pack(side="right", padx=8)
    return page
