import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
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
            self.head.prev = new_node
        
        self.head = new_node
        self.size += 1

    def add(self, data):
        if self.is_full():
            self.resize()
        
        new_node = Node(data)

        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
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
            self.head.prev = None
    
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
            self.tail.next = None

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
    
    def get(self, index):
        if self.is_empty():
            print("A lista está vazia, não existem elementos para buscar.")
            return None

        if index < 0 or index >= self.size:
            print("Índice fora do intervalo.")
            return None

        node = self.get_node(index)
        return node.data

    def set(self, index, new_data):
        if self.is_empty():
            print("A lista está vazia, não existem elementos para alterar.")
            return None

        if index < 0 or index >= self.size:
            print("Índice fora do intervalo.")
            return None

        node = self.get_node(index)
        node.data = new_data
        
    def indexof(self, data):
        if self.is_empty():
            print("A lista está vazia, não existem elementos para alterar.")
            return None
        
        index = 0
        
        aux_node = self.head
        
        while aux_node is not None:
            if aux_node.data == data:
                return index
            
            aux_node = aux_node.next
            index += 1
        
        return -1
    
    def remove_last_occurrence(self, data):
        if self.is_empty():
            print("A lista está vazia, não existem elementos para alterar.")
            return None
        
        for i in range(self.size - 1, -1, -1):
            if self.get(i) == data:
                self.remove_by_index(i)
                break

    def to_list(self):
        """Converte a lista encadeada em uma lista Python."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def from_list(self, lst):
        """Cria uma lista encadeada a partir de uma lista Python."""
        self.head = None
        self.tail = None
        self.size = 0
        for data in lst:
            self.add(data)
            
    def sort(self):
        if self.is_empty() or self.size == 1:
            return

        # Converte a lista encadeada para uma lista Python
        lst = self.to_list()

        def convert_if_possible(item):
            # Tenta converter para float, se falhar, mantém como string
            try:
                return float(item)
            except ValueError:
                return item

        # Converte os dados para números quando possível, mantendo strings intactas
        lst_converted = [(convert_if_possible(item), item) for item in lst]

        # Função personalizada para a ordenação
        def custom_key(item):
            converted_value, original_value = item
            # Prioriza strings sobre números
            return (isinstance(converted_value, float), converted_value)

        # Ordena a lista Python com base no valor convertido
        lst_converted.sort(key=custom_key)

        # Recria a lista encadeada a partir da lista Python ordenada
        sorted_lst = [item[1] for item in lst_converted]
        self.from_list(sorted_lst)

    def __str__(self):
        if self.is_empty():
            return "A lista está vazia"
        
        current = self.head
        list_str = "[null <- "
        
        while current:
            list_str += f"{current.data}"
            current = current.next
            if current:
                list_str += " <-> "
        
        list_str += " -> null]"
        return list_str

    def reverse(self):
        if self.is_empty():
            return "A lista está vazia"
        
        current = self.tail
        list_str = "[null <- "
        
        while current:
            list_str += f"{current.data}"
            current = current.prev
            if current:
                list_str += " <-> "
        
        list_str += " -> null]"
        return list_str

class DoublyLinkedListGUI:
    def __init__(self, root, max_size):
        self.list = DoublyLinkedList(max_size)
        self.root = root
        self.root.title("Lista Duplamente Encadeada: ")
        
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
        
        self.button_sort = tk.Button(root, text="Ordenar", command=self.sort)
        self.button_sort.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        self.label_index = tk.Label(root, text="Índice:")
        self.label_index.grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.entry_index = tk.Entry(root)
        self.entry_index.grid(row=5, column=1, padx=10, pady=5, sticky='ew')
        
        self.stack_display = tk.Text(root, height=20, width=100)
        self.stack_display.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        # Configure row and column weights to expand widgets
        root.grid_rowconfigure(6, weight=1)
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
        self.stack_display.insert(tk.END, "Lista Direta: " + str(self.list) + "\n")
        self.stack_display.insert(tk.END, "Lista Reversa: " + self.list.reverse() + "\n")
        self.update_buttons_visibility()

    def sort(self):
        self.list.sort()
        self.update_list_display()

# Criação da interface
root = tk.Tk()
app = DoublyLinkedListGUI(root, 5)
root.mainloop()
