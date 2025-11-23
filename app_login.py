from tkinter import *

class Dashboard(Tk):
    """
    Dashboard com cabeçalho fixo no topo da janela, barra lateral colapsável 
    e área de conteúdo principal na parte inferior.
    """
    def __init__(self):
        super().__init__()
        self.title("Nome do sistema de Reservas e Compras")
        self.geometry("800x550")
        self.configure(bg="#141107")

        # --- Definições de Largura e Rótulos ---
        self.sidebar_expanded_width = 200 
        self.sidebar_collapsed_width = 60  
        self.labels = ["Menu", "Perfil", "Reserva", "Compra"] 
        
        # O estado inicial é True para que a primeira chamada a toggle_sidebar() colapse o menu.
        self.sidebar_expand = True 
        
        # --- 1. REORGANIZAÇÃO DO GRID PRINCIPAL ---
        
        # Row 0: Header (fixo no topo)
        self.grid_rowconfigure(0, weight=0) 
        
        # Row 1: Conteúdo Principal (Sidebar e Text Area)
        self.grid_rowconfigure(1, weight=1)    
        
        # Column 0: Sidebar (não cresce)
        self.grid_columnconfigure(0, weight=0) 
        
        # Column 1: Área de Conteúdo (cresce)
        self.grid_columnconfigure(1, weight=1) 

        # --- CRIAÇÃO DO HEADER (Row 0) ---
        self.header_frame = Frame(self, bg="#0D0A02", height=60)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew") 
        self.header_frame.grid_propagate(False)

        self.app_title_label = Label(self.header_frame, text="Sistema Integrado de Gestão", 
                                  bg="#0D0A02", fg="#f4D465", font=("Georgia", 20, "bold"), anchor="w")
        self.app_title_label.pack(padx=20, pady=10, fill="x")

        # --- 2. CRIAÇÃO DA BARRA LATERAL (Row 1, Column 0) ---
        self.sidebar_frame = Frame(self, bg="#1B1709", width=self.sidebar_expanded_width)
        self.sidebar_frame.grid(row=1, column=0, sticky="ns")
        self.sidebar_frame.grid_propagate(False)

        # --- 3. CRIAÇÃO DO CONTEÚDO PRINCIPAL (Row 1, Column 1) ---
        self.content_frame = Frame(self, bg="#141107")
        self.content_frame.grid(row=1, column=1, sticky="nsew")

        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=0) 
        self.content_frame.grid_rowconfigure(1, weight=1) 

        # Área de Título da Página (usado para indicar a página atual)
        self.page_title_label = Label(self.content_frame, text="Menu Principal", 
                                  bg="#141107", fg="#f4D465", font=("Georgia", 16, "bold"), anchor="w")
        self.page_title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")


        # Área de Texto Principal (simulando um documento)
        self.main_text = Text(self.content_frame, wrap=WORD, bg="#24211A", fg="white", 
                              font=("Georgia", 12), bd=0, padx=15, pady=15, relief="flat")
        self.main_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        

        # --- Elementos da Sidebar ---
        self.toggle_btn = Button(self.sidebar_frame, text="X", bg="#141107", fg="#f4D465", 
                                 cursor="hand2", font=("Georgia",16), relief="flat",
                                 command=self.toggle_sidebar)
        self.toggle_btn.pack(pady=10, padx=10, fill="x", anchor="w")

        self.nav_buttons = []
        for text in self.labels:
            # O comando 'lambda t=text: self.navigate_to(t)' é o que faz a linkagem funcionar
            btn = Button(self.sidebar_frame, text=text, bg="#1B1709", fg="#f4D465", font=("Georgia",14), 
            relief="flat", cursor="hand2", anchor="w", 
            command=lambda t=text: self.navigate_to(t))
            btn.pack(fill="x", pady=5, padx=10) 
            self.nav_buttons.append(btn)
        
        # Inicia Colapsado e carrega o conteúdo inicial ("Menu")
        self.toggle_sidebar() 
        self.navigate_to("Menu") 


    def get_page_content(self, page_name):
        """Retorna o texto (simulado) para a página selecionada."""
        if page_name == "Menu":
            return "\menu."
        elif page_name == "Perfil":
            return "\n\nDetalhes da Conta:\nNome: Usuário Padrão\nID: 45789-A\nStatus: Ativo\n\nNesta secção, pode atualizar dados de contato e rever permissões. As alterações feitas aqui são instantâneas e aplicam-se a todas as transações futuras."
        elif page_name == "Reserva":
            return "Funcionalidade de Reserva.\n\nUtilize este espaço para agendar novos serviços. Para prosseguir, insira a data desejada e confirme a disponibilidade. Todos os agendamentos são imediatamente processados e confirmados via e-mail e notificação no sistema."
        elif page_name == "Compra":
            return "Portal de Compras.\n\nExplore os produtos disponíveis e adicione-os ao seu carrinho. O checkout é simplificado e seguro. Se houver alguma falha na transação, por favor, contacte o suporte técnico imediatamente. Histórico de Compras disponível na secção 'Perfil'."
        else:
            return f"Conteúdo detalhado para a seção '{page_name}' não disponível."

    
    def toggle_sidebar(self):
        """Alterna entre o estado expandido e colapsado da barra lateral."""
        if self.sidebar_expand:
            # Lógica para Colapsar (Estado: Expandido -> Colapsado)
            self.sidebar_frame.config(width=self.sidebar_collapsed_width)
            
            self.toggle_btn.pack_forget()
            self.toggle_btn.config(text="☰", fg="#f4D465" ,font=("Georgia",18), bg="#141107") 
            self.toggle_btn.pack(pady=10, padx=10, fill="x", anchor="center")
            
            for btn in self.nav_buttons:
                btn.pack_forget() 
            
            self.sidebar_expand = False
        else:
            # Lógica para Expandir (Estado: Colapsado -> Expandido)
            self.sidebar_frame.config(width=self.sidebar_expanded_width)
            
            self.toggle_btn.pack_forget()
            self.toggle_btn.config(text="X", fg="#f4D465", font=("Georgia",16), relief="flat", bg="#141107")
            self.toggle_btn.pack(pady=10, padx=10, fill="x", anchor="w")

            for btn in self.nav_buttons:
                btn.pack(fill="x", pady=5, padx=10)
                
            self.sidebar_expand = True
            
    def navigate_to(self, page_name):
        """Atualiza o título da página e a área de texto com o conteúdo."""
        
        # Atualiza o título da página
        self.page_title_label.config(text=page_name.upper())

        # Atualiza a área de texto principal
        content = self.get_page_content(page_name)
        self.main_text.config(state=NORMAL) 
        self.main_text.delete(1.0, END)      
        self.main_text.insert(END, content) 
        self.main_text.config(state=DISABLED) # Deixa como somente leitura

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()