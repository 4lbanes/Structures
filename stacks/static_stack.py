import tkinter as tk
from tkinter import messagebox
import time

class StaticStack:
    def __init__(self, max_size):
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        if not self.is_full():
            try:
                item = float(item)  # Tenta converter para número
            except ValueError:
                pass  # Mantém como string se não for número
            self.items.append(item)
            print(f"{item} foi adicionado à stack.")
        else:
            print("A stack está cheia.")

    def pop(self):
        if not self.is_empty():
            item = self.items.pop()
            print(f"{item} foi removido da stack.")
            return item
        else:
            print("A stack está vazia.")
            return None

    def is_empty(self):
        return len(self.items) == 0
    
    def is_full(self):
        return len(self.items) == self.max_size

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def size(self):
        return len(self.items)

    def get_stack(self):
        return self.items[::-1]  # Retorna a pilha invertida (base no final)
    
    def sort_stack(self):
     if self.is_empty():
        return
     # Converte números para comparação e mantém strings como estão
     def convert(item):
        try:
            return float(item)  # Converte para número se possível
        except ValueError:
            return item  # Mantém como string
    
     # Ordenar pelo valor numérico e colocar os menores no topo
     self.items.sort(key=lambda x: convert(x))

class StaticStackGUI:
    def __init__(self, root, max_size):
        self.stack = StaticStack(max_size)  
        self.root = root
        self.root.title("Pilha Estática: ")

        self.root.geometry("800x600")  # Define o tamanho da janela

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Usando pack() para todos os widgets
        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da pilha: {self.stack.max_size}")
        self.label_max_size.pack(pady=10)

        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.entry_data = tk.Entry(root)
        self.entry_data.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_push = tk.Button(root, text="Inserir na Pilha", command=self.push)
        self.button_push.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_pop = tk.Button(root, text="Remover da Pilha", command=self.pop)
        self.button_pop.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_sort = tk.Button(root, text="Ordenar a Pilha", command=self.sort_stack)
        self.button_sort.pack(side=tk.LEFT, padx=10, pady=10)

        self.stack_items = []
        self.update_buttons_visibility()
    
    def push(self):
        data = self.entry_data.get()
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        self.stack.push(data)
        self.update_stack_display()
        self.entry_data.delete(0, tk.END)
        self.update_buttons_visibility()

    def pop(self):
        removed = self.stack.pop()
        if removed is not None:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
            self.update_stack_display()
        else:
            messagebox.showwarning("Aviso", "A pilha está vazia.")
        self.update_buttons_visibility()

    def sort_stack(self):
        if not self.stack.is_empty():
            self.stack.sort_stack()
            self.update_stack_display()
        self.update_buttons_visibility()

    def update_stack_display(self):
        # Limpa os quadrados antigos
        self.canvas.delete("all")
        self.stack_items = []

        # Define a posição inicial do topo, calculando dinamicamente para centralizar na tela
        canvas_width = self.canvas.winfo_width()
        x_center = canvas_width // 2
        y_top = 50

        for index, item in enumerate(reversed(self.stack.items)):
            y_position = y_top + index * 50  # Ajusta a posição para cada elemento

            item_str = str(item)
            item_width = max(100, len(item_str) * 15)  # Largura mínima de 100, ajusta ao tamanho do texto

            # Desenha o quadrado
            square = self.canvas.create_rectangle(
                x_center - item_width // 2, y_position,
                x_center + item_width // 2, y_position + 40,
                fill="lightblue"
            )
            
            # Verifica se é o topo ou a base para personalizar o texto
            if index == 0:  # Se for o topo da pilha
                text_str = f"Topo\n{item_str}"
            elif index == len(self.stack.items) - 1:  # Se for a base da pilha
                text_str = f"Base\n{item_str}"
            else:
                text_str = item_str  # Apenas o valor para os demais itens

            # Adiciona o texto dentro do quadrado
            text = self.canvas.create_text(x_center, y_position + 20, text=text_str, font=("Arial", 16))

            self.stack_items.append((square, text))

            # Animação de movimento para cada quadrado
            for step in range(10): 
                self.canvas.move(square, 0, 3)
                self.canvas.move(text, 0, 3)
                self.canvas.update()
                time.sleep(0.02)

    def update_buttons_visibility(self):
        if self.stack.is_empty():
            self.button_pop.pack_forget()
            self.button_sort.pack_forget()
        else:
            self.button_pop.pack(side=tk.LEFT, padx=10, pady=10)
            self.button_sort.pack(side=tk.LEFT, padx=10, pady=10)
        
        if self.stack.is_full():
            self.button_push.pack_forget()
        else:
            self.button_push.pack(side=tk.LEFT, padx=10, pady=10)

# Criação da interface
root = tk.Tk()
app = StaticStackGUI(root, 5)
root.mainloop()
