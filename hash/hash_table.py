import tkinter as tk
from tkinter import ttk

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"{self.key}: {self.value}"

class Node:
    def __init__(self, entry):
        self.entry = entry
        self.next = None
        self.previous = None

class HashTable:
    def __init__(self, map_size):
        self.size = 0
        self.hash_table = [None] * map_size

    def hash_code(self, key):
        hash_code = 0
        a = 5

        for char in key:
            hash_code = (hash_code << a) | (hash_code >> (32 - a))
            hash_code += ord(char)

        return hash_code

    def compression(self, hash_code):
        comp = hash_code % len(self.hash_table)
        return abs(comp)

    def hash_function(self, key):
        if isinstance(key, str):
            return self.compression(self.hash_code(key))
        raise RuntimeError("Hash Function does not support that data type")

    def put(self, key, value):
        index = self.hash_function(key)
        entry = Entry(key, value)
        new_node = Node(entry)

        if self.hash_table[index] is None:
            self.hash_table[index] = new_node
        else:
            aux_node = self.hash_table[index]

            while aux_node is not None:
                if aux_node.entry.key == key:
                    aux_node.entry.value = value
                    return
                aux_node = aux_node.next

            new_node.next = self.hash_table[index]
            self.hash_table[index].previous = new_node
            self.hash_table[index] = new_node

        self.size += 1

    def get(self, key):
        index = self.hash_function(key)
        aux_node = self.hash_table[index]

        while aux_node is not None:
            if aux_node.entry.key == key:
                return aux_node.entry
            aux_node = aux_node.next

        return None

    def delete(self, key):
        index = self.hash_function(key)
        aux_node = self.hash_table[index]

        while aux_node is not None:
            if aux_node.entry.key == key:
                if aux_node.previous:
                    aux_node.previous.next = aux_node.next
                if aux_node.next:
                    aux_node.next.previous = aux_node.previous
                if aux_node == self.hash_table[index]:
                    self.hash_table[index] = aux_node.next
                self.size -= 1
                return aux_node.entry
            aux_node = aux_node.next

        return None

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __repr__(self):
        sb = []
        for i in range(len(self.hash_table)):
            sb.append(f"{i}:")
            aux_node = self.hash_table[i]
            while aux_node is not None:
                sb.append(f"\n    {aux_node.entry}")
                aux_node = aux_node.next
            sb.append("\n")
        return ''.join(sb)

class HashTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabelas Hash:")

        self.hash_table = HashTable(10)

        # Canvas para desenhar a tabela hash
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Frame para controles
        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(pady=10)

        # Entradas e botões
        self.key_entry = ttk.Entry(self.control_frame, width=15)
        self.key_entry.grid(row=0, column=0, padx=5)
        self.value_entry = ttk.Entry(self.control_frame, width=15)
        self.value_entry.grid(row=0, column=1, padx=5)

        ttk.Button(self.control_frame, text="Adicionar", command=self.add_entry).grid(row=0, column=2, padx=5)
        ttk.Button(self.control_frame, text="Remover", command=self.remove_entry).grid(row=0, column=3, padx=5)
        ttk.Button(self.control_frame, text="Atualizar", command=self.update_display).grid(row=1, column=0, columnspan=4, pady=5)

        self.update_display()

    def add_entry(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        if key and value:
            self.hash_table.put(key, value)
            self.key_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
            self.update_display()

    def remove_entry(self):
        key = self.key_entry.get()
        if key:
            self.hash_table.delete(key)
            self.key_entry.delete(0, tk.END)
            self.update_display()

    def update_display(self):
        self.canvas.delete("all")

        # Desenhar a tabela hash
        x_start = 50
        y_start = 50
        radius = 20
        for i in range(len(self.hash_table.hash_table)):
            node = self.hash_table.hash_table[i]
            x = x_start + i * 100
            self.canvas.create_oval(x - radius, y_start - radius, x + radius, y_start + radius, fill='lightblue', outline='black')
            self.canvas.create_text(x, y_start, text=str(i), font=('Arial', 12, 'bold'))

            while node:
                y_offset = 30
                self.canvas.create_rectangle(x - radius, y_start + y_offset - 10, x + radius, y_start + y_offset + 10, fill='lightgreen', outline='black')
                self.canvas.create_text(x, y_start + y_offset, text=f"{node.entry.key}: {node.entry.value}", font=('Arial', 10))
                y_offset += 30
                node = node.next

if __name__ == "__main__":
    root = tk.Tk()
    app = HashTableGUI(root)
    root.mainloop()
