# reserva_mesa.py
# Tela de reservas de mesas (simples, em memória) integrada ao Dashboard
# Mantém 10 mesas (Mesa 1..Mesa 10) e permite criar, visualizar e cancelar reservas

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Tema (mantém o estilo do projeto)
BG = "#1A1512"
DOURADO = "#F4D465"
CARD_BG = "#2A2218"
WHITE = "white"

# Estado simples em memória: dicionário "Mesa X" -> reserva ou None
RESERVAS = {f"Mesa {i}": None for i in range(1, 11)}


def criar_reserva_page(parent_frame):
    """Cria a página de reservas dentro do frame de conteúdo do Dashboard.
    Armazena reservas em memória no dicionário RESERVAS.
    Campos de reserva: nome, telefone, mesa, data, horário, observação, número de pessoas.
    """
    # limpa conteúdo
    for w in parent_frame.winfo_children():
        w.destroy()

    container = tk.Frame(parent_frame, bg=BG)
    container.pack(fill="both", expand=True)

    # Título
    tk.Label(container, text="Reservas de Mesas", font=("Georgia", 20, "bold"),
             bg=BG, fg=DOURADO).pack(pady=(12, 6))

    main = tk.Frame(container, bg=BG)
    main.pack(fill="both", expand=True, padx=12, pady=8)

    # Left: lista de mesas
    left = tk.Frame(main, bg=BG)
    left.pack(side="left", fill="both", expand=True)

    tk.Label(left, text="Mesas", font=("Georgia", 14, "bold"), bg=BG, fg=WHITE).pack(anchor="w", pady=(0,6))

    mesas_frame = tk.Frame(left, bg=BG)
    mesas_frame.pack(fill="both", expand=True)

    # Right: formulário de criação de reserva
    right = tk.Frame(main, bg=BG)
    right.pack(side="right", fill="y", padx=(20,0))

    tk.Label(right, text="Criar / Editar Reserva", font=("Georgia", 14, "bold"), bg=BG, fg=WHITE).pack(anchor="w", pady=(0,6))

    # Formulário
    form = tk.Frame(right, bg=BG)
    form.pack(fill="y", pady=6)

    tk.Label(form, text="Nome do Cliente:", bg=BG, fg=WHITE).grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(form, width=30)
    entry_nome.grid(row=0, column=1, pady=4)

    tk.Label(form, text="Telefone:", bg=BG, fg=WHITE).grid(row=1, column=0, sticky="w")
    entry_tel = tk.Entry(form, width=30)
    entry_tel.grid(row=1, column=1, pady=4)

    tk.Label(form, text="Mesa:", bg=BG, fg=WHITE).grid(row=2, column=0, sticky="w")
    mesa_var = tk.StringVar(value="Mesa 1")
    mesa_choices = [f"Mesa {i}" for i in range(1, 11)]
    mesa_menu = ttk.Combobox(form, values=mesa_choices, textvariable=mesa_var, state="readonly", width=28)
    mesa_menu.grid(row=2, column=1, pady=4)

    tk.Label(form, text="Data (DD/MM/AAAA):", bg=BG, fg=WHITE).grid(row=3, column=0, sticky="w")
    entry_data = tk.Entry(form, width=30)
    entry_data.grid(row=3, column=1, pady=4)

    tk.Label(form, text="Horário (HH:MM):", bg=BG, fg=WHITE).grid(row=4, column=0, sticky="w")
    entry_hora = tk.Entry(form, width=30)
    entry_hora.grid(row=4, column=1, pady=4)

    tk.Label(form, text="Número de pessoas:", bg=BG, fg=WHITE).grid(row=5, column=0, sticky="w")
    spin_pessoas = tk.Spinbox(form, from_=1, to=20, width=5)
    spin_pessoas.grid(row=5, column=1, sticky="w", pady=4)

    tk.Label(form, text="Observação:", bg=BG, fg=WHITE).grid(row=6, column=0, sticky="nw")
    txt_obs = tk.Text(form, width=22, height=4)
    txt_obs.grid(row=6, column=1, pady=4)

    # Funções auxiliares
    def validar_data(data_text):
        try:
            datetime.strptime(data_text, "%d/%m/%Y")
            return True
        except:
            return False

    def validar_hora(hora_text):
        try:
            datetime.strptime(hora_text, "%H:%M")
            return True
        except:
            return False

    def atualizar_mesas():
        # limpa quadro
        for w in mesas_frame.winfo_children():
            w.destroy()

        # exibe todas as mesas com status
        for i in range(1, 11):
            m = f"Mesa {i}"
            frame = tk.Frame(mesas_frame, bg=CARD_BG if RESERVAS[m] else BG, pady=6)
            frame.pack(fill="x", padx=4, pady=2)

            status = "Reservada" if RESERVAS[m] else "Livre"
            emoji = "🟡" if RESERVAS[m] else "🟢"

            lbl = tk.Label(frame, text=f"{m}  {emoji}", font=("Georgia", 12, "bold"), bg=frame["bg"], fg=DOURADO)
            lbl.pack(side="left", padx=8)

            if RESERVAS[m]:
                info = RESERVAS[m]
                info_text = f"{info['nome']} | {info['data']} {info['hora']} | {info['pessoas']}p"
                tk.Label(frame, text=info_text, bg=frame["bg"], fg=WHITE).pack(side="left", padx=8)

                tk.Button(frame, text="Cancelar", fg="white", bg="#b03a2e", relief="flat",
                          command=lambda mesa=m: cancelar_reserva(mesa)).pack(side="right", padx=6)
            else:
                tk.Button(frame, text="Reservar", fg="black", bg=DOURADO, relief="flat",
                          command=lambda mesa=m: preencher_form_para_mesa(mesa)).pack(side="right", padx=6)

    def preencher_form_para_mesa(mesa):
        # seleciona a mesa no combobox e foca nome
        mesa_var.set(mesa)
        entry_nome.focus_set()

    def cancelar_reserva(mesa):
        if messagebox.askyesno("Cancelar Reserva", f"Deseja cancelar a reserva de {mesa}?"):
            RESERVAS[mesa] = None
            atualizar_mesas()
            messagebox.showinfo("Cancelado", f"Reserva de {mesa} cancelada.")

    def criar_reserva():
        nome = entry_nome.get().strip()
        tel = entry_tel.get().strip()
        mesa = mesa_var.get()
        data = entry_data.get().strip()
        hora = entry_hora.get().strip()
        pessoas = spin_pessoas.get()
        obs = txt_obs.get("1.0", "end").strip()

        if not nome:
            messagebox.showwarning("Dados incompletos", "Preencha o nome do cliente")
            return
        if not tel:
            messagebox.showwarning("Dados incompletos", "Preencha o telefone")
            return
        if not validar_data(data):
            messagebox.showwarning("Data inválida", "Use o formato DD/MM/AAAA")
            return
        if not validar_hora(hora):
            messagebox.showwarning("Horário inválido", "Use o formato HH:MM")
            return

        # Verifica se já há reserva na mesa
        if RESERVAS[mesa]:
            if not messagebox.askyesno("Substituir Reserva", f"{mesa} já está reservada. Substituir?"):
                return

        RESERVAS[mesa] = {
            "nome": nome,
            "telefone": tel,
            "data": data,
            "hora": hora,
            "pessoas": pessoas,
            "observacao": obs,
            "criada_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        messagebox.showinfo("Reserva criada", f"Reserva para {nome} em {mesa} criada com sucesso.")
        # limpa form
        entry_nome.delete(0, "end")
        entry_tel.delete(0, "end")
        entry_data.delete(0, "end")
        entry_hora.delete(0, "end")
        txt_obs.delete("1.0", "end")
        spin_pessoas.delete(0, "end")
        spin_pessoas.insert(0, "1")

        atualizar_mesas()

    # Botões do formulário
    btn_frame = tk.Frame(right, bg=BG)
    btn_frame.pack(fill="x", pady=6)

    tk.Button(btn_frame, text="Criar Reserva", bg=DOURADO, fg="black", width=18, command=criar_reserva).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Limpar", bg="#555", fg="white", width=10,
              command=lambda: (entry_nome.delete(0, 'end'), entry_tel.delete(0, 'end'), entry_data.delete(0, 'end'), entry_hora.delete(0, 'end'), txt_obs.delete('1.0','end'), spin_pessoas.delete(0,'end'), spin_pessoas.insert(0,'1'))).pack(side="left", padx=6)

    # Inicializa display
    atualizar_mesas()

    return container
