import tkinter as tk
from tkinter import messagebox
import time
import math

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class CircularLinkedQueue:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def enqueue(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.first = new_node
            self.last = new_node
            new_node.next = new_node  # Aponta para ele mesmo
        else:
            self.last.next = new_node
            new_node.next = self.first
            self.last = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            print("Queue is Empty")
            return None

        value = self.first.value
        if self.size == 1:
            self.first = None
            self.last = None
        else:
            self.last.next = self.first.next
            self.first = self.first.next
        self.size -= 1
        return value

    def print_queue(self):
        if self.is_empty():
            return []
        result = []
        current = self.first
        for _ in range(self.size):
            result.append(current.value)
            current = current.next
        return result

    def merge_sort(self, lst):
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2
        left_half = self.merge_sort(lst[:mid])
        right_half = self.merge_sort(lst[mid:])

        return self.merge(left_half, right_half)

    def merge(self, left, right):
        result = []
        while left and right:
            if left[0] <= right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left or right)
        return result

class CircularQueueGUI:
    def __init__(self, root):
        self.queue = CircularLinkedQueue()
        self.root = root
        self.root.title("Fila Circular: ")

        self.canvas = tk.Canvas(root, bg="white", height=400, width=800)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=1, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=1, column=1)
        
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue, bg="lightblue", fg="black")
        self.button_enqueue.grid(row=2, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue, bg="lightblue", fg="black")
        self.button_dequeue.grid(row=3, column=0, columnspan=2)

        self.button_sort = tk.Button(root, text="Ordenar Fila", command=self.sort_queue, bg="lightblue", fg="black")
        self.button_sort.grid(row=4, column=0, columnspan=2)

        self.queue_items = []  # Armazena os retângulos e textos na tela
        self.update_queue_display()

    def enqueue(self):
        data = self.entry_data.get()

        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        self.queue.enqueue(int(data))  # Converte para inteiro
        self.entry_data.delete(0, tk.END)
        
        self.update_queue_display(animated=True)

    def dequeue(self):
        if self.queue.is_empty():
            messagebox.showwarning("Aviso", "A fila está vazia.")
            return
        
        removed = self.queue.dequeue()
        messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        self.update_queue_display()

    def sort_queue(self):
        if self.queue.is_empty():
            messagebox.showwarning("Aviso", "A fila está vazia. Não há nada para ordenar.")
            return
        
        queue_list = self.queue.print_queue()
        sorted_list = self.queue.merge_sort(queue_list)
        
        # Limpa a fila atual e insere os elementos ordenados
        self.queue = CircularLinkedQueue()
        for item in sorted_list:
            self.queue.enqueue(item)

        self.update_queue_display()

    def update_queue_display(self, animated=False):
        # Limpa os retângulos antigos
        self.canvas.delete("all")
        self.queue_items = []

        # Calcula posição central
        center_x = self.canvas.winfo_width() // 2
        center_y = self.canvas.winfo_height() // 2
        radius = 100  # Raio do círculo

        queue_list = self.queue.print_queue()

        # Desenha cada elemento da fila em um formato circular
        for index, item in enumerate(queue_list):
            angle = 2 * math.pi * index / len(queue_list)
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

            # Indicar o topo da fila
            if index == 0:
                self.canvas.create_text(x_position + 50, y_position + 10, text="Topo", fill="black", font=("Arial", 8, 'bold'))

            # Indicar a base da fila, apenas se houver mais de um elemento
            if index == len(queue_list) - 1 and len(queue_list) > 1:
                self.canvas.create_text(x_position + 50, y_position + 30, text="Base", fill="black", font=("Arial", 8, 'bold'))

            # Desenha setas entre os elementos
            if index < len(queue_list) - 1:
                next_angle = 2 * math.pi * (index + 1) / len(queue_list)
                next_x = center_x + radius * math.cos(next_angle)
                next_y = center_y + radius * math.sin(next_angle)

                self.canvas.create_line(
                    x_position + 100, y_position + 20,
                    next_x, next_y + 20,
                    arrow=tk.LAST, fill="black", width=2
                )

        # Controle de visibilidade do botão de remoção
        if self.queue.is_empty():
            self.button_dequeue.grid_forget()  # Oculta o botão se a fila estiver vazia
            self.button_sort.grid_forget()
        else:
            self.button_dequeue.grid(row=3, column=0, columnspan=2)  
            self.button_sort.grid(row=4, column=0, columnspan=2)

# Criação da interface
root = tk.Tk()
app = CircularQueueGUI(root)
root.mainloop()
