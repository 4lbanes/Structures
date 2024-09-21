import tkinter as tk
from tkinter import messagebox
import time

class DynamicStack:
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self):
        self.top = None
        self.height = 0

    def push(self, item):
        try:
            item = float(item)  # Tenta converter para número
        except ValueError:
            pass  # Mantém como string se não for número
        new_node = self.Node(item)
        new_node.next = self.top
        self.top = new_node
        self.height += 1
        print(f"{item} foi adicionado à stack.")

    def pop(self):
        if self.is_empty():
            print("A stack está vazia.")
            return None
        value = self.top.value
        self.top = self.top.next
        self.height -= 1
        print(f"{value} foi removido da stack.")
        return value

    def is_empty(self):
        return self.top is None

    def peek(self):
        if not self.is_empty():
            return self.top.value
        else:
            return None

    def size(self):
        return self.height

    def get_stack(self):
        stack_elements = []
        current = self.top
        while current is not None:
            stack_elements.append(current.value)
            current = current.next
        return stack_elements[::-1]  # Retorna a pilha invertida (base no final)

    def sort_stack(self):
        if self.is_empty():
            return

        # Função para converter elementos para comparação
        def convert(item):
            try:
                return float(item)
            except ValueError:
                return item

        # Coleta todos os itens em uma lista temporária
        temp_list = []
        current = self.top
        while current:
            temp_list.append(current.value)
            current = current.next

        # Ordena a lista e reconstrói a pilha
        temp_list.sort(key=convert)
        self.top = None
        self.height = 0
        for item in reversed(temp_list):
            self.push(item)

class DynamicStackGUI:
    def __init__(self, root):
        self.stack = DynamicStack()  
        self.root = root
        self.root.title("Pilha Dinâmica: ")

        self.root.geometry("800x600")  # Define o tamanho da janela

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Usando pack() para todos os widgets
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

        stack_elements = self.stack.get_stack()  # Pega a pilha como uma lista para desenhar

        for index, item in enumerate(reversed(stack_elements)):  # Corrige a ordem invertendo a lista para exibir como LIFO
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


# Criação da interface
root = tk.Tk()
app = DynamicStackGUI(root)
root.mainloop()
