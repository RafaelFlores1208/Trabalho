# carousel.py

import tkinter as tk
from PIL import Image, ImageTk
import itertools

class ImageCarousel(tk.Frame):
    def __init__(self, master, image_paths, delay_ms=4000):
        # Frame do carrossel — SEM BORDA, SEM COR INDESEJADA
        tk.Frame.__init__(self, master, bg="#1A1512", bd=0, highlightthickness=0)

        self.image_paths = image_paths
        self.delay_ms = delay_ms
        self.images = []

        # Carregar e padronizar imagens
        self.load_images()

        # Label principal onde a imagem é exibida
        self.image_label = tk.Label(self, bg="#1A1512", bd=0, highlightthickness=0)
        self.image_label.pack(expand=True, fill="both")

        # Iniciar o ciclo de slides
        self.next_slide()

    def load_images(self):
        CAROUSEL_WIDTH = 600
        CAROUSEL_HEIGHT = 400

        processed = []

        for path in self.image_paths:
            try:
                img = Image.open(path).resize(
                    (CAROUSEL_WIDTH, CAROUSEL_HEIGHT),
                    Image.Resampling.LANCZOS
                )
                img_tk = ImageTk.PhotoImage(img)
                processed.append(img_tk)
            except Exception as e:
                print(f"Erro ao carregar {path}: {e}")
                placeholder = tk.PhotoImage(
                    width=CAROUSEL_WIDTH,
                    height=CAROUSEL_HEIGHT
                )
                processed.append(placeholder)

        self.images = processed
        self.image_cycle = itertools.cycle(self.images)

    def next_slide(self):
        """Troca para a próxima imagem no ciclo"""
        next_image = next(self.image_cycle)

        if next_image:
            self.image_label.config(image=next_image)
            self.image_label.image = next_image  # evita garbage collection

        self.after(self.delay_ms, self.next_slide)


# Teste opcional
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Teste do Carrossel")
    root.geometry("900x600")
    root.configure(bg="#1A1512")

    images = [
        "imagens/ebano.png",
        "imagens/interior.png",
        "imagens/prato_principal.png",
    ]

    c = ImageCarousel(root, images)
    c.pack(pady=20)

    root.mainloop()
