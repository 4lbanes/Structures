import tkinter as tk
from tkinter import messagebox
import time

class StaticQueue:
    def __init__(self, max_size):
        self.queue = [None] * max_size  # Cria uma lista com tamanho máximo
        self.size = 0                   # Tamanho atual da fila
        self.size_max = max_size        # Tamanho máximo da fila

    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.size_max
    
    def enqueue(self, value):
        if self.is_full():
            print("Queue is Full!")
        
        # Insere o novo valor no final da fila
        self.queue[self.size] = value
        self.size += 1
        print(f"{value} foi adicionado à fila.")
    
    def dequeue(self):
        if self.is_empty():
         print("Queue is Empty")
        
        # Remove o primeiro elemento da fila
        removed_element = self.queue[0]

        # Move os elementos restantes para a esquerda
        for i in range(self.size - 1):
            self.queue[i] = self.queue[i + 1]

        self.queue[self.size - 1] = None  # Limpa o último valor
        self.size -= 1

        print(f"{removed_element} foi removido da fila.")
        return removed_element
    
    def peek(self):  # Mostra o primeiro elemento da fila sem removê-lo
        if self.is_empty():
         print("Queue is Empty")
        return self.queue[0]

    def print_queue(self):
        if self.is_empty():
            return []
        return self.queue[:self.size]  # Retorna apenas os elementos válidos da fila

    def sort_queue(self):
        # Implementa a ordenação dos elementos sem usar funções nativas do Python
        if self.is_empty():
            return
        
        # Algoritmo de ordenação básico (bolha) para a fila
        for i in range(self.size - 1):
            for j in range(self.size - 1 - i):
                if self.queue[j] > self.queue[j + 1]:
                    self.queue[j], self.queue[j + 1] = self.queue[j + 1], self.queue[j]
# Interface com Tkinter
class StaticQueueGUI:
    def __init__(self, root, max_size):
        self.queue = StaticQueue(max_size)  
        self.root = root
        self.root.title("Fila Estática: ")

        self.canvas = tk.Canvas(root, bg="white", height=400, width=800)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da fila: {max_size}")
        self.label_max_size.grid(row=1, column=0, columnspan=2)
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=2, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=2, column=1)
        
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)
        self.button_enqueue.grid(row=3, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)
        self.button_dequeue.grid(row=4, column=0, columnspan=2)

        self.button_sort = tk.Button(root, text="Ordenar a Fila", command=self.sort_queue)
        self.button_sort.grid(row=4, column=2)

        self.queue_items = []  # Armazena os retângulos e textos na tela
        self.update_queue_display()
        self.update_buttons_visibility()

    def enqueue(self):
        data = self.entry_data.get()

        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        if self.queue.is_full():
            messagebox.showwarning("Aviso", "A fila está cheia.")
            return
        
        self.queue.enqueue(data)
        self.entry_data.delete(0, tk.END)
        
        self.update_queue_display(animated=True)
        self.update_buttons_visibility()

    def dequeue(self):
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        
        self.update_queue_display()
        self.update_buttons_visibility()

    def sort_queue(self):
        if not self.queue.is_empty():
            self.queue.sort_queue()  
            self.update_queue_display(animated=False)
            messagebox.showinfo("Ordenação", "A fila foi ordenada.")
    
    def update_queue_display(self, animated=False):
        # Limpa os retângulos antigos
        self.canvas.delete("all")
        self.queue_items = []

        # Calcula posição inicial para o topo
        x_start = 50
        y_center = self.canvas.winfo_height() // 2

        queue_list = self.queue.print_queue()

        # Desenha cada elemento da fila
        for index, item in enumerate(queue_list):
            item_str = str(item)
            item_width = max(100, len(item_str) * 15)  # Largura ajustável com base no texto
            x_position = x_start + index * (item_width + 20)  # Espaço entre os elementos

            square = self.canvas.create_rectangle(
                x_position, y_center - 20, 
                x_position + item_width, y_center + 20,
                fill="lightblue"
            )

            if index == 0:
                text_str = f"Topo\n{item_str}"
            elif index == len(queue_list) - 1:
                text_str = f"Base\n{item_str}"
            else:
                text_str = item_str

            text = self.canvas.create_text(
                x_position + item_width // 2, y_center,
                text=text_str, font=("Arial", 16)
            )

            self.queue_items.append((square, text))

            # Se for para animar, move o quadrado da direita para a esquerda
            if animated:
                for step in range(10):
                    self.canvas.move(square, -2, 0)
                    self.canvas.move(text, -2, 0)
                    self.canvas.update()
                    time.sleep(0.02)

    def update_buttons_visibility(self):
        if self.queue.is_empty():
            self.button_dequeue.grid_remove()
            self.button_sort.grid_remove()
        else:
            self.button_dequeue.grid()
            self.button_sort.grid()

        if self.queue.is_full():
            self.button_enqueue.grid_remove()
            self.label_data.grid_remove()
            self.entry_data.grid_remove()
        else:
            self.button_enqueue.grid()
            self.label_data.grid()
            self.entry_data.grid()

# Criação da interface
root = tk.Tk()
app = StaticQueueGUI(root, 5)
root.mainloop()