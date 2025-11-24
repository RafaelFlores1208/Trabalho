# pagamento.py – Tela de pagamento com abas (PIX, Cartão, Dinheiro)
# Integrado ao sistema Ébano
# Agora aceita parametro opcional cliente_nome e libera reservas quando confirmado.

import tkinter as tk
from tkinter import ttk, messagebox
import order
from reserva_mesa import RESERVAS

BG = "#1A1512"
DOURADO = "#F4D465"
CARD = "#2A2218"
WHITE = "white"


def abrir_tela_pagamento(janela_anterior, cliente_nome=None):
    """
    Abre a tela de pagamento. cliente_nome é opcional:
    - se preenchido, após pagamento todas as reservas cujo nome casar (case-insensitive)
      com cliente_nome serão liberadas (RESERVAS[mesa] = None).
    """
    janela_anterior.withdraw()

    tela = tk.Toplevel()
    tela.title("Pagamento")
    tela.geometry("520x520")
    tela.configure(bg=BG)

    total = order.get_total()

    # Cabeçalho
    tk.Label(
        tela,
        text="Pagamento",
        font=("Georgia", 26, "bold"),
        fg=DOURADO,
        bg=BG
    ).pack(pady=10)

    tk.Label(
        tela,
        text=f"Total a pagar: R$ {total:.2f}",
        font=("Georgia", 16),
        fg=WHITE,
        bg=BG
    ).pack(pady=(0, 6))

    # Se cliente_nome foi passado, mostra na tela (informativo)
    if cliente_nome:
        tk.Label(tela, text=f"Reserva informada: {cliente_nome}", bg=BG, fg="#CFC6A3", font=("Arial", 10, "italic")).pack(pady=(0,6))

    # ---------- NOTEBOOK (ABAS) ----------
    notebook = ttk.Notebook(tela)
    notebook.pack(fill="both", expand=True, padx=12, pady=8)

    # Estilo simples para o notebook
    style = ttk.Style()
    try:
        style.theme_create("ebanostyle", parent="alt", settings={
            "TNotebook.Tab": {
                "configure": {"padding": [10, 6], "font": ("Georgia", 10, "bold")},
                "map": {"background": [("selected", DOURADO)],
                        "foreground": [("selected", "black")]}
            }
        })
        style.theme_use("ebanostyle")
    except Exception:
        # se falhar (ambiente), continua com style padrão
        pass

    # ----------------- ABA PIX -----------------
    aba_pix = tk.Frame(notebook, bg=BG)
    notebook.add(aba_pix, text="PIX")

    tk.Label(aba_pix, text="E-mail para envio do comprovante:", bg=BG, fg=WHITE).pack(pady=8)
    email_entry = tk.Entry(aba_pix, width=40)
    email_entry.pack()

    tk.Label(aba_pix, text="Chave PIX:", bg=BG, fg=DOURADO, font=("Arial", 12, "bold")).pack(pady=12)
    tk.Label(aba_pix, text="ebano_restaurante@pix.com", bg=CARD, fg=WHITE,
             font=("Arial", 13), width=36, relief="groove").pack(pady=4)

    # ----------------- ABA CARTÃO -----------------
    aba_cartao = tk.Frame(notebook, bg=BG)
    notebook.add(aba_cartao, text="Cartão")

    tk.Label(aba_cartao, text="Nome no Cartão:", bg=BG, fg=WHITE).pack(pady=(8,2))
    nome_cartao = tk.Entry(aba_cartao, width=40)
    nome_cartao.pack()

    tk.Label(aba_cartao, text="Número do Cartão:", bg=BG, fg=WHITE).pack(pady=(8,2))
    numero_cartao = tk.Entry(aba_cartao, width=40)
    numero_cartao.pack()

    tk.Label(aba_cartao, text="Bandeira:", bg=BG, fg=WHITE).pack(pady=(8,2))
    bandeira_var = tk.StringVar(value="Visa")
    ttk.Combobox(aba_cartao, values=["Visa", "MasterCard", "Elo", "Hipercard"], width=36,
                 textvariable=bandeira_var, state="readonly").pack()

    tk.Label(aba_cartao, text="Tipo:", bg=BG, fg=WHITE).pack(pady=(8,2))
    tipo_var = tk.StringVar(value="Crédito")
    ttk.Combobox(aba_cartao, values=["Crédito", "Débito"], width=36,
                 textvariable=tipo_var, state="readonly").pack()

    tk.Label(aba_cartao, text="Validade (MM/AA):", bg=BG, fg=WHITE).pack(pady=(8,2))
    validade_entry = tk.Entry(aba_cartao, width=20)
    validade_entry.pack()

    tk.Label(aba_cartao, text="CVV:", bg=BG, fg=WHITE).pack(pady=(8,2))
    cvv_entry = tk.Entry(aba_cartao, width=12, show="*")
    cvv_entry.pack()

    # ----------------- ABA DINHEIRO -----------------
    aba_dinheiro = tk.Frame(notebook, bg=BG)
    notebook.add(aba_dinheiro, text="Dinheiro")

    tk.Label(aba_dinheiro, text="Valor entregue:", bg=BG, fg=WHITE).pack(pady=10)
    valor_entregue = tk.Entry(aba_dinheiro, width=20)
    valor_entregue.pack()

    troco_label = tk.Label(aba_dinheiro, text="", bg=BG, fg=DOURADO, font=("Arial", 12, "bold"))
    troco_label.pack(pady=8)

    def calcular_troco(event=None):
        try:
            pago = float(valor_entregue.get())
            troco = pago - total
            if troco < 0:
                troco_label.config(text="Valor insuficiente!")
            else:
                troco_label.config(text=f"Troco: R$ {troco:.2f}")
        except:
            troco_label.config(text="")

    valor_entregue.bind("<KeyRelease>", calcular_troco)

    # ----------------- FINALIZAR -----------------
    def finalizar_pagamento():
        metodo = notebook.tab(notebook.select(), "text")
        email = None

        if metodo == "PIX":
            email = email_entry.get().strip()
            if not email:
                messagebox.showwarning("Campo vazio", "Digite o e-mail para o comprovante.")
                return

        elif metodo == "Cartão":
            if not nome_cartao.get().strip() or not numero_cartao.get().strip():
                messagebox.showwarning("Campos vazios", "Preencha nome e número do cartão.")
                return

        elif metodo == "Dinheiro":
            try:
                pago = float(valor_entregue.get())
                if pago < total:
                    messagebox.showwarning("Valor insuficiente", "O valor entregue é menor que o total.")
                    return
            except:
                messagebox.showwarning("Inválido", "Digite um valor entregue válido.")
                return

        # Confirmação
        if not messagebox.askyesno("Confirmar Pagamento", f"Pagar R$ {total:.2f} via {metodo}?"):
            return

        # GERAR RECIBO (único recibo como combinado)
        itens = order.get_items()
        try:
            with open("recibo.txt", "w", encoding="utf-8") as f:
                f.write("===== RECIBO DE COMPRA =====\n\n")
                for nome, preco, qtd, desc in itens:
                    f.write(f"{nome} x{qtd} - R$ {preco * qtd:.2f}\n")
                f.write("\n------------------------------\n")
                f.write(f"TOTAL: R$ {total:.2f}\n")
                f.write(f"Método: {metodo}\n")
                if email:
                    f.write(f"Comprovante enviado para: {email}\n")
                if cliente_nome:
                    f.write(f"Reserva associada ao cliente: {cliente_nome}\n")
                f.write("=============================\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar recibo: {e}")
            # mesmo se falhar, tentamos prosseguir com limpeza/registro

        # Registrar pedido (se order.registrar_pedido existir)
        try:
            if hasattr(order, "registrar_pedido"):
                order.registrar_pedido(itens, total, metodo=metodo, email=email)
        except Exception:
            pass

        # Se cliente_nome informado, liberar reservas com esse nome (case-insensitive)
        if cliente_nome:
            nome_normalizado = cliente_nome.strip().lower()
            mesas_liberadas = []
            for mesa, reserva in list(RESERVAS.items()):
                if reserva and isinstance(reserva, dict):
                    if reserva.get("nome", "").strip().lower() == nome_normalizado:
                        RESERVAS[mesa] = None
                        mesas_liberadas.append(mesa)
            if mesas_liberadas:
                messagebox.showinfo("Reserva liberada", f"As seguintes mesas foram liberadas: {', '.join(mesas_liberadas)}")

        # Limpa comanda
        order.clear_order()

        messagebox.showinfo("Aprovado", f"Pagamento via {metodo} concluído!\nRecibo salvo em 'recibo.txt'.")

        tela.destroy()
        janela_anterior.deiconify()

    tk.Button(
        tela,
        text="FINALIZAR PAGAMENTO",
        font=("Georgia", 14, "bold"),
        bg=DOURADO,
        fg="black",
        width=30,
        command=finalizar_pagamento
    ).pack(pady=14)

    # Botão Voltar
    def voltar():
        tela.destroy()
        janela_anterior.deiconify()

    tk.Button(
        tela,
        text="Voltar",
        font=("Arial", 12),
        width=14,
        bg="#444",
        fg=WHITE,
        command=voltar
    ).pack(pady=6)

    tela.mainloop()
