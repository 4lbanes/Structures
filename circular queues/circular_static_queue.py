import tkinter as tk
import math

class CircularStaticQueue:
    def __init__(self, max_size):
        self.queue = [None] * max_size
        self.max_size = max_size
        self.size = 0
        self.first = 0

    def enqueue(self, value):
        if self.is_full():
            print("Queue is Full!")
            return
        
        self.queue[(self.first + self.size) % self.max_size] = value
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            print("Queue is Empty")
            return None
        
        value = self.first_item()
        self.queue[self.first] = None
        self.first = (self.first + 1) % self.max_size
        self.size -= 1
        
        return value

    def first_item(self):
        if self.is_empty():
            print("Queue is Empty!")
            return None
        return self.queue[self.first]

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.max_size

    def get_size(self):
        return self.size

    def sort(self):
        # Ordena a fila em ordem crescente
        if self.is_empty():
            return
        
        sorted_items = [self.queue[(self.first + i) % self.max_size] for i in range(self.size)]
        sorted_items.sort()

        for i in range(self.size):
            self.queue[(self.first + i) % self.max_size] = sorted_items[i]

    def __str__(self):
        elements = []
        for i in range(self.size):
            elements.append(self.queue[(self.first + i) % self.max_size])
        return "[" + ", ".join(map(str, elements)) + "]"

class CircularQueueGUI:
    def __init__(self, root):
        self.queue = CircularStaticQueue(5)  # Tamanho máximo da fila
        self.root = root
        self.root.title("Fila Circular Estática")

        self.canvas = tk.Canvas(root, bg="white", height=400, width=800)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=1, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=1, column=1)
        
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)
        self.button_enqueue.grid(row=2, column=0, columnspan=2)

        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)
        self.button_sort = tk.Button(root, text="Ordenar Fila", command=self.sort_queue)

        # Adicionando a label para mostrar o tamanho máximo da fila
        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da fila: {self.queue.max_size}")
        self.label_max_size.grid(row=4, column=0, columnspan=2)

        self.queue_items = []  # Armazena os retângulos e textos na tela
        self.update_queue_display()

    def enqueue(self):
        data = self.entry_data.get()

        if not data:
            print("Preencha o campo de elemento!")
            return
        
        self.queue.enqueue(int(data))  # Converte para inteiro
        self.entry_data.delete(0, tk.END)
        
        self.update_queue_display()

    def dequeue(self):
        removed = self.queue.dequeue()
        if removed is not None:
            print(f"Elemento removido: {removed}")
        self.update_queue_display()

    def sort_queue(self):
        self.queue.sort()
        self.update_queue_display()

    def update_queue_display(self):
     # Limpa os retângulos antigos
     self.canvas.delete("all")
     self.queue_items = []

     # Calcula posição central
     center_x = self.canvas.winfo_width() // 2
     center_y = self.canvas.winfo_height() // 2
     radius = 100  # Raio do círculo

     # Desenha cada posição da fila como uma caixa vazia, independentemente de estar preenchida ou não
     for index in range(self.queue.max_size):
        angle = 2 * math.pi * index / self.queue.max_size
        x_position = center_x + radius * math.cos(angle) - 50
        y_position = center_y + radius * math.sin(angle) - 20

        # Desenha a caixa para cada posição
        self.canvas.create_rectangle(
            x_position, y_position, 
            x_position + 100, y_position + 40,
            outline="gray", fill="lightgray"
        )

     # Desenha cada elemento da fila, se houver
     for index in range(self.queue.get_size()):
        item = self.queue.queue[(self.queue.first + index) % self.queue.max_size]
        angle = 2 * math.pi * ((self.queue.first + index) % self.queue.max_size) / self.queue.max_size
        x_position = center_x + radius * math.cos(angle) - 50
        y_position = center_y + radius * math.sin(angle) - 20

        square = self.canvas.create_rectangle(
            x_position, y_position, 
            x_position + 100, y_position + 40,
            fill="lightblue"
        )

        text = self.canvas.create_text(
            x_position + 50, y_position + 20,
            text=str(item), font=("Arial", 16)
        )

        self.queue_items.append((square, text))

        # Desenha setas entre os elementos
        if index < self.queue.get_size() - 1:
            next_angle = 2 * math.pi * ((self.queue.first + index + 1) % self.queue.max_size) / self.queue.max_size
            next_x = center_x + radius * math.cos(next_angle)
            next_y = center_y + radius * math.sin(next_angle)

            self.canvas.create_line(
                x_position + 100, y_position + 20,
                next_x, next_y + 20,
                arrow=tk.LAST, fill="black", width=2
            )

     # Indicar o topo da fila
     if not self.queue.is_empty():
        first_item_angle = 2 * math.pi * self.queue.first / self.queue.max_size
        first_x = center_x + radius * math.cos(first_item_angle)
        first_y = center_y + radius * math.sin(first_item_angle)
        self.canvas.create_text(first_x + 50, first_y + 20, text="Topo", fill="black", font=("Arial", 8, 'bold'))

     # Indicar a base da fila, apenas se houver mais de um elemento
     if self.queue.get_size() > 1:
        last_item_angle = 2 * math.pi * ((self.queue.first + self.queue.get_size() - 1) % self.queue.max_size) / self.queue.max_size
        last_x = center_x + radius * math.cos(last_item_angle)
        last_y = center_y + radius * math.sin(last_item_angle)
        self.canvas.create_text(last_x + 50, last_y + 20, text="Base", fill="black", font=("Arial", 8, 'bold'))

     # Atualiza a visibilidade dos botões de remoção e ordenação
     if self.queue.is_empty():
        self.button_dequeue.grid_forget()
        self.button_sort.grid_forget()
     else:
        self.button_dequeue.grid(row=3, column=0, columnspan=2)
        self.button_sort.grid(row=3, column=1, columnspan=2)
        
     if self.queue.is_full():
         self.button_enqueue.grid_forget()
 

# Criação da interface
root = tk.Tk()
app = CircularQueueGUI(root)
root.mainloop()
