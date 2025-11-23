# carousel.py

import tkinter as tk
from PIL import Image, ImageTk
import itertools # Usado para criar o ciclo de imagens

class ImageCarousel(tk.Frame):
    def __init__(self, master, image_paths, delay_ms=4000):
        # Inicializa o Frame (o container do carrossel)
        tk.Frame.__init__(self, master, bg="yellow", bd=5, relief="solid")
        
        self.image_paths = image_paths
        self.delay_ms = delay_ms  # Atraso em milissegundos (4000 ms = 4 segundos)
        self.images = []
        self.photo_labels = []

        # 1. Carregar e Redimensionar Imagens
        self.load_images()

        # 2. Criar o Label onde a imagem será exibida
        self.image_label = tk.Label(self, bg="#1A1512")
        self.image_label.pack(expand=True, fill="both")

        # 3. Iniciar o ciclo do carrossel
        self.next_slide()

    def load_images(self):
        # Define um tamanho fixo para todas as imagens do carrossel
        CAROUSEL_WIDTH = 600
        CAROUSEL_HEIGHT = 400
        
        processed_images = []
        for path in self.image_paths:
            try:
                # Carregar e redimensionar a imagem usando Pillow
                img_pil = Image.open(path).resize((CAROUSEL_WIDTH, CAROUSEL_HEIGHT), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img_pil)
                processed_images.append(img_tk)
            except FileNotFoundError:
                print(f"ATENÇÃO: Arquivo de imagem não encontrado em {path}. Usando placeholder.")
                # Cria um placeholder vazio se a imagem não for encontrada
                placeholder = tk.PhotoImage(width=CAROUSEL_WIDTH, height=CAROUSEL_HEIGHT)
                processed_images.append(placeholder)
            except Exception as e:
                print(f"Erro ao carregar imagem {path}: {e}")
                placeholder = tk.PhotoImage(width=CAROUSEL_WIDTH, height=CAROUSEL_HEIGHT)
                processed_images.append(placeholder)

        self.images = processed_images
        # Cria um iterador que repete a lista de imagens indefinidamente
        self.image_cycle = itertools.cycle(self.images)

    def next_slide(self):
        # Pega a próxima imagem no ciclo
        next_image = next(self.image_cycle)

        if next_image:
            # Atualiza o Label com a nova imagem
            self.image_label.config(image=next_image)
            # ESSENCIAL: Armazena a referência para evitar o 'garbage collection' do Python
            self.image_label.image = next_image 
        
        # Agenda a próxima troca de slide
        self.after(self.delay_ms, self.next_slide)
        
        
# --- Seção de Teste (Opcional) ---
# Você pode remover esta seção se não quiser testar o carrossel separadamente.
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste de Carrossel Tkinter")
    root.geometry("800x600")
    root.configure(bg="red")

    # ⚠️ SUBSTITUA ESTES CAMINHOS PELOS SEUS ARQUIVOS REAIS! ⚠️
    image_list_test = [
        "imagens/ebano.png", 
        "imagens/interior.png", 
        "imagens/prato_principal.png"
    ]
    
    # Criar e empacotar o carrossel
    # Note: Se você não substituir os caminhos, verá placeholders vazios.
    carousel = ImageCarousel(root, image_list_test, delay_ms=3000) 
    carousel.pack(pady=50, padx=50, expand=True)

    root.mainloop()