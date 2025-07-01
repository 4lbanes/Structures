import tkinter as tk
import tkinter.font as tkFont
import time

class DictionaryVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dicionários")
        self.dict_data = {}

        # Frame da esquerda para controles
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Canvas para visualização gráfica
        self.canvas = tk.Canvas(self, width=700, height=250, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Entrada para adicionar chave
        self.key_label = tk.Label(self.left_frame, text="Chave:")
        self.key_label.pack()
        self.key_entry = tk.Entry(self.left_frame)
        self.key_entry.pack()

        # Entrada para adicionar valor
        self.value_label = tk.Label(self.left_frame, text="Valor:")
        self.value_label.pack()
        self.value_entry = tk.Entry(self.left_frame)
        self.value_entry.pack()

        # Botão para adicionar par chave-valor
        self.add_button = tk.Button(self.left_frame, text="Adicionar par (chave:valor)", command=self.add_pair, bg="lightblue")
        self.add_button.pack(pady=5)

        # Entrada para buscar valor pela chave
        self.search_key_label = tk.Label(self.left_frame, text="Buscar valor pela chave:")
        self.search_key_label.pack()
        self.search_key_entry = tk.Entry(self.left_frame)
        self.search_key_entry.pack()
        self.search_key_button = tk.Button(self.left_frame, text="Buscar valor", command=self.search_by_key, bg="lightblue")
        self.search_key_button.pack(pady=5)

        # Entrada para buscar chave pelo valor
        self.search_value_label = tk.Label(self.left_frame, text="Buscar chave(s) pelo valor:")
        self.search_value_label.pack()
        self.search_value_entry = tk.Entry(self.left_frame)
        self.search_value_entry.pack()
        self.search_value_button = tk.Button(self.left_frame, text="Buscar chave(s)", command=self.search_by_value, bg="lightblue")
        self.search_value_button.pack(pady=5)

        # Botão para contar quantas vezes um valor aparece
        self.count_button = tk.Button(self.left_frame, text="Contar ocorrências de valor", command=self.count_value, bg="lightblue")
        self.count_button.pack(pady=5)

        # Botão para exibir tamanho do dicionário
        self.size_button = tk.Button(self.left_frame, text="Mostrar tamanho do dicionário", command=self.show_size, bg="lightblue")
        self.size_button.pack(pady=5)

        # Botão para exibir dicionário completo
        self.display_button = tk.Button(self.left_frame, text="Exibir dicionário", command=self.display_dict, bg="lightblue")
        self.display_button.pack(pady=5)

        # Caixa de texto para saídas
        self.output_text = tk.Text(self.left_frame, height=12, width=40)
        self.output_text.pack(pady=5)

    def add_pair(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        if not key:
            self.output_text.insert(tk.END, "A chave não pode ser vazia!\n")
            return

        # Converter valor para int se possível
        if value.isdigit():
            value = int(value)

        self.dict_data[key] = value

        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.output_text.insert(tk.END, f"Par ({key}: {value}) adicionado!\n")
        self.display_dict()

    def display_dict(self):
        self.canvas.delete("all")
        font = tkFont.Font(family="Arial", size=12)
        padding = 10
        x = 50
        y = 120

        # Desenhar pares chave:valor como caixas no canvas
        for key, value in self.dict_data.items():
            text = f"{key}: {value}"
            text_width = font.measure(text)
            box_width = text_width + padding * 2

            self.canvas.create_rectangle(x, y - 20, x + box_width, y + 20, fill="lightgreen")
            self.canvas.create_text(x + box_width // 2, y, text=text, font=font)
            x += box_width + 15  # espaçamento entre caixas

        self.output_text.insert(tk.END, f"\nDicionário atual: {self.dict_data}\n")

    def search_by_key(self):
        key = self.search_key_entry.get()
        if key in self.dict_data:
            value = self.dict_data[key]
            self.output_text.insert(tk.END, f"Valor para a chave '{key}': {value}\n")
        else:
            self.output_text.insert(tk.END, f"Chave '{key}' não encontrada.\n")

    def search_by_value(self):
        val = self.search_value_entry.get()
        if val.isdigit():
            val = int(val)
        found_keys = [k for k, v in self.dict_data.items() if v == val]
        if found_keys:
            self.output_text.insert(tk.END, f"Chave(s) com valor {val}: {found_keys}\n")
        else:
            self.output_text.insert(tk.END, f"Nenhuma chave encontrada com valor {val}.\n")

    def count_value(self):
        val = self.search_value_entry.get()
        if val.isdigit():
            val = int(val)
        count = sum(1 for v in self.dict_data.values() if v == val)
        self.output_text.insert(tk.END, f"Valor {val} ocorre {count} vez(es) no dicionário.\n")

    def show_size(self):
        size = len(self.dict_data)
        self.output_text.insert(tk.END, f"Tamanho do dicionário: {size}\n")


if __name__ == "__main__":
    app = DictionaryVisualizer()
    app.mainloop()
