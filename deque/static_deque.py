import tkinter as tk
import time

class StaticDeque:
    def __init__(self, max_size):
        self.deque = [None] * max_size
        self.size = 0
        self.first = 0
        self.max_size = max_size

    def is_full(self):
        return self.size == len(self.deque)

    def is_empty(self):
        return self.size == 0

    def add(self, value):
        if not self.is_full():
            index = (self.first + self.size) % len(self.deque)
            self.deque[index] = value
            self.size += 1
            return index

    def insert(self, value):
        if not self.is_full():
            self.first = (self.first - 1 + len(self.deque)) % len(self.deque)
            self.deque[self.first] = value
            self.size += 1
            return self.first

    def remove_first(self):
        if not self.is_empty():
            value = self.deque[self.first]
            self.deque[self.first] = None
            self.first = (self.first + 1) % len(self.deque)
            self.size -= 1
            return value, self.first

    def remove_last(self):
        if not self.is_empty():
            last_index = (self.first + self.size - 1) % len(self.deque)
            value = self.deque[last_index]
            self.deque[last_index] = None
            self.size -= 1
            return value, last_index

# Interface gráfica com Tkinter

class DequeGUI:
    def __init__(self, root):
        self.deque = StaticDeque(5)
        self.root = root
        self.root.title("Deque Estático: ")

        # Label de input
        self.label = tk.Label(root, text="Insira o valor:")
        self.label.pack(pady=5)
        
        # Caixa de input
        self.input_value = tk.Entry(root)
        self.input_value.pack(pady=5)

        # Canvas para visualização do deque
        self.canvas = tk.Canvas(root, width=500, height=100, bg='lightblue')
        self.canvas.pack(pady=10)

        # Botões de inserção e remoção
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.insert_btn = tk.Button(self.btn_frame, text="Inserir em Primeiro", command=self.insert_first)
        self.insert_btn.grid(row=0, column=0, padx=5)

        self.add_btn = tk.Button(self.btn_frame, text="Adicionar em Último", command=self.add_last)
        self.add_btn.grid(row=0, column=1, padx=5)

        self.remove_first_btn = tk.Button(self.btn_frame, text="Remover Primeiro", command=self.remove_first)
        self.remove_first_btn.grid(row=0, column=2, padx=5)

        self.remove_last_btn = tk.Button(self.btn_frame, text="Remover Último", command=self.remove_last)
        self.remove_last_btn.grid(row=0, column=3, padx=5)

        # Rótulo para mostrar as fórmulas usadas na operação
        self.formula_label = tk.Label(root, text="Fórmula: ", font=("Arial", 14), fg="blue")
        self.formula_label.pack(pady=10)

        self.update_canvas()
        self.update_buttons()

    def insert_first(self):
        value = self.input_value.get()
        if value:
            index = self.deque.insert(value)
            formula = f"Índice = (first - 1 + max_size) % max_size\nÍndice = ({(self.deque.first + 1)} - 1 + {self.deque.max_size}) % {self.deque.max_size} = {index}"
            self.formula_label.config(text=f"Fórmula: {formula}")
            self.update_canvas()
            self.update_buttons()

    def add_last(self):
        value = self.input_value.get()
        if value:
            index = self.deque.add(value)
            formula = f"Índice = (first + size) % max_size\nÍndice = ({self.deque.first} + {self.deque.size - 1}) % {self.deque.max_size} = {index}"
            self.formula_label.config(text=f"Fórmula: {formula}")
            self.update_canvas()
            self.update_buttons()

    def remove_first(self):
        removed_value, new_first = self.deque.remove_first()
        formula = f"Novo first = (first + 1) % max_size\nNovo first = ({new_first - 1}) + 1 % {self.deque.max_size} = {new_first}"
        self.formula_label.config(text=f"Fórmula: {formula}")
        self.update_canvas()
        self.update_buttons()

    def remove_last(self):
        removed_value, last_index = self.deque.remove_last()
        formula = f"Índice do último = (first + size - 1) % max_size\nÍndice = ({self.deque.first} + {self.deque.size} - 1) % {self.deque.max_size} = {last_index}"
        self.formula_label.config(text=f"Fórmula: {formula}")
        self.update_canvas()
        self.update_buttons()

    def update_buttons(self):
        # Controlar visibilidade dos botões de remoção e inserção
        if self.deque.is_empty():
            self.remove_first_btn.grid_remove()
            self.remove_last_btn.grid_remove()
        else:
            self.remove_first_btn.grid()
            self.remove_last_btn.grid()

        if self.deque.is_full():
            self.insert_btn.grid_remove()
            self.add_btn.grid_remove()
        else:
            self.insert_btn.grid()
            self.add_btn.grid()

    def update_canvas(self):
        # Atualizar visualização do deque
        self.canvas.delete("all")
        for i, value in enumerate(self.deque.deque):
            x = 50 + i * 80
            self.canvas.create_rectangle(x, 40, x + 60, 80, fill='white')
            if value is not None:
                self.canvas.create_text(x + 30, 60, text=value, font=("Arial", 16))
            else:
                self.canvas.create_text(x + 30, 60, text="None", font=("Arial", 16))

if __name__ == "__main__":
    root = tk.Tk()
    app = DequeGUI(root)
    root.mainloop()  
