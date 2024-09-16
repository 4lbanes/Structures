import tkinter as tk
from tkinter import simpledialog, messagebox

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class CircularDoublyLinkedList:
    
    def __init__(self, max_size):
        self.size_max = max_size
        self.size = 0
        self.head = None
        self.tail = None
    
    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.size_max
    
    def resize(self):
        self.size_max *= 2  # Aumenta o tamanho máximo da lista quando redimensionada
    
    def insert(self, data):
        if self.is_full():
            self.resize()  # Redimensionar a lista quando estiver cheia
    
        new_node = Node(data)
    
        if self.is_empty():
            self.head = self.tail = new_node
            self.head.next = self.head.prev = self.head  # Circularidade
        else:
            new_node.next = self.head
            new_node.prev = self.tail
            self.tail.next = new_node
            self.head.prev = new_node
            self.head = new_node  # Atualizando o novo head corretamente
    
        self.size += 1

    def add(self, data):
        if self.is_full():
            self.resize()  # Redimensionar a lista quando estiver cheia
        
        new_node = Node(data)

        if self.is_empty():
            self.head = self.tail = new_node
            self.head.next = self.head.prev = self.head  # Circularidade
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node
        
        self.size += 1

    def remove_first(self):
        if self.is_empty():
            print("A lista está vazia, não é possível remover elementos.")
            return None
    
        removed_value = self.head.data

        if self.size == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = self.tail
            self.tail.next = self.head
    
        self.size -= 1
        return removed_value
    
    def remove_last(self):
        if self.is_empty():
            print("A lista está vazia, não existem elementos para remover.")
            return None

        removed_value = self.tail.data

        if self.size == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = self.head
            self.head.prev = self.tail

        self.size -= 1
        return removed_value
    
    def remove_by_index(self, index):
        if self.is_empty():
            print("A lista está vazia, não existem elementos para remover.")
            return None

        if index < 0 or index >= self.size:
            print("Índice fora do intervalo.")
            return None
        
        if index == 0:
            return self.remove_first()
        elif index == self.size - 1:
            return self.remove_last()
        else:
            node_to_remove = self.get_node(index)
            removed_value = node_to_remove.data
            node_to_remove.prev.next = node_to_remove.next
            node_to_remove.next.prev = node_to_remove.prev
            self.size -= 1
            return removed_value

    def get_node(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Índice fora do intervalo.")
        
        current = self.head
        for _ in range(index):
            current = current.next
        
        return current
    def __str__(self):
     if self.is_empty():
        return "A lista está vazia"

     current = self.head
     elements = []
     for _ in range(self.size):
        elements.append(str(current.data))
        current = current.next

    # Adicionando a ligação circular explícita
     return " <-> ".join(elements) + f" (circular: head.prev -> {self.tail.data}, tail.next -> {self.head.data})"

# Interface gráfica com Tkinter
class CircularDoublyLinkedListGUI:
    def __init__(self, root, max_size):
        self.list = CircularDoublyLinkedList(max_size)
        self.root = root
        self.root.title("Listas Circulares: ")

        # Widgets
        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da lista: {max_size}")
        self.label_max_size.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='w')
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        self.button_add_last = tk.Button(root, text="Adicionar em Último", command=self.add_last)
        self.button_add_last.grid(row=2, column=0, padx=10, pady=5)
        
        self.button_add_first = tk.Button(root, text="Adicionar em Primeiro", command=self.add_first)
        self.button_add_first.grid(row=2, column=1, padx=10, pady=5)
        
        self.button_remove_first = tk.Button(root, text="Remover Primeiro", command=self.remove_first)
        self.button_remove_first.grid(row=3, column=0, padx=10, pady=5)
        
        self.button_remove_last = tk.Button(root, text="Remover Último", command=self.remove_last)
        self.button_remove_last.grid(row=3, column=1, padx=10, pady=5)
        
        self.button_remove_by_index = tk.Button(root, text="Remover por Índice", command=self.remove_by_index)
        self.button_remove_by_index.grid(row=3, column=2, padx=10, pady=5)
        
        self.label_index = tk.Label(root, text="Índice:")
        self.label_index.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.entry_index = tk.Entry(root)
        self.entry_index.grid(row=4, column=1, padx=10, pady=5, sticky='ew')
        
        self.stack_display = tk.Text(root, height=20, width=100)
        self.stack_display.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        root.grid_rowconfigure(5, weight=1)
        root.grid_columnconfigure(1, weight=1)
        self.update_list_display()
    
    def add_last(self):
        data = self.entry_data.get()
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        self.list.add(data)
        self.update_list_display()
        self.entry_data.delete(0, tk.END)
    
    def add_first(self):
        data = self.entry_data.get()
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        self.list.insert(data)
        self.update_list_display()
        self.entry_data.delete(0, tk.END)
    
    def remove_first(self):
        self.list.remove_first()
        self.update_list_display()
    
    def remove_last(self):
        self.list.remove_last()
        self.update_list_display()
    
    def remove_by_index(self):
        index = self.entry_index.get()
        if not index.isdigit():
            messagebox.showerror("Erro", "Índice inválido!")
            return
        index = int(index)
        if index < 0 or index >= self.list.size:
            messagebox.showerror("Erro", "Índice fora do intervalo!")
            return
        self.list.remove_by_index(index)
        self.update_list_display()
    
    def update_buttons_visibility(self):
        if self.list.is_empty():
            self.button_remove_first.grid_forget()
            self.button_remove_last.grid_forget()
            self.button_remove_by_index.grid_forget()
        else:
            self.button_remove_first.grid(row=3, column=0, padx=10, pady=5)
            self.button_remove_last.grid(row=3, column=1, padx=10, pady=5)
            self.button_remove_by_index.grid(row=3, column=2, padx=10, pady=5)
    
    def update_list_display(self):
        self.stack_display.delete(1.0, tk.END)
        self.stack_display.insert(tk.END, str(self.list) + "\n")
        self.update_buttons_visibility()


cldl = CircularDoublyLinkedList(5)

# Criação da interface
root = tk.Tk()
app = CircularDoublyLinkedListGUI(root, cldl)
root.mainloop()
