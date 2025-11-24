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

# --- PALETA DE CORES ---
DORADO_POLIDO = "#BEA95B"
BG_ESCuro = "#1A1512" 
TEXTO_SUAVE = "#444444" 
CATEGORIA_HEADER = "#D4AF37"

# dados do menu (nome, preco (float), descricao, imagem_path)
MENU_ITENS = {
    "🥂 Entradas": [
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
    
    "🍽️ Pratos Principais": [
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
    
    "🍚 Acompanhamentos": [
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
    
    "🍷 Bebidas": [
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

    "✨ Sobremesas (Estilo Ébano)": [
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


# ==========================================================
# 3. FUNÇÕES AUXILIARES (Definidas antes de serem chamadas!)
# ==========================================================

# Importa a função create_compra_page do módulo 'compra'
try:
    from compra import create_compra_page
except ImportError:
    def create_compra_page(parent, usuario_logado=False, email_pix="rafael@email.com"):
        messagebox.showwarning("Erro", "Módulo 'compra.py' não encontrado ou não importado.")
        
def _add_items_to_order(entries, dlg, parent_window):
    """
    Função que adiciona os itens selecionados ao módulo de pedidos, 
    fecha o diálogo e atualiza a tela de compra.
    """
    items_added = 0
    for item, sp in entries:
        try:
            qty = int(sp.get())
            if qty > 0:
                # CORREÇÃO: Adiciona o item ao order.py
                order.add_item(item["nome"], item["preço"], qty, desc=item.get("desc",""))
                items_added += 1
        except ValueError:
            messagebox.showerror("Erro de Quantidade", f"Quantidade inválida para {item['nome']}. Use apenas números inteiros.")
            return

    if items_added > 0:
        dlg.destroy()
        messagebox.showinfo("Adicionado", f"{items_added} itens adicionados à comanda com sucesso.")
        
        # Recarrega a página da comanda após a adição para visualização imediata
        create_compra_page(parent_window) 
    else:
        messagebox.showinfo("Nenhum Item Adicionado", "Nenhum item foi adicionado. Verifique as quantidades.")


def _open_quantity_dialog(parent, checkbox_vars):
    """Abre um Toplevel onde o usuário define quantidade para cada item selecionado."""
    
    selected_items_data = [item_data for var, item_data in checkbox_vars if var.get() == 1]
    
    if not selected_items_data:
        messagebox.showinfo("Nenhum item", "Por favor selecione ao menos um item.")
        return

    # Criar janela modal
    dlg = Toplevel(parent)
    dlg.title("Quantidade dos Itens Selecionados")
    dlg.geometry("450x400") 
    dlg.transient(parent)
    dlg.grab_set()
    
    # Configuração do Scroll
    dlg_canvas = Canvas(dlg)
    dlg_scrollbar = Scrollbar(dlg, orient="vertical", command=dlg_canvas.yview)
    dlg_scroll_frame = Frame(dlg_canvas)

    dlg_scroll_frame.bind("<Configure>", lambda e: dlg_canvas.configure(scrollregion=dlg_canvas.bbox("all")))
    dlg_canvas.create_window((0,0), window=dlg_scroll_frame, anchor="nw", width=420) 
    dlg_canvas.configure(yscrollcommand=dlg_scrollbar.set)

    dlg_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(10, 0))
    dlg_scrollbar.pack(side="right", fill="y")
    
    # Aplicando o tema na Toplevel
    dlg.config(bg=BG_ESCuro)
    dlg_scroll_frame.config(bg=BG_ESCuro)

    Label(dlg_scroll_frame, text="Defina a quantidade para cada item:", font=("Georgia", 12, "bold"), 
          bg=BG_ESCuro, fg=DORADO_POLIDO).pack(anchor="w", padx=12, pady=8)

    entries = []  # tuplas (item_data_dict, Spinbox)

    for item in selected_items_data:
        row = Frame(dlg_scroll_frame, bg=BG_ESCuro)
        row.pack(fill="x", pady=4, padx=12)

        # Nome do item e preço
        Label(row, text=f"{item['nome']} (R$ {item['preço']:.2f})", anchor="w", justify="left", 
              wraplength=280, bg=BG_ESCuro, fg="white").pack(side="left", fill="x", expand=True)
        
        # Spinbox para quantidade
        sp = Spinbox(row, from_=1, to=20, width=4, relief="flat", bg="#FFF", fg="#111")
        sp.pack(side="right", padx=6)
        entries.append((item, sp))

    # Botões OK / Cancel
    btns = Frame(dlg, bg=BG_ESCuro)
    btns.pack(fill="x", pady=8)
    
    # Botão de Adicionar
    Button(btns, text="Adicionar à Comanda", bg=DORADO_POLIDO, fg="#141107", 
           font=("Georgia", 11, "bold"), relief="flat", cursor="hand2",
           # Passamos 'parent' para a função de adição para que ela possa recarregar a tela
           command=lambda: _add_items_to_order(entries, dlg, parent)).pack(side="right", padx=12) 
           
    Button(btns, text="Cancelar", command=dlg.destroy, bg="#333", fg="white", relief="flat").pack(side="right", padx=8)


# ==========================================================
# 4. FUNÇÃO PRINCIPAL
# ==========================================================

def create_menu_page(parent):
    """Cria a página de menu dentro do frame `parent`."""
    for w in parent.winfo_children():
        w.destroy()

    page = Frame(parent, bg=BG_ESCuro)
    page.pack(fill="both", expand=True)

    Label(page, text="Cardápio — Selecione os itens", font=("Georgia", 24, "bold"),
          fg=CATEGORIA_HEADER, bg=BG_ESCuro).pack(anchor="w", padx=20, pady=(15, 8))
    

    # Área Scroll
    container = Frame(page, bg=BG_ESCuro)
    container.pack(fill="both", expand=True, padx=12, pady=0)

    canvas = Canvas(container, bg=BG_ESCuro, highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg=BG_ESCuro)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)
        
    canvas.bind('<Configure>', on_canvas_resize)
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    photos = []
    checkbox_vars = []
    
    # Tamanhos de imagem usados no seu código anterior (130x90)
    IMAGE_W = 130
    IMAGE_H = 90

    # Itera sobre as categorias
    for category_name, items_list in MENU_ITENS.items():
        # Título da Categoria: Efeito de Destaque
        category_frame = Frame(scroll_frame, bg=BG_ESCuro)
        category_frame.pack(fill="x", padx=12, pady=(20, 8))
        
        Label(category_frame, text=category_name.upper(), font=("Georgia", 18, "bold"),
              fg=CATEGORIA_HEADER, bg=BG_ESCuro).pack(side="left")
        
        # Linha Decorativa Dourada
        Frame(category_frame, height=2, bg=DORADO_POLIDO).pack(side="left", fill="x", expand=True, padx=(10, 0))


        # Itera sobre os itens
        for item in items_list:
            # FRAME DO CARD: Borda Fina Dourada
            card_wrapper = Frame(scroll_frame, bg=DORADO_POLIDO, padx=1, pady=1) 
            card_wrapper.pack(fill="x", pady=6, padx=6)

            card = Frame(card_wrapper, bg="#FFFFFF", bd=0, relief="flat")
            card.pack(fill="x", expand=True)
            
            card.columnconfigure(1, weight=1) 

            # --- Coluna 0: Imagem ---
            image_path = item.get("img")
            ph = None
            if PIL_AVAILABLE and image_path and os.path.exists(image_path):
                try:
                    im = Image.open(image_path).resize((IMAGE_W, IMAGE_H)) 
                    ph = ImageTk.PhotoImage(im)
                    photos.append(ph)
                    Label(card, image=ph, bg="white").grid(row=0, column=0, rowspan=4, padx=6, pady=6, sticky="nsew") 
                except Exception:
                    ph = None
            
            if ph is None:
                # Placeholder centralizado
                placeholder = Frame(card, width=IMAGE_W, height=IMAGE_H, bg="#EFEFEF")
                placeholder.grid(row=0, column=0, rowspan=4, padx=6, pady=6, sticky="nsew") 
                placeholder.pack_propagate(False)
                Label(placeholder, text="Imagem", bg="#EFEFEF", fg="#AAAAAA", font=("Georgia", 10)).pack(expand=True)


            # --- Coluna 1: Texto e Controles (Layout Ajustado) ---
            right = Frame(card, bg="white")
            right.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=(0, 8), pady=6)
            right.columnconfigure(0, weight=1)

            # Frame principal do conteúdo de texto
            content_frame = Frame(right, bg="white")
            content_frame.pack(fill="x", expand=True, pady=(0, 4))
            
            # 1. NOME DA COMIDA (Centralizado)
            Label(content_frame, text=item["nome"], bg="white", fg="#111", 
                  font=("Georgia", 16, "bold"), justify="center"
                  ).pack(fill="x", pady=(0, 4)) 

            # 2. DESCRIÇÃO (Centralizada)
            Label(content_frame, text=item["desc"], bg="white", fg=TEXTO_SUAVE,
                  font=("Georgia", 10), wraplength=300, justify="center"
                  ).pack(fill="x", pady=(2, 6))

            # 3. PREÇO (Canto Inferior Esquerdo)
            price_frame = Frame(content_frame, bg="white")
            price_frame.pack(fill="x", pady=(4, 0))
            
            # Label do Preço, ancorada no Oeste ("w" - Esquerda)
            Label(price_frame, text=f"R$ {item['preço']:.2f}", bg="white", fg=DORADO_POLIDO,
                  font=("Georgia", 16, "bold"), anchor="w"
                  ).pack(side="right", padx=10)
            
            # Espaçador
            Frame(price_frame, bg="white").pack(side="left", fill="x", expand=True)
            

            # 4. Checkbox para seleção (Posicionado no final do bloco 'right')
            var = IntVar(value=0)
            chk = Checkbutton(right, text="SELECIONAR", variable=var, bg="white", anchor="w",
                              fg=DORADO_POLIDO, selectcolor="#E0E0E0",
                              font=("Georgia", 11, "bold"), activebackground="white", cursor="hand2")
            chk.pack(anchor="w", pady=(4, 0))

            checkbox_vars.append((var, item)) 
            
    # Botão para abrir diálogo de quantidades (no rodapé)
    btn_frame = Frame(page, bg=BG_ESCuro)
    btn_frame.pack(fill="x", padx=20, pady=(10, 20))
    add_selected_btn = Button(btn_frame, text="ADICIONAR SELECIONADOS À COMANDA",
                              bg=DORADO_POLIDO, fg=BG_ESCuro, font=("Georgia", 13, "bold"),
                              relief="flat", cursor="hand2", padx=10, pady=5, 
                              command=lambda: _open_quantity_dialog(parent, checkbox_vars))
    add_selected_btn.pack(side="right")

    page.photos = photos
    return page