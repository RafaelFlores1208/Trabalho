# compra.py
from tkinter import *
from tkinter import messagebox
import order

# --- Cores do Tema ---
DORADO_POLIDO = "#BEA95B" # Destaque Dourado Polido
BG_ESCuro = "#1A1512"    # Cor de Fundo Escura (Ébano)
COR_CONTRASTE = "#F0F0F0" # Cor para o rótulo de Quantidade

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

# --- Funções de Incremento/Decremento (Auxiliares de refresh_items) ---
def increment_item(item_name, refresh_func):
    # Encontra a quantidade atual (current_qty) do item pelo nome (item_name)
    current_qty = next((it[2] for it in order.get_items() if it[0] == item_name), 0)
    order.set_quantity(item_name, current_qty + 1)
    refresh_func()
    
def decrement_item(item_name, refresh_func):
    current_qty = next((it[2] for it in order.get_items() if it[0] == item_name), 0)
    order.set_quantity(item_name, current_qty - 1)
    refresh_func()


# --- Função principal da comanda ---
def create_compra_page(parent, usuario_logado=False, email_pix="rafael@email.com"):
    for w in parent.winfo_children():
        w.destroy()

    page = Frame(parent, bg=BG_ESCuro)
    page.pack(fill="both", expand=True) # A página principal se expande

    # Cabeçalho com tema
    Label(page, text="Comanda (Compra)", font=("Georgia", 20, "bold"),
          fg=DORADO_POLIDO, bg=BG_ESCuro).pack(anchor="w", padx=16, pady=(12,6))

    # Status do usuário com tema
    status_text = "Consultando preços (login necessário para finalizar)" \
                  if not usuario_logado else "Usuário logado (pode finalizar pedido)"
    Label(page, text=status_text, font=("Georgia", 12, "italic"),
          fg=DORADO_POLIDO, bg=BG_ESCuro).pack(anchor="w", padx=16, pady=(0,6))

    body = Frame(page, bg=BG_ESCuro)
    # Corpo se expande para a responsividade
    body.pack(fill="both", expand=True, padx=12, pady=10) 

    # Cabeçalho da tabela
    hdr = Frame(body, bg=BG_ESCuro)
    hdr.pack(fill="x")
    Label(hdr, text="Item", width=40, anchor="w", bg=BG_ESCuro, fg="white", font=("Georgia", 11, "bold")).pack(side="left")
    Label(hdr, text="Qtd", width=6, anchor="center", bg=BG_ESCuro, fg="white", font=("Georgia", 11, "bold")).pack(side="left")
    Label(hdr, text="Subtotal", width=12, anchor="e", bg=BG_ESCuro, fg="white", font=("Georgia", 11, "bold")).pack(side="right", padx=(0,12))

    items_frame = Frame(body, bg=BG_ESCuro)
    # Quadro da lista de itens se expande e preenche (Crucial para responsividade)
    items_frame.pack(fill="both", expand=True, pady=(6,12)) 

    # Total fixo
    total_frame = Frame(body, bg=BG_ESCuro)
    total_label = Label(total_frame, text="", bg=BG_ESCuro, fg=DORADO_POLIDO, font=("Georgia", 16, "bold"))
    total_label.pack(side="right", padx=12)
    total_frame.pack(fill="x", padx=12, pady=(6,12)) # Preenche a largura

    # --- Atualiza lista de itens ---
    def refresh_items():
        for w in items_frame.winfo_children():
            w.destroy()

        items = order.get_items()
        for nome, preco, qtd, desc in items:
            row = Frame(items_frame, bg="white")
            row.pack(fill="x", padx=12, pady=6)

            left = Frame(row, bg="white")
            left.pack(side="left", fill="both", expand=True) # O lado esquerdo (nome/desc) se expande
            Label(left, text=nome, bg="white", fg="#222", font=("Georgia", 12, "bold")).pack(anchor="w")
            if desc:
                # wraplength dinâmico para garantir responsividade no texto
                wraplength_val = max(100, left.winfo_width() - 20) 
                Label(left, text=desc, bg="white", fg="#555", font=("Georgia", 10), wraplength=wraplength_val).pack(anchor="w")

            # quantidade
            qty_frame = Frame(row, bg="white", width=80)
            qty_frame.pack(side="left")
            
            # Botão +
            Button(qty_frame, text="+", width=3, bg=DORADO_POLIDO, fg=BG_ESCuro, relief="flat", cursor="hand2",
                   command=lambda n=nome: increment_item(n, refresh_items)).pack(side="left", padx=(6,2), pady=6)
            
            # Label de Quantidade
            Label(qty_frame, text=str(qtd), width=4, bg=COR_CONTRASTE, fg="#222", font=("Georgia", 11, "bold")).pack(side="left", padx=2) 
            
            # Botão -
            Button(qty_frame, text="-", width=3, bg=DORADO_POLIDO, fg=BG_ESCuro, relief="flat", cursor="hand2",
                   command=lambda n=nome: decrement_item(n, refresh_items)).pack(side="left", padx=(2,6), pady=6)

            # subtotal
            subtotal = preco * qtd
            Label(row, text=f"R$ {subtotal:.2f}", bg="white", fg="#222", font=("Georgia", 12)).pack(side="right", padx=(0,12))

        # atualiza total
        total = order.get_total()
        total_label.config(text=f"Total: R$ {total:.2f}")

    # Bind o evento <Configure> para atualizar a lista ao redimensionar a janela
    items_frame.bind("<Configure>", lambda e: refresh_items())
    refresh_items()

    # --- Funções de ação ---
    actions = Frame(page, bg=BG_ESCuro)
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

        # Popup de confirmação do total
        confirmar = messagebox.askyesno(
            "Confirmar Pagamento",
            f"O total do pedido é R$ {total:.2f}.\nDeseja confirmar o pagamento?"
        )
        if not confirmar:
            return 

        # processa pagamento
        pagamento = PagamentoPIX(email_pix)
        resultado = pagamento.pagar(total)

        # gerar recibo
        try:
            with open("recibo.txt", "w", encoding='utf-8') as f:
                f.write("RECIBO DE COMPRA\n")
                f.write("=================\n")
                for nome, preco, qtd, desc in itens:
                    f.write(f"{nome} x{qtd} - R$ {preco*qtd:.2f}\n")
                f.write("-----------------\n")
                f.write(f"TOTAL: R$ {total:.2f}\n")
                f.write("=================\n")
        except Exception as e:
            messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar o recibo: {e}")

        order.clear_order()
        messagebox.showinfo("Pedido Finalizado", f"{resultado}\nRecibo salvo em 'recibo.txt'.")
        create_compra_page(parent, usuario_logado)

    # Botões de Ação com Tema
    Button(actions, text="Limpar Comanda", bg="#555", fg="white", relief="flat", cursor="hand2", command=on_clear).pack(side="left", padx=8)
    Button(actions, text="Finalizar Pedido", bg=DORADO_POLIDO, fg=BG_ESCuro, font=("Georgia", 12, "bold"), relief="flat", cursor="hand2", command=on_finalize).pack(side="right", padx=8)

    return page