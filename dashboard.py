# dashboard.py

from tkinter import *
# Importa a função principal da Home Page
from home_page import create_home_page as create_home_page_content 
from menu import create_menu_page
from compra import create_compra_page
from reserva_mesa import criar_reserva_page

class Dashboard(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema com Menu e Comanda")
        self.geometry("1000x700")
        self.configure(bg="#1A1512")
        
        # Inicia o estado da sidebar como FECHADO
        self.sidebar_expand = False 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # sidebar (Largura inicial 60 - Fechado)
        self.sidebar = Frame(self, bg="#1A1512", width=60) 
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Toggle (☰)
        self.toggle_btn = Button(
            self.sidebar, text="☰", bg="#1A1512", fg="#F4D465",
            font=("Georgia", 12), relief="flat", command=self.toggle_sidebar
        )
        self.toggle_btn.pack(pady=12, padx=12, fill="x")

        # Lista para os botões
        self.nav_buttons = []

        # Botão Início
        self.nav_buttons.append(Button(
            self.sidebar, text="Início", bg="#2A2218", fg="#F4D465",
            font=("Georgia", 14), relief="flat", command=self.go_home
        ))

        # Botão Menu
        self.nav_buttons.append(Button(
            self.sidebar, text="Menu", bg="#2A2218", fg="#F4D465",
            font=("Georgia", 14), relief="flat", command=self.open_menu
        ))

        # Botão Reserva (AGORA FUNCIONAL)
        self.nav_buttons.append(Button(
            self.sidebar, text="Reserva", bg="#2A2218", fg="#F4D465",
            font=("Georgia", 14), relief="flat", command=self.open_reserva
        ))

        # Botão Compra (Comanda)
        self.nav_buttons.append(Button(
            self.sidebar, text="Compra (Comanda)", bg="#2A2218", fg="#F4D465",
            font=("Georgia", 14), relief="flat", command=self.open_compra
        ))

        # Área de conteúdo
        self.content = Frame(self, bg="#1A1512")
        self.content.grid(row=0, column=1, sticky="nsew")

        # Abre Home ao iniciar
        self.go_home()

    # ---- Navegação ----

    def go_home(self):
        create_home_page_content(self.content)

    def open_menu(self):
        create_menu_page(self.content)

    def open_compra(self):
        create_compra_page(self.content)

    def open_reserva(self):
        # CHAMADA REAL DO ARQUIVO reserva_mesa.py
        criar_reserva_page(self.content)

    # ---- Sidebar abrir/fechar ----
    def toggle_sidebar(self):
        if self.sidebar_expand:
            # FECHAR
            for btn in self.nav_buttons:
                btn.pack_forget()
                
            self.sidebar.config(width=60)
            self.sidebar_expand = False
            self.toggle_btn.config(text="☰", font=("Georgia", 12))
        else:
            # ABRIR
            for btn in self.nav_buttons:
                btn.pack(fill="x", padx=12, pady=6)
                
            self.sidebar.config(width=220)
            self.sidebar_expand = True
            self.toggle_btn.config(text="X", font=("Georgia", 16))

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
