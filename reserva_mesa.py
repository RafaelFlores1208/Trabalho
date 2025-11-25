# reserva_mesa.py
# Sistema de reservas estilizado com Tkinter

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ========= 🎨 PALETA DE CORES ==========
BG = "#1A1512"
DOURADO = "#F4D465"
CARD_BG = "#2A2218"
WHITE = "white"
CANCEL = "#b03a2e"
BTN_HOVER = "#e8c25e"

# ========= 📌 BANCO DE RESERVAS (em memória) =========
RESERVAS = {f"Mesa {i}": None for i in range(1, 11)}


# ============= ⭐ FUNÇÕES DE UI AUXILIARES =====================

def hover_on(e):
    e.widget["bg"] = BTN_HOVER

def hover_off(e, original):
    e.widget["bg"] = original


def criar_titulo(parent, texto):
    """ Label de título padrão do sistema """
    return tk.Label(parent, text=texto, font=("Georgia", 20, "bold"), bg=BG, fg=DOURADO, pady=10)


def criar_subtitulo(parent, texto):
    """ Subtítulo bonito """
    return tk.Label(parent, text=texto, font=("Georgia", 14, "bold"), bg=BG, fg=WHITE, pady=4)


# ====================================================================
# ========================== RESERVA PAGE =============================
# ====================================================================

