import tkinter as tk
from tkinter import messagebox
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DynamicQueue:
    def __init__(self):
        self.front = None  # O início da fila
        self.rear = None   # O final da fila
        self.size = 0      # Tamanho da fila
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:  # Se a fila estiver vazia
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1
        print(f"{item} foi adicionado à fila.")
    
    def dequeue(self):
        if self.is_empty():
            print("A fila está vazia.")
            return None
        
        removed_value = self.front.data
        self.front = self.front.next
        if self.front is None:  # Se a fila ficou vazia
            self.rear = None
        
        self.size -= 1
        print(f"{removed_value} foi removido da fila.")
        return removed_value
    
    def peek(self):  # Retorna o primeiro elemento da fila
        if self.is_empty():
            print("A fila está vazia.")
            return None
        return self.front.data
    
    def sort_queue(self):
     if self.is_empty():
        return
    
     nodes = []
     current = self.front
     while current:
        try:
            nodes.append(int(current.data))
        except ValueError:
            nodes.append(current.data)
        current = current.next
    
    # Ordena primeiro números, depois strings
     nodes.sort(key=lambda x: (isinstance(x, str), x))
    
    # Reconstrói a fila ordenada
     self.front = None
     self.rear = None
     self.size = 0
     for data in nodes:
       self.enqueue(data)
    
    def print_queue(self):
        if self.is_empty():
            return []
        
        current = self.front
        queue_list = []
        while current:
            queue_list.append(current.data)
            current = current.next
        return queue_list

# Interface com Tkinter
class DynamicQueueGUI:
    def __init__(self, root, max_size):
        self.queue = DynamicQueue()  
        self.root = root
        self.root.title("Fila Dinâmica: ")

        self.canvas = tk.Canvas(root, bg="white", height=400, width=800)
        self.canvas.grid(row=0, column=0, columnspan=3)
        
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

# Criação da interface
root = tk.Tk()
app = DynamicQueueGUI(root, 5)
root.mainloop()