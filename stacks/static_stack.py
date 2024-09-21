import tkinter as tk
from tkinter import messagebox
import time

# Classe que representa um nó
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Aponta para o próximo nó

# Classe que representa a pilha estática utilizando nós e ponteiros
class StaticStack:
    def __init__(self, max_size):
        self.top = None  # O topo da pilha (apontador para o nó do topo)
        self.max_size = max_size
        self.size = 0  # Contador do número de elementos na pilha
    
    def push(self, item):
        if not self.is_full():
            try:
                item = float(item)  # Tenta converter para número
            except ValueError:
                pass  # Mantém como string se não for número

            new_node = Node(item)  # Cria um novo nó com o item
            new_node.next = self.top  # O próximo nó será o topo atual
            self.top = new_node  # O novo nó se torna o topo
            self.size += 1  # Incrementa o tamanho da pilha
            print(f"{item} foi adicionado à stack.")
        else:
            print("A stack está cheia.")

    def pop(self):
        if not self.is_empty():
            removed_node = self.top  # Pega o nó do topo
            self.top = self.top.next  # Atualiza o topo para o próximo nó
            self.size -= 1  # Decrementa o tamanho da pilha
            print(f"{removed_node.data} foi removido da stack.")
            return removed_node.data
        else:
            print("A stack está vazia.")
            return None

    def is_empty(self):
        return self.top is None  # Verifica se o topo é None
    
    def is_full(self):
        return self.size == self.max_size  # Verifica se o tamanho atingiu o limite

    def peek(self):
        if not self.is_empty():
            return self.top.data  # Retorna o dado no topo
        else:
            return None

    def get_stack(self):
        current = self.top
        stack_items = []
        while current is not None:
            stack_items.append(current.data)
            current = current.next
        return stack_items[::-1]  # Retorna a pilha invertida (base no final)
    
    def sort_stack(self):
        if self.is_empty():
            return

        # Extrai os elementos da pilha em uma lista
        stack_list = self.get_stack()

        # Converte números para comparação e mantém strings como estão
        def convert(item):
            try:
                return float(item)  # Converte para número se possível
            except ValueError:
                return item  # Mantém como string

        # Ordenar pelo valor numérico e colocar os menores no topo
        stack_list.sort(key=lambda x: convert(x))

        # Reconstrói a pilha ordenada
        self.top = None
        self.size = 0
        for item in stack_list[::-1]:
            self.push(item)

# Classe da interface gráfica da pilha estática
class StaticStackGUI:
    def __init__(self, root, max_size):
        self.stack = StaticStack(max_size)
        self.root = root
        self.root.title("Pilha Estática: ")

        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

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
        self.canvas.delete("all")
        self.stack_items = []

        # Define a posição inicial do topo, centralizado
        canvas_width = self.canvas.winfo_width()
        x_center = canvas_width // 2
        y_top = 50

        # Pega os itens da pilha do topo até a base
        stack_items = self.stack.get_stack()

        # Vamos desenhar do último item ao primeiro (LIFO)
        for index, item in enumerate(reversed(stack_items)):  # Reverter para seguir a ordem LIFO
            y_position = y_top + index * 50

            item_str = str(item)
            item_width = max(100, len(item_str) * 15)

            square = self.canvas.create_rectangle(
                x_center - item_width // 2, y_position,
                x_center + item_width // 2, y_position + 40,
                fill="lightblue"
            )

            if index == 0:  
                text_str = f"Topo\n{item_str}"  # O primeiro item desenhado é o topo
            else:
                text_str = item_str

            text = self.canvas.create_text(x_center, y_position + 20, text=text_str, font=("Arial", 16))

            self.stack_items.append((square, text))

            # Animação de descida
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