def criar_reserva_page(parent_frame):

    # LIMPA TELA
    for w in parent_frame.winfo_children():
        w.destroy()

    # ---------- CONTAINER PRINCIPAL ----------
    container = tk.Frame(parent_frame, bg=BG)
    container.pack(fill="both", expand=True)

    criar_titulo(container, "Reservas de Mesas").pack()

    main = tk.Frame(container, bg=BG)
    main.pack(fill="both", expand=True, padx=20, pady=10)

    # ============== 📋 LISTA DE MESAS ==============
    left = tk.Frame(main, bg=BG)
    left.pack(side="left", fill="both", expand=True)

    criar_subtitulo(left, "Mesas").pack(anchor="w")

    mesas_frame = tk.Frame(left, bg=BG)
    mesas_frame.pack(fill="both", expand=True)

    # ============== 📝 FORMULÁRIO ==============
    right = tk.Frame(main, bg=BG)
    right.pack(side="right", fill="y", padx=(30, 0))

    criar_subtitulo(right, "Criar / Editar Reserva").pack(anchor="w")

    form = tk.Frame(right, bg=BG)
    form.pack(fill="y", pady=8)

    # -------- Inputs --------
    campos = [
        ("Nome do Cliente:", "nome"),
        ("Telefone:", "tel"),
        ("Data (DD/MM/AAAA):", "data"),
        ("Horário (HH:MM):", "hora"),
    ]

    entries = {}

    for i, (label, key) in enumerate(campos):
        tk.Label(form, text=label, bg=BG, fg=WHITE).grid(row=i, column=0, sticky="w", pady=4)
        entry = tk.Entry(form, width=30)
        entry.grid(row=i, column=1, pady=4)
        entries[key] = entry

    # Mesa
    tk.Label(form, text="Mesa:", bg=BG, fg=WHITE).grid(row=2, column=0, sticky="w")
    mesa_var = tk.StringVar(value="Mesa 1")
    mesa_choices = [f"Mesa {i}" for i in range(1, 11)]
    mesa_menu = ttk.Combobox(form, values=mesa_choices, textvariable=mesa_var, state="readonly", width=28)
    mesa_menu.grid(row=2, column=1, pady=4)

    # Pessoas
    tk.Label(form, text="Número de pessoas:", bg=BG, fg=WHITE).grid(row=5, column=0, sticky="w")
    spin_pessoas = tk.Spinbox(form, from_=1, to=20, width=5)
    spin_pessoas.grid(row=5, column=1, sticky="w", pady=4)

    # Observação
    tk.Label(form, text="Observação:", bg=BG, fg=WHITE).grid(row=6, column=0, sticky="nw")
    txt_obs = tk.Text(form, width=22, height=4)
    txt_obs.grid(row=6, column=1, pady=4)

    # ====================================================================
    #                     FUNÇÕES INTERNAS
    # ====================================================================

    def validar_data(texto):
        try:
            datetime.strptime(texto, "%d/%m/%Y")
            return True
        except:
            return False

    def validar_hora(texto):
        try:
            datetime.strptime(texto, "%H:%M")
            return True
        except:
            return False

    def preencher_form_para_mesa(mesa):
        mesa_var.set(mesa)
        entries["nome"].focus_set()

    def cancelar_reserva(mesa):
        if messagebox.askyesno("Cancelar Reserva", f"Deseja cancelar a reserva de {mesa}?"):
            RESERVAS[mesa] = None
            atualizar_mesas()
            messagebox.showinfo("Cancelado", f"Reserva de {mesa} cancelada.")

    def criar_reserva():
        nome = entries["nome"].get().strip()
        tel = entries["tel"].get().strip()
        mesa = mesa_var.get()
        data = entries["data"].get().strip()
        hora = entries["hora"].get().strip()
        pessoas = spin_pessoas.get()
        obs = txt_obs.get("1.0", "end").strip()

        # VALIDAÇÕES
        if not nome:
            return messagebox.showwarning("Dados incompletos", "Preencha o nome.")
        if not tel:
            return messagebox.showwarning("Dados incompletos", "Preencha o telefone.")
        if not validar_data(data):
            return messagebox.showwarning("Data inválida", "Formato correto: DD/MM/AAAA")
        if not validar_hora(hora):
            return messagebox.showwarning("Horário inválido", "Formato correto: HH:MM")

        # Se mesa já reservada
        if RESERVAS[mesa]:
            if not messagebox.askyesno("Substituir Reserva", f"{mesa} já está reservada. Substituir?"):
                return

        # CRIA RESERVA
        RESERVAS[mesa] = {
            "nome": nome,
            "telefone": tel,
            "data": data,
            "hora": hora,
            "pessoas": pessoas,
            "observacao": obs,
            "criada_em": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        messagebox.showinfo("Sucesso", f"Reserva criada para {nome}!")

        # LIMPA
        for e in entries.values():
            e.delete(0, "end")
        txt_obs.delete("1.0", "end")
        spin_pessoas.delete(0, "end")
        spin_pessoas.insert(0, "1")

        atualizar_mesas()

    # ====================================================================
    #                    BOTÕES DO FORMULÁRIO
    # ====================================================================

    btn_frame = tk.Frame(right, bg=BG)
    btn_frame.pack(fill="x", pady=10)

    btn_reservar = tk.Button(btn_frame, text="Criar Reserva", bg=DOURADO, fg="black", width=18,
                             relief="flat", command=criar_reserva)
    btn_reservar.pack(side="left", padx=5)

    btn_limpar = tk.Button(btn_frame, text="Limpar", bg="#555", fg="white", width=10, relief="flat",
                           command=lambda: (
                               [e.delete(0, 'end') for e in entries.values()],
                               txt_obs.delete("1.0", "end"),
                               spin_pessoas.delete(0, "end"),
                               spin_pessoas.insert(0, "1")
                           ))
    btn_limpar.pack(side="left", padx=5)

    # Efeitos hover
    for btn, original in [(btn_reservar, DOURADO), (btn_limpar, "#555")]:
        btn.bind("<Enter>", lambda e, o=original: hover_on(e))
        btn.bind("<Leave>", lambda e, o=original: hover_off(e, o))

    # ====================================================================
    #                  LISTAGEM DE MESAS
    # ====================================================================

    def atualizar_mesas():
        for w in mesas_frame.winfo_children():
            w.destroy()

        for i in range(1, 11):
            mesa = f"Mesa {i}"
            reservada = RESERVAS[mesa]

            card = tk.Frame(mesas_frame, bg=CARD_BG if reservada else BG, padx=8, pady=6)
            card.pack(fill="x", pady=4)

            status = "🟡 Reservada" if reservada else "🟢 Livre"

            tk.Label(card, text=f"{mesa}  {status}", font=("Georgia", 12, "bold"),
                     bg=card["bg"], fg=DOURADO).pack(side="left")

            if reservada:
                info = f"{reservada['nome']} | {reservada['data']} {reservada['hora']} | {reservada['pessoas']}p"
                tk.Label(card, text=info, bg=card["bg"], fg=WHITE).pack(side="left", padx=10)

                btn_cancelar = tk.Button(card, text="Cancelar", bg=CANCEL, fg="white", relief="flat",
                                         command=lambda m=mesa: cancelar_reserva(m))
                btn_cancelar.pack(side="right")

            else:
                btn_reservar_mesa = tk.Button(card, text="Reservar", bg=DOURADO, fg="black", relief="flat",
                                              command=lambda m=mesa: preencher_form_para_mesa(m))
                btn_reservar_mesa.pack(side="right")

    atualizar_mesas()

    return container
