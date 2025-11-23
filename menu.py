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
# OBS: O caminho IMAGE_FILE deve ser alterado para um caminho acessível no seu ambiente.
IMAGE_FILE = "/mnt/data/17751107-d138-43f5-8cab-7b272178d5bf.png" 

# Dourado Polido para destaque
DORADO_POLIDO = "#BEA95B"
# Cor de Fundo Escura (Ébano)
BG_ESCuro = "#1A1512"

# dados do menu (nome, preco (float), descricao, imagem_path)
# ... (Seu dicionário MENU_ITENS permanece o mesmo aqui) ...
IMAGE_PLACEHOLDER = ""

MENU_ITENS = {
    "Entradas": [
        {
            "nome": "Camarão à Milanesa com Gergelim",
            "preço": 76.00,
            "desc": "Camarões empanados na milanesa com toque de gergelim. Acompanha molho tártaro artesanal.",
            "img":"imagens/camara_enter.png"
        },
        {
            "nome": "Isca de Peixe Crocante",
            "preço": 74.00,
            "desc": "Iscas de peixe branco empanadas com gergelim, servidas com molho tártaro. Uma entrada leve e saborosa.",
            "img":"imagens/isca_enter.png"
        },
        {
            "nome": "Filé Mignon aos Queijos",
            "preço": 74.00,
            "desc": "Cubos de filé mignon grelhados, imersos em um cremoso molho de quatro queijos. Acompanha torradas de pão de fermentação natural.",
            "img":"imagens/fileaomolho_enter.png"
        },
        {
            "nome": "Filé com Fritas Ébano",
            "preço": 67.00,
            "desc": "Cubos de filé mignon refogados com cebola roxa e um toque de molho especial da casa. Acompanha batatas fritas.",
            "img": "imagens/fritasecarne_enter.png"
        }
    ],
    
    "Pratos Principais": [
        {
            "nome": "Salmão com Risoto de Limão Siciliano",
            "preço": 125.00,
            "desc": "Salmão fresco grelhado no ponto perfeito, servido sobre um risoto cremoso com raspas e suco de limão siciliano.",
            "img": "imagens/salmao_p.png"
        },
        {
            "nome": "Mignon ao Molho de Vinho Tinto e Purê Trufado",
            "preço": 149.00,
            "desc": "Medalhão de filé mignon com redução de vinho tinto. Acompanha purê de batatas com azeite trufado.",
            "img": "imagens/mion_p.png"
        },
        {
            "nome": "Ravioli de Ossobuco",
            "preço": 118.00,
            "desc": "Massa artesanal recheada com ossobuco cozido lentamente, servida na manteiga de sálvia com um toque de queijo parmesão.",
            "img": "imagens/ravioli_p.png"
        }
    ],
    
    "Acompanhamentos": [
        {
            "nome": "Arroz de Brócolis e Amêndoas",
            "preço": 35.00,
            "desc": "Arroz soltinho com brócolis frescos e crocantes lascas de amêndoas tostadas.",
            "img": "imagens/arroz_a.png"
        },
        {
            "nome": "Batatas Rústicas",
            "preço": 32.00,
            "desc": "Batatas cortadas em estilo rústico, assadas com azeite, alecrim fresco e alho.",
            "img": "imagens/batata_a.png"
        },
        {
            "nome": "Mix de Legumes Grelhados",
            "preço": 38.00,
            "desc": "Seleção de legumes sazonais grelhados na brasa e temperados com azeite de ervas finas.",
            "img": "imagens/carneleg_a.png"
        }
    ],
    
    "Bebidas": [
        {
            "nome": "Vinho Tinto Reserva",
            "preço": 180.00,
            "desc": "Consultar nosso sommelier para a seleção da safra do dia. Servido em taça de cristal.",
            "img": "imagens/vinhotinto.png"
        },
        {
            "nome": "Coquetel Clássico",
            "preço": 45.00,
            "desc": "Old Fashioned, Negroni ou Dry Martini. Clássicos feitos com destilados premium e guarnições frescas.",
            "img": "imagens/coquetel.png"
        },
        {
            "nome": "Suco de Frutas Vermelhas",
            "preço": 22.00,
            "desc": "Suco natural e refrescante feito com uma seleção de morangos, amoras e framboesas frescas.",
            "img": "imagens/sucovermelho.png"
        },
        {
            "nome": "Spritz Refrescante Sem Álcool",
            "preço": 35.00,
            "desc": "Bebida leve e gaseificada com toques cítricos e botânicos, servida com especiarias. Perfeito para acompanhar qualquer prato.",
            "img": "imagens/suco.png"
        }
    ],

    "Sobremesas (Estilo Ébano)": [
        {
            "nome": "Esfera de Chocolate Ébano",
            "preço": 48.00,
            "desc": "Esfera de chocolate amargo 70% recheada com mousse de chocolate. Servida com coulis quente de cereja negra e ouro comestível.",
            "img": "imagens/esferera.png"
        },
        {
            "nome": "Tiramisu de Carvão e Café",
            "preço": 45.00,
            "desc": "Camadas de queijo mascarpone e biscoitos umedecidos no café espresso. O toque 'Ébano' vem do leve pó de carvão ativado e cacau.",
            "img": "imagens/tira.png"
        },
        {
            "nome": "Creme Brûlée de Fava Tonka",
            "preço": 42.00,
            "desc": "Creme brûlée delicado com o aroma exótico da fava tonka. Finalizado com uma camada crocante de açúcar caramelizado e frutas escuras.",
            "img": "imagens/creme.png"
        }
    ]
}


