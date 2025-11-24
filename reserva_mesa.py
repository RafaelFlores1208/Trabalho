# reserva_mesa.py
from tkinter import *
from tkinter import messagebox
import order # Para limpar a comanda após selecionar a mesa e iniciar o pedido
from servicos import PedidoService
from sistema import Mesa, Cliente

# --- PALETA DE CORES (Consistente com menu.py) ---
DORADO_POLIDO = "#BEA95B"
BG_ESCuro = "#1A1512"
COR_LIVRE = "#4CAF50" # Verde para Livre
COR_OCUPADA = "#F44336" # Vermelho para Ocupada

# Inicialização fictícia das Mesas
# Em um sistema real, isso viria de um banco de dados
def init_mesas():
    # Mesas de 2, 4 e 6 lugares
    mesas = [Mesa(i, 2) for i in range(1, 4)]  # Mesas 1, 2, 3 (2 lugares)
    mesas += [Mesa(i, 4) for i in range(4, 7)] # Mesas 4, 5, 6 (4 lugares)
    mesas += [Mesa(i, 6) for i in range(7, 9)] # Mesas 7, 8 (6 lugares)
    # Define uma mesa inicial como ocupada para teste
    mesas[3].ocupar() # Mesa 4 começa ocupada
    return mesas

MESAS_DISPONIVEIS = init_mesas()
pedido_service = PedidoService()

def liberar_mesa(mesa: Mesa, refresh_func):
    """Libera a mesa após o pagamento/limpeza, retornando ao status Livre."""
    if mesa.ocupada:
        mesa.liberar()
        # Aqui, em um sistema mais complexo, você registraria a transação do pedido
        messagebox.showinfo("Mesa Liberada", f"A Mesa {mesa.numero} foi liberada pelo Garçom.")
        refresh_func()
    else:
        messagebox.showwarning("Atenção", f"A Mesa {mesa.numero} já está livre.")

def criar_reserva_page(parent_frame, usuario_logado, navigate_to_menu_func):
    """
    Cria a interface de gerenciamento de Mesas para o Garçom/Cliente.
    Permite visualizar o status e liberar mesas (Garçom) ou selecionar (Cliente).
    """
    # Limpa o frame pai
    for w in parent_frame.winfo_children():
        w.destroy()

    # --- 1. Frame Principal (Container) e Scrollbar ---
    canvas = Canvas(parent_frame, bg=BG_ESCuro, highlightthickness=0)
    v_scroll = Scrollbar(parent_frame, orient="vertical", command=canvas.yview)

    scroll_frame = Frame(canvas, bg=BG_ESCuro, padx=20, pady=20)
    canvas.configure(yscrollcommand=v_scroll.set)
    scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw", tags="scroll_frame")

    # Título da Página
    Label(scroll_frame, text="✨ Gerenciamento de Mesas", font=("Georgia", 24, "bold"),
          fg=DORADO_POLIDO, bg=BG_ESCuro).pack(pady=(10, 20), anchor="center")

    def refresh_mesa_grid():
        """Função para reconstruir o grid de mesas e atualizar o status."""
        
        # Limpa o grid de mesas antigo
        for w in mesa_grid_frame.winfo_children():
            w.destroy()
            
        # Garante que o PedidoService tem uma instância (global) para controle
        global pedido_service 
        
        # Cria e exibe os botões/boxes das Mesas
        for i, mesa in enumerate(MESAS_DISPONIVEIS):
            status = "OCUPADA" if mesa.ocupada else "LIVRE"
            cor = COR_OCUPADA if mesa.ocupada else COR_LIVRE

            # Frame individual da Mesa
            mesa_frame = Frame(mesa_grid_frame, bg=BG_ESCuro, bd=2, relief="groove")
            mesa_frame.grid(row=i // 4, column=i % 4, padx=15, pady=15, sticky="nsew")
            
            # Número da Mesa
            Label(mesa_frame, text=f"MESA {mesa.numero}", font=("Georgia", 18, "bold"),
                  fg=DORADO_POLIDO, bg=BG_ESCuro).pack(pady=(10, 5))
            
            # Capacidade
            Label(mesa_frame, text=f"{mesa.lugares} Lugares", font=("Georgia", 11),
                  fg="white", bg=BG_ESCuro).pack(pady=2)

            # Status (com a cor de status)
            status_label = Label(mesa_frame, text=status, font=("Georgia", 14, "bold"),
                                 fg="white", bg=cor, relief="solid", bd=1, padx=10, pady=5)
            status_label.pack(pady=(5, 10))

            # --- Botão de Ação ---
            if mesa.ocupada:
                # Se ocupada, a ação é liberar (somente Garçom/Admin)
                btn_text = "Liberar Mesa (Garçom)"
                btn_color = COR_OCUPADA
                btn_command = lambda m=mesa: liberar_mesa(m, refresh_mesa_grid)
            else:
                # Se livre, a ação é selecionar para iniciar o pedido (Cliente/Garçom)
                btn_text = "Selecionar & Pedir"
                btn_color = DORADO_POLIDO
                btn_command = lambda m=mesa: selecionar_mesa_iniciar_pedido(m, navigate_to_menu_func, refresh_mesa_grid)

            Button(mesa_frame, text=btn_text, bg=btn_color, fg=BG_ESCuro,
                   font=("Georgia", 10, "bold"), relief="flat", cursor="hand2",
                   command=btn_command).pack(fill="x", padx=10, pady=(0, 10))
            
    def selecionar_mesa_iniciar_pedido(mesa: Mesa, navigate_func, refresh_func):
        """
        Altera o status da mesa para 'ocupada', cria um novo pedido e navega para o menu.
        """
        # 1. Confirmação
        confirmar = messagebox.askyesno(
            "Confirmar Seleção",
            f"Deseja selecionar a Mesa {mesa.numero} para iniciar um novo pedido?"
        )
        if not confirmar:
            return

        # 2. Lógica de Reserva
        mesa.ocupar()
        
        # 3. Limpa a comanda existente (crucial)
        order.clear_order()
        
        # 4. Cria um PedidoService (embora o sistema não use este objeto para a comanda Tkinter, a lógica de negócio aqui é registrar a ocupação)
        # O Pedido real (sistema.Pedido) seria criado no momento do pagamento para persistência, 
        # mas marcamos a mesa como ocupada agora.

        messagebox.showinfo("Mesa Selecionada", f"Mesa {mesa.numero} selecionada. Comece a adicionar itens.")
        
        # 5. Atualiza o grid de mesas na página de reserva
        refresh_func() 
        
        # 6. Navega para a página de Menu
        navigate_func("Menu")

    # --- Container para o Grid de Mesas ---
    mesa_grid_frame = Frame(scroll_frame, bg=BG_ESCuro)
    mesa_grid_frame.pack(pady=20, fill="x", expand=True)

    # Garante que o grid de mesas seja responsivo
    for i in range(4): # Assumindo 4 colunas
        mesa_grid_frame.grid_columnconfigure(i, weight=1)
        
    refresh_mesa_grid()