import tkinter as tk
from tkinter import simpledialog, messagebox

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
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
        self.size_max *= 2
    
    def insert(self, data):
        if self.is_full():
            self.resize()
        
        new_node = Node(data)
        
        if self.is_empty():
            self.tail = new_node
        else:
            new_node.next = self.head
        
        self.head = new_node
        self.size += 1

    def add(self, data):
        if self.is_full():
            self.resize()
        
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        
        self.tail = new_node
        self.size += 1

    def remove_first(self):
        if self.is_empty():
            print("A lista está vazia, não é possível remover elementos.")
            return None
    
        removed_value = self.head.data

        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
    
        self.size -= 1
        return removed_value
    
    def get_node(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Índice fora do intervalo.")
        
        current = self.head
        for _ in range(index):
            current = current.next
        
        return current
    
    def remove_last(self):
        if self.is_empty():
            print("A lista está vazia, não existem elementos para remover.")
            return None
        
        removed_value = self.tail.data

        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            aux_node = self.head
            while aux_node.next != self.tail:
                aux_node = aux_node.next
            aux_node.next = None
            self.tail = aux_node

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
            prev_node = self.get_node(index - 1)
            node_to_remove = prev_node.next
            removed_value = node_to_remove.data
            prev_node.next = node_to_remove.next

            if node_to_remove == self.tail:
                self.tail = prev_node

            self.size -= 1
            return removed_value

    def __str__(self):
        if self.is_empty():
            return "A lista está vazia"
        
        current = self.head
        list_str = ""

        while current:
            list_str += str(current.data)
            current = current.next
            if current:
                list_str += " -> "
        
        list_str += " -> null"
        return list_str

class LinkedListGUI:
    def __init__(self, root, max_size):
        self.linked_list = LinkedList(max_size)
        self.root = root
        self.root.title("Lista Simplesmente Encadeada: ")
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=1, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=1, column=1)
        
        self.button_insert = tk.Button(root, text="Inserir em primeiro", command=self.insert)
        self.button_insert.grid(row=2, column=0, columnspan=2)
        
        self.button_add = tk.Button(root, text="Inserir em último", command=self.add)
        self.button_add.grid(row=2, column=1, columnspan=2)
        
        self.button_remove_first = tk.Button(root, text="Remover Primeiro", command=self.remove_first)
        self.button_remove_first.grid(row=3, column=0, columnspan=2)
        
        self.button_remove_last = tk.Button(root, text="Remover Último", command=self.remove_last)
        self.button_remove_last.grid(row=3, column=1, columnspan=2)
        
        self.label_index = tk.Label(root, text="Índice para Remover:")
        self.label_index.grid(row=5, column=0)
        self.entry_index = tk.Entry(root)
        self.entry_index.grid(row=5, column=1)
        self.button_remove_index = tk.Button(root, text="Remover por Índice", command=self.remove_by_index)
        self.button_remove_index.grid(row=6, column=0, columnspan=2)
        
        self.list_display = tk.Text(root, height=10, width=50)
        self.list_display.grid(row=7, column=0, columnspan=2)
        
        self.update_list_display()
    
    def insert(self):
        data = self.entry_data.get()
        
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        self.linked_list.insert(data)
        self.update_list_display()
        self.entry_data.delete(0, tk.END)
    
    def add(self):
        data = self.entry_data.get()
        
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        self.linked_list.add(data)
        self.update_list_display()
        self.entry_data.delete(0, tk.END)
    
    def remove_first(self):
        removed = self.linked_list.remove_first()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        self.update_list_display()
    
    def remove_last(self):
        removed = self.linked_list.remove_last()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        self.update_list_display()
    
    def remove_by_index(self):
        index = self.entry_index.get()
        if not index.isdigit():
            messagebox.showerror("Erro", "Índice deve ser um número!")
            return
        
        index = int(index)
        removed = self.linked_list.remove_by_index(index)
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        self.update_list_display()
    
    def update_list_display(self):
        self.list_display.delete(1.0, tk.END)
        self.list_display.insert(tk.END, str(self.linked_list))

ll = LinkedList(5)

# Criação da interface
root = tk.Tk()
app = LinkedListGUI(root, ll)
root.mainloop()