def create_menu_page(parent):
    """Cria a página de menu dentro do frame `parent`."""
    # limpar conteúdo anterior
    for w in parent.winfo_children():
        w.destroy()

    page = Frame(parent, bg=BG_ESCuro)
    page.pack(fill="both", expand=True)

    # título
    Label(page, text="Cardápio — Selecione os itens", font=("Georgia", 20, "bold"),
          fg=DORADO_POLIDO, bg=BG_ESCuro).pack(anchor="w", padx=16, pady=(12,6))

    # área scroll
    container = Frame(page, bg=BG_ESCuro)
    container.pack(fill="both", expand=True, padx=12, pady=8)

    canvas = Canvas(container, bg=BG_ESCuro, highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg=BG_ESCuro)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # Adicionar este binding para o canvas se redimensionar horizontalmente junto com a janela
    def on_canvas_resize(event):
        canvas.itemconfig(canvas.find_all()[0], width=event.width)
        
    canvas.bind('<Configure>', on_canvas_resize)
    canvas_window = canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # referências de imagens para evitar coleta de lixo
    photos = []
    # Lista de variáveis para checkboxes (tupla: (var, item_data_dictionary))
    checkbox_vars = []
    
    # ID global para rastrear os itens no diálogo de quantidade (necessário para o Spinbox)
    global_item_id = 0

    # ----------------------------------------------------
    # CORREÇÃO: Itera sobre as categorias (chaves) e as listas de itens (valores)
    for category_name, items_list in MENU_ITENS.items():
        # Título da Categoria
        Label(scroll_frame, text=category_name, font=("Georgia", 16, "underline"),
              fg="#BEA95B", bg=BG_ESCuro).pack(anchor="w", padx=12, pady=(15, 5))

        # Itera sobre os itens dentro de cada lista de categoria
        for item in items_list:
            card = Frame(scroll_frame, bg="white", bd=0, relief="flat")
            card.pack(fill="x", pady=6, padx=12)
            card.columnconfigure(1, weight=1) # Permite que a coluna de texto se expanda

            # --- Coluna 0: Imagem (lado esquerdo) ---
            image_path = item.get("img")
            ph = None
            if PIL_AVAILABLE and image_path and os.path.exists(image_path):
                try:
                    im = Image.open(image_path).resize((180, 100)) # Reduzi o tamanho para caber melhor
                    ph = ImageTk.PhotoImage(im)
                    photos.append(ph)
                    Label(card, image=ph, bg="white").grid(row=0, column=0, rowspan=4, padx=8, pady=8, sticky="n")
                except Exception:
                    ph = None
            
            if ph is None:
                placeholder = Frame(card, width=180, height=100, bg="#E6E6E6")
                placeholder.grid(row=0, column=0, rowspan=4, padx=8, pady=8, sticky="n")
                placeholder.pack_propagate(False)
                Label(placeholder, text="Imagem", bg="#E6E6E6", fg="#777").pack(expand=True)


            # --- Coluna 1: Texto e Controles (Direita) ---
            right = Frame(card, bg="white")
            right.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=8, pady=8)
            right.columnconfigure(0, weight=1) # Permite que o texto se expanda
            
            # Linha do Nome e Preço
            top_row = Frame(right, bg="white")
            top_row.pack(fill="x")
            
            Label(top_row, text=item["nome"], bg="white", fg="#222",
                  font=("Georgia", 14, "bold"), anchor="w").pack(side="left", fill="x", expand=True)
            
            # Preço Dourado
            Label(top_row, text=f"R$ {item['preço']:.2f}", bg="white", fg=DORADO_POLIDO,
                  font=("Georgia", 14, "bold")).pack(side="right", padx=(10, 0))
            
            # Descrição
            Label(right, text=item["desc"], bg="white", fg="#555",
                  font=("Georgia", 11), wraplength=450, justify="left").pack(fill="x", pady=(4,6))

            # Checkbox para seleção
            var = IntVar(value=0)
            chk = Checkbutton(right, text="Selecionar", variable=var, bg="white", anchor="w")
            chk.pack(anchor="w", pady=(4,0))

            # Adiciona o dicionário do item em vez do índice simples
            checkbox_vars.append((var, item)) 
            
            global_item_id += 1 # Aumenta o ID para cada item

    # botão para abrir diálogo de quantidades
    btn_frame = Frame(page, bg=BG_ESCuro)
    btn_frame.pack(fill="x", padx=16, pady=(6,16))
    add_selected_btn = Button(btn_frame, text="Adicionar selecionados à comanda",
                              bg=DORADO_POLIDO, fg="#141107", font=("Georgia", 12, "bold"),
                              relief="flat", cursor="hand2",
                              command=lambda: _open_quantity_dialog(parent, checkbox_vars))
    add_selected_btn.pack(side="right")

    # manter ref para fotos (para evitar garbage collection)
    page.photos = photos
    return page

