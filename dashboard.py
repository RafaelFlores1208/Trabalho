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

        # toggle button (Ícone de abrir ☰) - **CORRIGIDO**
        self.toggle_btn = Button(self.sidebar, text="☰", bg="#1A1512", fg="#F4D465", # <-- O 'text="☰"' é crucial!
                                 font=("Georgia", 12), relief="flat", command=self.toggle_sidebar)
        self.toggle_btn.pack(pady=12, padx=12, fill="x")

        # Lista para guardar os botões de navegação
        self.nav_buttons = []

        # Botões - **CORRIGIDOS** (garantindo text= em todos)
        self.nav_buttons.append(Button(self.sidebar, text="Início", bg="#2A2218", fg="#F4D465", font=("Georgia", 14),
               relief="flat", command=self.go_home))
        self.nav_buttons.append(Button(self.sidebar, text="Menu", bg="#2A2218", fg="#F4D465", font=("Georgia", 14),
               relief="flat", command=self.open_menu))
        self.nav_buttons.append(Button(self.sidebar, text="Perfil", bg="#2A2218", fg="#F4D465", font=("Georgia", 14),
               relief="flat", command=lambda: self.update_content("Perfil")))\
        self.nav_buttons.append(Button(self.sidebar, text="Reserva", bg="#2A2218", fg="#F4D465", font=("Georgia", 14),
               relief="flat", command=lambda: self.update_content("Reserva")))
        self.nav_buttons.append(Button(self.sidebar, text="Compra (Comanda)", bg="#2A2218", fg="#F4D465", font=("Georgia", 14),
               relief="flat", command=self.open_compra))

        # content area
        self.content = Frame(self, bg="#1A1512")
        self.content.grid(row=0, column=1, sticky="nsew")

        # Inicialização: Carrega a Home Page com o Carrossel
        self.go_home() 
        
    def go_home(self):
        # Chama a função importada de home_page.py, que contém o carrossel
        create_home_page_content(self.content)

    def open_menu(self):
        create_menu_page(self.content)

    def open_compra(self):
        create_compra_page(self.content)

    def update_content(self, text):
        # Método genérico para telas simples (como Perfil/Reserva)
        for w in self.content.winfo_children():
            w.destroy()
            
        center_frame = Frame(self.content, bg="#1A1512")
        center_frame.pack(expand=True)
        
        # Labels - **CORRIGIDAS** (garantindo text= em ambos)
        Label(center_frame, 
              text=text, 
              font=("Georgia", 20), 
              fg="white", 
              bg="#1A1512").pack(pady=(0, 10)) 
        
        if text == "Perfil":
            novo_texto = "Esta é a área do Perfil. Informações do usuário virão aqui."
        elif text == "Reserva":
            novo_texto = "Use esta seção para gerenciar reservas de mesas."
        else:
            novo_texto = ""

        if novo_texto:
             Label(center_frame, 
                  text=novo_texto, 
                  font=("Georgia", 12), 
                  fg="#F4D465", 
                  bg="#1A1512",
                  wraplength=400, 
                  justify=CENTER).pack(pady=5)

    def toggle_sidebar(self):
        if self.sidebar_expand:
            # FECHA: Remove botões e encolhe a barra lateral
            for btn in self.nav_buttons:
                btn.pack_forget() 
                
            self.sidebar.config(width=60)
            self.sidebar_expand = False
            self.toggle_btn.config(text="☰", font=("Georgia", 12))
        else:
            # ABRE: Empacota botões e expande a barra lateral
            for btn in self.nav_buttons:
                btn.pack(fill="x", padx=12, pady=6) 
                
            self.sidebar.config(width=220)
            self.sidebar_expand = True
            self.toggle_btn.config(text="X", font=("Georgia", 16))

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()