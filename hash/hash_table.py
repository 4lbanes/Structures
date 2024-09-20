import tkinter as tk
from tkinter import ttk

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"K:{self.key}, V:{self.value}"

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
        return abs(hash_code % len(self.hash_table))

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
            self.size += 1  # Increment size for new key
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
            self.size += 1  # Increment size for new key

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
            self.size -= 1  # Decrement size only when an entry is actually removed
            return aux_node.entry
        aux_node = aux_node.next

     return None


    def __len__(self):
     return max(self.size, 0)
class HashTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabela Hash: ")

        self.hash_table = HashTable(10)

        # Frame para controles
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Labels e Entradas
        self.key_label = ttk.Label(self.control_frame, text="Chave:")
        self.key_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.key_entry = ttk.Entry(self.control_frame, width=20)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        self.value_label = ttk.Label(self.control_frame, text="Valor:")
        self.value_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.value_entry = ttk.Entry(self.control_frame, width=20)
        self.value_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.control_frame, text="Adicionar", command=self.add_entry).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Remover", command=self.remove_entry).grid(row=2, column=1, padx=5, pady=5)

        self.info_label = ttk.Label(self.control_frame, text="Tamanho: 0")
        self.info_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Canvas para desenhar a tabela hash
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.update_display()
        
    def update_display(self):
        self.canvas.delete("all")
        self.info_label.config(text=f"Tamanho: {len(self.hash_table)}")

        x_start = 50
        y_start = 50
        radius = 50
        margin_top = 20
        margin_between_nodes = 30

        for i in range(len(self.hash_table.hash_table)):
            node = self.hash_table.hash_table[i]
            x = x_start + i * 100
            self.canvas.create_rectangle(x - radius, y_start - radius, x + radius, y_start + radius, fill='lightblue', outline='black')
            self.canvas.create_text(x, y_start, text=str(i), font=('Arial', 12, 'bold'))

            y_offset = radius + margin_top
            while node:
                # Limitar tamanho da chave e valor
                key_text = node.entry.key if len(node.entry.key) <= 10 else node.entry.key[:7] + "..."
                value_text = node.entry.value if len(str(node.entry.value)) <= 10 else str(node.entry.value)[:7] + "..."
                text = f"Chave: {key_text}\nValor: {value_text}"
                self.canvas.create_rectangle(x - radius, y_start + y_offset - 20, x + radius, y_start + y_offset + 20, outline='black', fill='lightgray')
                self.canvas.create_text(x, y_start + y_offset, text=text, font=('Arial', 6), anchor='n')

                y_offset += margin_between_nodes + 40
                node = node.next
        
    def animate_hashing(self, key, value):
        self.canvas.delete("all")
        self.canvas.create_text(300, 50, text=f"Calculando hash para a chave '{key}'", font=('Arial', 14, 'bold'))

        hash_code = 0
        a = 5
        y_start = 50
        # Fase 1: Mostrar cada caractere e seu valor ASCII
        for i, char in enumerate(key):
            self.canvas.create_text(300, 100 + i * 30, text=f"{char} -> ASCII: {ord(char)}", font=('Arial', 12))
            self.root.update()
            self.root.after(500)  # Pausa de 500 ms para simular o processamento
            hash_code = (hash_code << a) | (hash_code >> (32 - a))
            hash_code += ord(char)

        # Mostrar o hash_code resultante
        self.canvas.create_text(300, 100 + len(key) * 30, text=f"Hash code final: {hash_code}", font=('Arial', 14))
        self.root.update()
        self.root.after(1000)

        # Fase 2: Animar o processo de compressão para encontrar o índice
        self.canvas.create_text(300, 150 + len(key) * 30, text="Aplicando compressão para calcular o índice...", font=('Arial', 12))
        self.root.update()
        self.root.after(1000)

        # Fórmula de compressão com os números reais
        index = self.hash_table.compression(hash_code)
        formula_text = f"Índice = {hash_code} % {len(self.hash_table.hash_table)} = {index}"
        self.canvas.create_text(300, 180 + len(key) * 30, text=formula_text, font=('Arial', 14, 'bold'))
        self.root.update()
        self.root.after(1000)  # Deixar a fórmula visível por mais tempo (3 segundos)

        # Inserir o valor na tabela hash após a animação
        self.root.after(3000, lambda: self.animate_insert(key, value))

    def remove_entry(self):
        key = self.key_entry.get()
        if key:
            self.hash_table.delete(key)
            self.key_entry.delete(0, tk.END)
            self.update_display()
            
    def animate_insert(self, key, value):
     index = self.hash_table.hash_function(key)
     entry = Entry(key, value)
     new_node = Node(entry)
     collision_detected = False

     if self.hash_table.hash_table[index] is None:
        self.hash_table.hash_table[index] = new_node
        self.hash_table.size += 1  # Incrementar o tamanho corretamente aqui
     else:
        aux_node = self.hash_table.hash_table[index]
        while aux_node is not None:
            if aux_node.entry.key == key:
                old_value = aux_node.entry.value
                aux_node.entry.value = value
                # Exibir a mensagem de atualização
                self.canvas.create_text(800, 100, text=f"Atualização de valor no índice {index}:", font=('Arial', 12, 'bold'), fill='blue')
                self.canvas.create_text(800, 130, text=f"Valor antigo -> {old_value}", font=('Arial', 12, 'bold'), fill='blue')
                self.canvas.create_text(800, 160, text=f"Valor novo -> {value}", font=('Arial', 12, 'bold'), fill='blue')
                self.root.update()
                self.root.after(2000)
                self.update_display()  # Atualizar a interface gráfica após a inserção
                return
            aux_node = aux_node.next

        # Colisão detectada
        collision_detected = True
        self.canvas.create_text(500, 200, text=f"Colisão detectada no índice {index}!", font=('Arial', 14, 'bold'), fill='red')
        self.root.update()
        self.root.after(1000)

        # Mover o nó existente para baixo
        y_offset = 60
        old_key_text = self.canvas.create_text(100 + index * 100, y_offset + 20, text=f"{self.hash_table.hash_table[index].entry.key}", font=('Arial', 12), fill='red')
        old_value_text = self.canvas.create_text(100 + index * 100, y_offset + 40, text=f"{self.hash_table.hash_table[index].entry.value}", font=('Arial', 12), fill='red')
        
        for _ in range(10):  # Animação descendo o nó antigo
            self.canvas.move(old_key_text, 0, 5)
            self.canvas.move(old_value_text, 0, 5)
            self.root.update()
            self.root.after(100)

        new_node.next = self.hash_table.hash_table[index]
        self.hash_table.hash_table[index].previous = new_node
        self.hash_table.hash_table[index] = new_node
        self.hash_table.size += 1  # Incrementar o tamanho corretamente aqui

     self.update_display()  # Atualizar a interface gráfica após a animação
    
    def add_entry(self):
     key = self.key_entry.get()
     value = self.value_entry.get()
     if key and value:
        self.animate_hashing(key, value)
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.update_display()  # Certifique-se de atualizar o display ao final

root = tk.Tk()
app = HashTableGUI(root)
root.mainloop()