def _open_quantity_dialog(parent, checkbox_vars):
    """Abre um Toplevel onde o usuário define quantidade para cada item selecionado."""
    
    # Filtrar apenas os itens selecionados (var.get() == 1)
    selected_items_data = [item_data for var, item_data in checkbox_vars if var.get() == 1]
    
    if not selected_items_data:
        messagebox.showinfo("Nenhum item", "Por favor selecione ao menos um item.")
        return

    # Criar janela modal
    dlg = Toplevel(parent)
    dlg.title("Quantidade dos Itens Selecionados")
    # Ajustei o tamanho para melhor visualização
    dlg.geometry("450x400") 
    dlg.transient(parent)
    dlg.grab_set()
    
    # Criar uma área de scroll dentro do diálogo se houver muitos itens
    dlg_canvas = Canvas(dlg)
    dlg_scrollbar = Scrollbar(dlg, orient="vertical", command=dlg_canvas.yview)
    dlg_scroll_frame = Frame(dlg_canvas)

    dlg_scroll_frame.bind("<Configure>", lambda e: dlg_canvas.configure(scrollregion=dlg_canvas.bbox("all")))
    dlg_canvas.create_window((0,0), window=dlg_scroll_frame, anchor="nw", width=420) 
    dlg_canvas.configure(yscrollcommand=dlg_scrollbar.set)

    dlg_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(10, 0))
    dlg_scrollbar.pack(side="right", fill="y")
    
    Label(dlg_scroll_frame, text="Defina a quantidade para cada item:", font=("Georgia", 12, "bold"), bg=dlg_scroll_frame.cget('bg')).pack(anchor="w", padx=12, pady=8)

    entries = []  # tuplas (item_data_dict, Spinbox)

    for item in selected_items_data:
        row = Frame(dlg_scroll_frame, bg=dlg_scroll_frame.cget('bg'))
        row.pack(fill="x", pady=4, padx=12)

        # Nome do item e preço
        Label(row, text=f"{item['nome']} (R$ {item['preço']:.2f})", anchor="w", justify="left", wraplength=280).pack(side="left", fill="x", expand=True)
        
        # Spinbox para quantidade
        sp = Spinbox(row, from_=1, to=20, width=4)
        sp.pack(side="right", padx=6)
        entries.append((item, sp))

    # Botões OK / Cancel
    btns = Frame(dlg)
    btns.pack(fill="x", pady=8)
    
    # Adicionar o padding correto aos botões
    Button(btns, text="Adicionar à Comanda", bg=BG_ESCuro, fg="white", 
           font=("Georgia", 11, "bold"), relief="flat", cursor="hand2",
           command=lambda: _add_items_to_order(entries, dlg)).pack(side="right", padx=12)
    Button(btns, text="Cancelar", command=dlg.destroy).pack(side="right", padx=8)

def _add_items_to_order(entries, dlg):
    """Função que adiciona os itens selecionados ao módulo de pedidos e fecha o diálogo."""
    # O módulo 'order' precisa ser definido (você pode precisar de um 'order.py' separado)
    
    items_added = 0
    for item, sp in entries:
        try:
            qty = int(sp.get())
            if qty > 0:
                # Chama a função no módulo 'order' (assumindo que existe)
                # order.add_item(nome, preco, quantidade, desc)
                # Note: Se 'order' não estiver definido, esta linha causará um erro
                # order.add_item(item["nome"], item["preço"], qty, desc=item.get("desc",""))
                items_added += 1
        except ValueError:
            messagebox.showerror("Erro de Quantidade", f"Quantidade inválida para {item['nome']}. Use apenas números inteiros.")
            return

    if items_added > 0:
        dlg.destroy()
        messagebox.showinfo("Adicionado", f"{items_added} itens adicionados à comanda com sucesso.")
    else:
        messagebox.showinfo("Nenhum Item Adicionado", "Nenhum item foi adicionado. Verifique as quantidades.")