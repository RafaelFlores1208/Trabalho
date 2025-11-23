# menu.py
from tkinter import *
from tkinter import messagebox
import os
import order

# Tente importar Pillow; se não estiver disponível usamos placeholders
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# caminho da imagem enviada por você (usada como placeholder)
IMAGE_FILE = "/mnt/data/17751107-d138-43f5-8cab-7b272178d5bf.png"

# dados do menu (nome, preco (float), descricao, imagem_path)
MENU_ITENS = [
    {"nome": "Entradinha Camarão à Milanesa", "preco": 76.00,
     "desc": "Camarão à milanesa com gergelim. Acompanha molho tártaro.", "img": IMAGE_FILE},
    {"nome": "Entradinha Isca de Peixe", "preco": 74.00,
     "desc": "Iscas de peixe à milanesa com gergelim e molho tártaro.", "img": IMAGE_FILE},
    {"nome": "Entradinha de Filé aos Queijos", "preco": 74.00,
     "desc": "Cubos de filé com molho de queijos. Acompanha torradas.", "img": IMAGE_FILE},
    {"nome": "Entradinha Filé com Fritas", "preco": 67.00,
     "desc": "Cubos de filé, refogado com cebola roxa e molho especial.", "img": IMAGE_FILE},
]

def create_menu_page(parent):
    """Cria a página de menu dentro do frame `parent`."""
    # limpar conteúdo anterior
    for w in parent.winfo_children():
        w.destroy()

    page = Frame(parent, bg="#1A1512")
    page.pack(fill="both", expand=True)

    # título
    Label(page, text="Cardápio — Selecione os itens", font=("Georgia", 20, "bold"),
          fg="white", bg="#1A1512").pack(anchor="w", padx=16, pady=(12,6))

    # área scroll
    container = Frame(page, bg="#1A1512")
    container.pack(fill="both", expand=True, padx=12, pady=8)

    canvas = Canvas(container, bg="#1A1512", highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg="#1A1512")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # referências de imagens para evitar coleta de lixo
    photos = []

    # Lista de variáveis para checkboxes (tupla: (var, item_index))
    checkbox_vars = []

    for idx, item in enumerate(MENU_ITENS):
        card = Frame(scroll_frame, bg="white", bd=0, relief="flat")
        card.pack(fill="x", pady=8, padx=12)

        # imagem (lado esquerdo)
        if PIL_AVAILABLE and item.get("img") and os.path.exists(item["img"]):
            try:
                im = Image.open(item["img"]).resize((260, 150))
                ph = ImageTk.PhotoImage(im)
                photos.append(ph)
                Label(card, image=ph, bg="white").pack(side="left", padx=8, pady=8)
            except Exception:
                # fallback para placeholder
                ph = None
        else:
            ph = None

        if ph is None:
            placeholder = Frame(card, width=260, height=150, bg="#E6E6E6")
            placeholder.pack_propagate(False)
            placeholder.pack(side="left", padx=8, pady=8)
            Label(placeholder, text="Imagem", bg="#E6E6E6").pack(expand=True)

        # texto e controles (direita)
        right = Frame(card, bg="white")
        right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        Label(right, text=item["nome"], bg="white", fg="#222",
              font=("Georgia", 14, "bold"), anchor="w").pack(fill="x")
        Label(right, text=f"R$ {item['preco']:.2f}", bg="white", fg="#444",
              font=("Georgia", 12)).pack(anchor="w", pady=(4,2))
        Label(right, text=item["desc"], bg="white", fg="#555",
              font=("Georgia", 11), wraplength=480, justify="left").pack(anchor="w", pady=(4,6))

        # checkbox para seleção
        var = IntVar(value=0)
        chk = Checkbutton(right, text="Selecionar", variable=var, bg="white", anchor="w")
        chk.pack(anchor="w", pady=(4,0))

        checkbox_vars.append((var, idx))

    # botão para abrir diálogo de quantidades
    btn_frame = Frame(page, bg="#1A1512")
    btn_frame.pack(fill="x", padx=16, pady=(6,16))
    add_selected_btn = Button(btn_frame, text="Adicionar selecionados à comanda",
                              bg="#F4D465", fg="#141107", font=("Georgia", 12, "bold"),
                              relief="flat", cursor="hand2",
                              command=lambda: _open_quantity_dialog(parent, checkbox_vars, photos))
    add_selected_btn.pack(side="right")

    # manter ref para fotos (para evitar garbage collection)
    page.photos = photos
    return page

def _open_quantity_dialog(parent, checkbox_vars, photos_ref):
    """Abre um Toplevel onde o usuário define quantidade para cada item selecionado."""
    selected = [(var, idx) for var, idx in checkbox_vars if var.get() == 1]
    if not selected:
        messagebox.showinfo("Nenhum item", "Por favor selecione ao menos um item.")
        return

    # criar janela modal
    dlg = Toplevel(parent)
    dlg.title("Quantidade dos Itens Selecionados")
    dlg.geometry("420x350")
    dlg.transient(parent)
    dlg.grab_set()

    Label(dlg, text="Defina a quantidade para cada item:", font=("Georgia", 12, "bold")).pack(anchor="w", padx=12, pady=8)

    entries = []  # tuplas (idx, Spinbox)
    body = Frame(dlg)
    body.pack(fill="both", expand=True, padx=12, pady=6)

    for var, idx in selected:
        item = MENU_ITENS[idx]
        row = Frame(body)
        row.pack(fill="x", pady=6)

        Label(row, text=item["nome"], anchor="w", justify="left", wraplength=220).pack(side="left", fill="x", expand=True)
        sp = Spinbox(row, from_=1, to=20, width=4)
        sp.pack(side="right", padx=6)
        entries.append((idx, sp))

    # Botões OK / Cancel
    btns = Frame(dlg)
    btns.pack(fill="x", pady=8)
    def on_ok():
        # Adiciona todos os itens ao order (agrupando)
        for idx, sp in entries:
            qty = int(sp.get())
            item = MENU_ITENS[idx]
            order.add_item(item["nome"], item["preco"], qty, desc=item.get("desc",""))
        dlg.destroy()
        messagebox.showinfo("Adicionado", "Itens adicionados à comanda com sucesso.")

    Button(btns, text="Adicionar à Comanda", bg="#1A1512", fg="white", command=on_ok).pack(side="right", padx=8)
    Button(btns, text="Cancelar", command=dlg.destroy).pack(side="right")

