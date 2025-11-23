from tkinter import *
from tkinter import messagebox
import order

# --- Classes de Pagamento ---
class Pagamento:
    """Classe abstrata de pagamento"""
    def pagar(self, total):
        raise NotImplementedError("Método pagar deve ser implementado pela subclasse")

class PagamentoPIX(Pagamento):
    def __init__(self, email):
        self.email = email

    def pagar(self, total):
        # Simulação de pagamento PIX
        return f"Pagamento de R$ {total:.2f} via PIX para {self.email} processado com sucesso!"

# --- Função principal da comanda ---
def create_compra_page(parent, usuario_logado=False, email_pix="rafael@email.com"):
    for w in parent.winfo_children():
        w.destroy()

    page = Frame(parent, bg="#1A1512")
    page.pack(fill="both", expand=True)

    # Cabeçalho
    Label(page, text="Comanda (Compra)", font=("Georgia", 20, "bold"),
          fg="white", bg="#1A1512").pack(anchor="w", padx=16, pady=(12,6))

    # Status do usuário
    status_text = "Consultando preços (login necessário para finalizar)" \
                  if not usuario_logado else "Usuário logado (pode finalizar pedido)"
    Label(page, text=status_text, font=("Georgia", 12, "italic"),
          fg="#F4D465", bg="#1A1512").pack(anchor="w", padx=16, pady=(0,6))

    body = Frame(page, bg="#1A1512")
    body.pack(fill="both", expand=True, padx=12, pady=10)

    # Cabeçalho da tabela
    hdr = Frame(body, bg="#1A1512")
    hdr.pack(fill="x")
    Label(hdr, text="Item", width=40, anchor="w", bg="#1A1512", fg="white", font=("Georgia", 11, "bold")).pack(side="left")
    Label(hdr, text="Qtd", width=6, anchor="center", bg="#1A1512", fg="white", font=("Georgia", 11, "bold")).pack(side="left")
    Label(hdr, text="Subtotal", width=12, anchor="e", bg="#1A1512", fg="white", font=("Georgia", 11, "bold")).pack(side="right", padx=(0,12))

    items_frame = Frame(body, bg="#1A1512")
    items_frame.pack(fill="both", expand=True, pady=(6,12))

    # Total fixo
    total_frame = Frame(body, bg="#1A1512")
    total_frame.pack(fill="x", padx=12, pady=(6,12))
    total_label = Label(total_frame, text="", bg="#1A1512", fg="#F4D465", font=("Georgia", 16, "bold"))
    total_label.pack(side="right", padx=12)

    # --- Atualiza lista de itens ---
    def refresh_items():
        for w in items_frame.winfo_children():
            w.destroy()

        items = order.get_items()
        for nome, preco, qtd, desc in items:
            row = Frame(items_frame, bg="white")
            row.pack(fill="x", padx=12, pady=6)

            left = Frame(row, bg="white")
            left.pack(side="left", fill="both", expand=True)
            Label(left, text=nome, bg="white", fg="#222", font=("Georgia", 12, "bold")).pack(anchor="w")
            if desc:
                Label(left, text=desc, bg="white", fg="#555", font=("Georgia", 10), wraplength=420).pack(anchor="w")

            # quantidade
            qty_frame = Frame(row, bg="white", width=80)
            qty_frame.pack(side="left")
            def make_inc_dec(nm):
                def inc():
                    current = {it[0]: it for it in order.get_items()}.get(nm, [0,0,0, ""])[2]
                    order.set_quantity(nm, current+1)
                    refresh_items()
                def dec():
                    current = {it[0]: it for it in order.get_items()}.get(nm, [0,0,0, ""])[2]
                    order.set_quantity(nm, current-1)
                    refresh_items()
                return inc, dec

            inc, dec = make_inc_dec(nome)
            Button(qty_frame, text="+", width=3, command=inc).pack(side="left", padx=(6,2), pady=6)
            Label(qty_frame, text=str(qtd), width=4, bg="white").pack(side="left", padx=2)
            Button(qty_frame, text="-", width=3, command=dec).pack(side="left", padx=(2,6), pady=6)

            # subtotal
            subtotal = preco * qtd
            Label(row, text=f"R$ {subtotal:.2f}", bg="white", fg="#222", font=("Georgia", 12)).pack(side="right", padx=(0,12))

        # atualiza total
        total = order.get_total()
        total_label.config(text=f"Total: R$ {total:.2f}")

    refresh_items()

    # --- Funções de ação ---
    actions = Frame(page, bg="#1A1512")
    actions.pack(fill="x", padx=12, pady=(0,12))

    def on_clear():
        if messagebox.askyesno("Limpar comanda", "Deseja limpar toda a comanda?"):
            order.clear_order()
            create_compra_page(parent, usuario_logado)

    def on_finalize():
        if not usuario_logado:
            messagebox.showwarning("Acesso negado", "Você precisa estar logado para finalizar a comanda.")
            return

        itens = order.get_items()
        if not itens:
            messagebox.showwarning("Comanda vazia", "Adicione itens antes de finalizar.")
            return

        total = order.get_total()

        # --- Popup de confirmação do total ---
        confirmar = messagebox.askyesno(
            "Confirmar Pagamento",
            f"O total do pedido é R$ {total:.2f}.\nDeseja confirmar o pagamento?"
        )
        if not confirmar:
            return  # usuário cancelou

        # processa pagamento
        pagamento = PagamentoPIX(email_pix)
        resultado = pagamento.pagar(total)

        # gerar recibo
        with open("recibo.txt", "w") as f:
            f.write("RECIBO DE COMPRA\n")
            f.write("=================\n")
            for nome, preco, qtd, desc in itens:
                if desc:
                    f.write(f"{nome} x{qtd} - R$ {preco*qtd:.2f} ({desc})\n")
                else:
                    f.write(f"{nome} x{qtd} - R$ {preco*qtd:.2f}\n")
            f.write("-----------------\n")
            f.write(f"TOTAL: R$ {total:.2f}\n")
            f.write("=================\n")

        order.clear_order()
        messagebox.showinfo("Pedido Finalizado", f"{resultado}\nRecibo salvo em 'recibo.txt'.")
        create_compra_page(parent, usuario_logado)

    Button(actions, text="Limpar Comanda", bg="#333", fg="white", command=on_clear).pack(side="left", padx=8)
    Button(actions, text="Finalizar Pedido", bg="#F4D465", fg="#141107", command=on_finalize).pack(side="right", padx=8)

    return page

# --- Função para adicionar item pelo menu ---
def adicionar_item_menu(parent, nome, preco, desc="", usuario_logado=False):
    order.add_item(nome, preco, 1, desc)
    create_compra_page(parent, usuario_logado)  # recarrega página mostrando subtotal e total
