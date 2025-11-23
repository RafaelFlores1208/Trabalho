# home_page.py
from tkinter import *
# Importa a classe Carrossel que deve estar em um arquivo chamado 'carousel.py'
from carousel import ImageCarousel 

def create_home_page(parent_frame):
    """
    Cria e exibe o conteúdo da Página Inicial (Home), centralizado e responsivo,
    incluindo o carrossel de imagens.
    """
    # Destrói os widgets antigos no frame pai (content)
    for w in parent_frame.winfo_children():
        w.destroy()
    
    # --- 1. Frame Principal (Container) e Scrollbar ---
    
    canvas = Canvas(parent_frame, bg="#1A1512", highlightthickness=0)
    v_scroll = Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    
    # Criamos o frame que conterá todo o nosso conteúdo
    scroll_frame = Frame(canvas, bg="#1A1512", padx=20, pady=20)
    
    # Configura a rolagem
    canvas.configure(yscrollcommand=v_scroll.set)
    
    # Bind para atualizar a região de rolagem quando o conteúdo muda de tamanho
    scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    # Cria a janela do canvas e garante que ela use toda a largura
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Bind para garantir que o scroll_frame use a largura total do Canvas
    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind('<Configure>', on_canvas_resize)

    # --- 2. Centralização do Conteúdo no scroll_frame ---
    
    # Usamos um 'central_frame' para garantir que todo o conteúdo seja centralizado
    central_frame = Frame(scroll_frame, bg="#1A1512")
    central_frame.pack(expand=True, fill="x")
    
    # Configuração de Grid para centralizar o conteúdo (colunas laterais com peso 1)
    central_frame.grid_columnconfigure(0, weight=1)
    central_frame.grid_columnconfigure(2, weight=1)
    
    content_area = Frame(central_frame, bg="#1A1512")
    content_area.grid(row=0, column=1, sticky="ew") # Preenche horizontalmente na coluna central

    # --- Título ---
    Label(content_area, 
          text="Ébano", 
          font=("Georgia", 33, "bold"), 
          fg="white", 
          bg="#1A1512").pack(pady=(10, 5)) 
    
    Label(content_area, 
          text="Experiência Única. Sabores Inesquecíveis. Faça sua Reserva.", 
          font=("Georgia", 20), 
          fg="#BEA95B", 
          bg="#1A1512").pack(pady=(10, 20)) 

    # --- Seção de Fotos (Carrossel) ---
    
    Label(content_area, 
          text="O Cenário Perfeito", 
          font=("Georgia", 18), 
          fg="#F4D465", 
          bg="#1A1512",
          anchor="center").pack(fill="x", pady=(10, 10))
          
    # 1. DEFINIÇÃO DAS FOTOS DO RESTAURANTE PARA O CARROSSEL
    restaurante_fotos = [
          "imagens/ebano.png",
          "imagens/interior.png",
          "imagens/prato_principal.png",
          "imagens/sobre.png"
    ]

    # 2. CRIAÇÃO E EMPACOTAMENTO DO WIDGET CARROSSEL
    # Ele usa um Frame, então se centraliza automaticamente dentro do content_area
    carousel_widget = ImageCarousel(content_area, restaurante_fotos, delay_ms=4000)# Troca a cada 4s
    print("Carrossel criado com sucesso:", carousel_widget)

    carousel_widget.pack(pady=10)


    # --- Seção História, Valores e Metas (Texto Centralizado) ---
    
    Label(content_area, 
          text="Nossa Essência", 
          font=("Georgia", 18, "underline"), 
          fg="#BEA95B", 
          bg="#1A1512",
          anchor="center").pack(fill="x", pady=(10, 5))
          
    # História
    Label(content_area, 
          text="📜 História:", 
          font=("Georgia", 14, "bold"), 
          fg="#F4D465", 
          bg="#1A1512", anchor="center").pack(fill="x", pady=(10, 2))
    historia_texto = "Fundado em 1951, nosso restaurante nasceu da paixão por cozinhar. Nossa jornada começou com uma pequena cozinha e o sonho de elevar a gastronomia a uma forma de arte, focando sempre na qualidade dos ingredientes e na hospitalidade."
    Label(content_area, text=historia_texto, font=("Arial", 12), fg="white", bg="#1A1512",
          wraplength=750, justify=CENTER).pack(fill="x") 
          
    # Valores
    Label(content_area, 
          text="✨ Valores:", 
          font=("Georgia", 14, "bold"), 
          fg="#F4D465", 
          bg="#1A1512", anchor="center").pack(fill="x", pady=(10, 2))
    valores_texto = "Qualidade Inegável, Hospitalidade Excepcional, Inovação Culinária e Sustentabilidade. Esses pilares guiam cada prato e cada interação com nossos clientes."
    Label(content_area, text=valores_texto, font=("Georgia", 12), fg="white", bg="#1A1512",
          wraplength=750, justify=CENTER).pack(fill="x") 
          
    # Metas Futuras
    Label(content_area, 
          text="🎯 Metas Futuras:", 
          font=("Georgia", 14, "bold"), 
          fg="#F4D465", 
          bg="#1A1512", anchor="center").pack(fill="x", pady=(10, 2))
    metas_texto = "Nossa meta é expandir para novas cidades mantendo a exclusividade, lançar um menu sazonal focado em ingredientes locais e conquistar nossa tarceira estrela michelin,nossa experiência gastronômica é a  mais renomada do país nos últimos 3 anos."
    Label(content_area, text=metas_texto, font=("Georgia", 12), fg="white", bg="#1A1512",
          wraplength=750, justify=CENTER).pack(fill="x") 

    # --- Opinião dos Degustadores (Críticas Centralizadas) ---
    
    Label(content_area, 
          text="O que Dizem Nossos Críticos", 
          font=("Georgia", 18, "underline"), 
          fg="#BEA95B", 
          bg="#1A1512",
          anchor="center").pack(fill="x", pady=(30, 10))
          
    # Frame para as críticas (Centralizado)
    critica_frame = Frame(content_area, bg="#1A1512")
    critica_frame.pack(pady=10)

    # ... (Blocos de críticas permanecem os mesmos, mas centralizados pelo pack do critica_frame) ...

    # 1. Crítica 1
    critica1_box = Frame(critica_frame, bg="#2A2218", padx=15, pady=15, width=380, height=180, relief="raised", bd=2)
    critica1_box.pack_propagate(False) 
    critica1_box.grid(row=0, column=0, padx=15)
    
    Label(critica1_box, 
          text="\"Uma orquestra de sabores. O melhor Medalhão de Filé Mignon que já provei! Experiência de cinco estrelas.\" - Anthony Bourdain, ELLE à Table", 
          font=("Georgia", 11, "italic"), fg="white", bg="#2A2218", 
          wraplength=350, justify=CENTER).pack(expand=True, fill="both") 

    # 2. Crítica 2
    critica2_box = Frame(critica_frame, bg="#2A2218", padx=15, pady=15, width=380, height=180, relief="raised", bd=2)
    critica2_box.pack_propagate(False) 
    critica2_box.grid(row=0, column=1, padx=15)
    
    Label(critica2_box, 
          text="\"O serviço impecável e o ambiente criam o clima ideal para uma noite especial. É o novo templo da alta cozinha local.\" -Érick Jacquin, Blog Sabor & Arte", 
          font=("Georgia", 11, "italic"), fg="white", bg="#2A2218", 
          wraplength=350, justify=CENTER).pack(expand=True, fill="both")
          
    # --- Chamada para Reserva ---
    Label(content_area, 
          text="Não perca tempo! Clique no botão 'Reserva' no menu lateral e garanta sua mesa.", 
          font=("Georgia", 14, "bold"), 
          fg="white", 
          bg="#1A1512").pack(pady=(30, 10))