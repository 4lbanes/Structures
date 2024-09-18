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
            self.head = new_node
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

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def from_list(self, lst):
        self.head = None
        self.tail = None
        self.size = 0
        for data in lst:
            self.add(data)

    def sort(self):
        if self.is_empty() or self.size == 1:
            return

        lst = self.to_list()

        def convert_if_possible(item):
            try:
                return float(item)
            except ValueError:
                return item

        lst_converted = [(convert_if_possible(item), item) for item in lst]

        def custom_key(item):
            converted_value, original_value = item
            return (isinstance(converted_value, float), converted_value)

        lst_converted.sort(key=custom_key)

        sorted_lst = [item[1] for item in lst_converted]
        self.from_list(sorted_lst)

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

class DoublyLinkedListGUI:
    def __init__(self, root, max_size):
        self.linked_list = DoublyLinkedList(max_size)
        self.root = root
        self.root.title("Lista Duplamente Encadeada: ")
        
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
        
        self.button_sort = tk.Button(root, text="Ordenar", command=self.sort_list) 
        self.button_sort.grid(row=4, column=0, columnspan=3, padx=10, pady=5)
        
        self.canvas = tk.Canvas(root, bg="white", height=600, width=1000)
        self.canvas.grid(row=7, column=0, columnspan=2)

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
    
    def sort_list(self):
        self.linked_list.sort()
        messagebox.showinfo("Ordenação", "Lista ordenada com sucesso!")
        self.update_list_display()

    def update_list_display(self):
        self.draw_doubly_linked_list()
        
    def draw_doubly_linked_list(self):
      self.canvas.delete("all")
      current = self.linked_list.head
      x_start = 50
      y_start = 50
      node_width = 60
      node_height = 40
      arrow_offset = 40

      if current:
        # Centraliza "null" e "head" em relação ao primeiro nó
         self.canvas.create_line(x_start - arrow_offset, y_start + node_height / 2, 
                                x_start, y_start + node_height / 2, arrow=tk.LAST)
         self.canvas.create_text(x_start - 30, y_start + node_height / 2, text="null", fill="black")
         self.canvas.create_text(x_start + node_width / 2, y_start - 20, text="head", fill="black")

      while current:
        # Desenha o retângulo para o nó atual
        self.canvas.create_rectangle(x_start, y_start, x_start + node_width, y_start + node_height, fill="lightblue")
        self.canvas.create_text(x_start + node_width / 2, y_start + node_height / 2, text=str(current.data))

        if current.next:
            # Seta do nó atual para o próximo (seta para frente)
            self.canvas.create_line(x_start + node_width, y_start + node_height / 2, 
                                    x_start + node_width + arrow_offset, y_start + node_height / 2, arrow=tk.LAST)
            # Seta do próximo nó de volta para o nó atual (seta para trás)
            self.canvas.create_line(x_start + node_width + arrow_offset - 10, y_start + node_height / 2 - 10, 
                                    x_start + node_width + 10, y_start + node_height / 2 - 10, arrow=tk.LAST)

        x_start += node_width + arrow_offset
        current = current.next

      if self.linked_list.tail:
        # Centraliza "tail" sobre o último nó
        self.canvas.create_text(x_start - node_width - arrow_offset, y_start - 20, text="tail", fill="black")

    # Adiciona "null" para o próximo do tail
      if self.linked_list.tail:
        self.canvas.create_line(x_start - arrow_offset, y_start + node_height / 2, 
                                x_start, y_start + node_height / 2, arrow=tk.LAST)
        self.canvas.create_text(x_start + 20, y_start + node_height / 2, text="null", fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    gui = DoublyLinkedListGUI(root, 10)
    root.mainloop() 
