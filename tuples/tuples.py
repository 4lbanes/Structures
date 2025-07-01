import tkinter as tk
import tkinter.font as tkFont
import time

class TupleVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Tuplas")
        self.tuple_data = ()  # Tupla principal que será manipulada

        # Layout: Frame à esquerda com botões e entradas
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Canvas para desenhar a visualização da tupla
        self.canvas = tk.Canvas(self, width=600, height=200, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # --- SEÇÃO: Inserção de elemento ---
        self.entry_label = tk.Label(self.left_frame, text="Adicionar elemento:")
        self.entry_label.pack()
        self.entry = tk.Entry(self.left_frame)
        self.entry.pack()
        self.add_button = tk.Button(self.left_frame, text="Adicionar", command=self.add_element, bg="lightblue")
        self.add_button.pack(pady=(0, 10))

        # --- SEÇÃO: Buscar índice ---
        self.index_label = tk.Label(self.left_frame, text="Buscar índice de:")
        self.index_label.pack()
        self.index_entry = tk.Entry(self.left_frame)
        self.index_entry.pack()
        self.index_button = tk.Button(self.left_frame, text="Buscar índice", command=self.find_index, bg="lightblue")
        self.index_button.pack(pady=(0, 10))

        # --- SEÇÃO: Buscar valor na tupla ---
        self.search_label = tk.Label(self.left_frame, text="Buscar valor:")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.left_frame)
        self.search_entry.pack()
        self.search_button = tk.Button(self.left_frame, text="Buscar valor (visual)", command=self.search_element, bg="lightblue")
        self.search_button.pack(pady=(0, 10))

        # --- SEÇÃO: Contar ocorrências ---
        self.count_button = tk.Button(self.left_frame, text="Contar elemento", command=self.count_element, bg="lightblue")
        self.count_button.pack(pady=(0, 10))

        # --- SEÇÃO: Mostrar tamanho da tupla ---
        self.size_button = tk.Button(self.left_frame, text="Tamanho da tupla", command=self.show_size, bg="lightblue")
        self.size_button.pack(pady=(0, 10))

        # --- SEÇÃO: Exibir tupla completa ---
        self.display_button = tk.Button(self.left_frame, text="Exibir Tupla", command=self.display_tuple, bg="lightblue")
        self.display_button.pack(pady=(0, 10))

        # --- Área de saída de texto ---
        self.output_text = tk.Text(self.left_frame, height=12, width=35, font=("Courier", 10))
        self.output_text.pack()

    def add_element(self):
        """Adiciona um elemento à tupla (como string ou inteiro)."""
        value = self.entry.get()
        if value.strip() == "":
            self.output_text.insert(tk.END, "Insira um valor válido.\n")
            return

        # Converter para inteiro se for um número
        if value.isdigit():
            value = int(value)

        self.tuple_data += (value,)  # Tuplas são imutáveis, por isso criamos uma nova
        self.entry.delete(0, tk.END)
        self.display_tuple()

    def display_tuple(self):
        """Exibe visualmente a tupla no canvas e também no texto."""
        self.canvas.delete("all")
        font = tkFont.Font(family="Arial", size=12)
        padding = 10
        x = 50
        y = 100

        for val in self.tuple_data:
            text = str(val)
            text_width = font.measure(text)
            box_width = text_width + padding * 2

            # Desenhar o retângulo e texto no canvas
            self.canvas.create_rectangle(x, y - 20, x + box_width, y + 20, fill="lightgreen")
            self.canvas.create_text(x + box_width // 2, y, text=text, font=font)
            x += box_width + 10

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Tupla atual: {self.tuple_data}\n")

    def find_index(self):
        """Encontra o índice da primeira ocorrência de um valor."""
        val = self.index_entry.get()
        if val.strip() == "":
            self.output_text.insert(tk.END, "Insira um valor para buscar o índice.\n")
            return

        if val.isdigit():
            val = int(val)

        try:
            idx = self.tuple_data.index(val)
            self.output_text.insert(tk.END, f"O valor '{val}' está no índice {idx}.\n")
        except ValueError:
            self.output_text.insert(tk.END, f"Valor '{val}' não encontrado na tupla.\n")

    def search_element(self):
        """Busca visual de um elemento na tupla."""
        val = self.search_entry.get()
        if val.strip() == "":
            self.output_text.insert(tk.END, "Insira um valor para busca visual.\n")
            return

        if val.isdigit():
            val = int(val)

        font = tkFont.Font(family="Arial", size=12)
        padding = 10
        x = 50
        y = 100

        for i, v in enumerate(self.tuple_data):
            text = str(v)
            text_width = font.measure(text)
            box_width = text_width + padding * 2

            # Destaque amarelo
            self.canvas.create_rectangle(x, y - 20, x + box_width, y + 20, fill="yellow")
            self.canvas.create_text(x + box_width // 2, y, text=text, font=font)
            self.update()
            time.sleep(0.4)

            if v == val:
                # Encontrado! Destacar em vermelho
                self.canvas.create_rectangle(x, y - 20, x + box_width, y + 20, fill="red")
                self.canvas.create_text(x + box_width // 2, y, text=text, font=font)
                self.output_text.insert(tk.END, f"Valor '{val}' encontrado na posição {i}.\n")
                return

            x += box_width + 10

        self.output_text.insert(tk.END, f"Valor '{val}' não encontrado.\n")

    def count_element(self):
        """Conta quantas vezes o valor aparece na tupla."""
        val = self.search_entry.get()
        if val.strip() == "":
            self.output_text.insert(tk.END, "Insira um valor para contar.\n")
            return

        if val.isdigit():
            val = int(val)

        count = self.tuple_data.count(val)
        self.output_text.insert(tk.END, f"O valor '{val}' aparece {count} vez(es).\n")

    def show_size(self):
        """Exibe o tamanho atual da tupla."""
        size = len(self.tuple_data)
        self.output_text.insert(tk.END, f"A tupla possui {size} elemento(s).\n")

# --- Execução principal ---
if __name__ == "__main__":
    app = TupleVisualizer()
    app.mainloop()
