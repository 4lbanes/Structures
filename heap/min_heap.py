import tkinter as tk
import math

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, key):
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            return None
        min_elem = self.heap[0]
        last_elem = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = last_elem
            self._heapify_down(0)
        return min_elem

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index

        if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest]:
            smallest = left_child_index

        if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest]:
            smallest = right_child_index

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

class MinHeapGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MinHeap Visualization")
        self.heap = MinHeap()
        
        # Frame para os controles à esquerda
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Labels e Entry para inserção de valores
        self.label = tk.Label(control_frame, text="Inserir Valor:")
        self.label.pack()
        
        self.entry = tk.Entry(control_frame)
        self.entry.pack()
        
        # Botão para inserir no heap
        self.insert_button = tk.Button(control_frame, text="Inserir", command=self.insert_value)
        self.insert_button.pack(pady=5)
        
        # Botão para extrair o mínimo
        self.extract_button = tk.Button(control_frame, text="Extrair Min", command=self.extract_min)
        self.extract_button.pack(pady=5)

        # Botão para printar o heap
        self.print_button = tk.Button(control_frame, text="Printar", command=self.print_heap)
        self.print_button.pack(pady=5)
        
        # Label para exibir o conteúdo do heap (vetor)
        self.heap_label = tk.Label(control_frame, text="Heap: []")
        self.heap_label.pack(pady=10)

        # Canvas para desenhar a árvore
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=20, pady=20)

        # Configuração dos parâmetros de desenho
        self.node_radius = 13
        self.horizontal_spacing = 120
        self.vertical_spacing = 60

    def insert_value(self):
        value = self.entry.get()
        if value.isdigit():
            self.heap.insert(int(value))
            self.entry.delete(0, tk.END)
            self.update_heap_label()
            self.animate_insert()

    def extract_min(self):
        if len(self.heap.heap) > 0:
            self.heap.extract_min()
            self.update_heap_label()
            self.animate_extract()

    def draw_heap(self):
        self.canvas.delete("all")
        if len(self.heap.heap) > 0:
            self._draw_nodes(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)))

    def _draw_nodes(self, index, x, y, levels):
        if index < len(self.heap.heap):
            # Desenha o nó
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(self.heap.heap[index]))

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            if left_child_index < len(self.heap.heap):
                x_left = x - self.horizontal_spacing / (2 ** (levels - 1))
                y_left = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_left, y_left - self.node_radius)
                self._draw_nodes(left_child_index, x_left, y_left, levels - 1)

            if right_child_index < len(self.heap.heap):
                x_right = x + self.horizontal_spacing / (2 ** (levels - 1))
                y_right = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_right, y_right - self.node_radius)
                self._draw_nodes(right_child_index, x_right, y_right, levels - 1)

    def animate_insert(self):
        self.canvas.delete("all")
        self._animate_nodes(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)), self.draw_heap)

    def animate_extract(self):
        self.canvas.delete("all")
        self._animate_nodes(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)), self.draw_heap)

    def _animate_nodes(self, index, x, y, levels, callback):
        if index < len(self.heap.heap):
            # Animação para desenhar o nó
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(self.heap.heap[index]))

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            if left_child_index < len(self.heap.heap):
                x_left = x - self.horizontal_spacing / (2 ** (levels - 1))
                y_left = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_left, y_left - self.node_radius)
                self.after(200, self._animate_nodes, left_child_index, x_left, y_left, levels - 1, callback)

            if right_child_index < len(self.heap.heap):
                x_right = x + self.horizontal_spacing / (2 ** (levels - 1))
                y_right = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_right, y_right - self.node_radius)
                self.after(200, self._animate_nodes, right_child_index, x_right, y_right, levels - 1, callback)

            if index == 0:
                self.after(500, callback)

    def print_heap(self):
        """Desenha o caminho da raiz até os nós da esquerda para a direita em todos os níveis com uma seta ao final."""
        self.canvas.delete("all")
        if len(self.heap.heap) > 0:
            self._draw_nodes(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)))
            self.draw_traversal_line()
            
    def draw_traversal_line(self):
        """Desenha a linha da esquerda para a direita passando por todos os nós."""
        self.canvas.delete("all")
        self.draw_heap()  # Primeiro desenha a árvore

        path_coords = []
        if len(self.heap.heap) > 0:
            # Coleta as coordenadas de todos os nós da esquerda para a direita
            self._collect_path_coords(0, 300, 50, path_coords)

            # Gradualmente desenha a linha, de um nó ao outro, da esquerda para a direita
            for i in range(len(path_coords) - 1):
                x1, y1 = path_coords[i]
                x2, y2 = path_coords[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
                self.update()  # Atualiza a tela para mostrar a linha gradualmente
                self.after(500)  # Aguarda 500ms antes de desenhar a próxima parte da linha

            # Desenha uma seta no final do caminho
            if path_coords:
                x_end, y_end = path_coords[-1]
                self.canvas.create_line(x_end, y_end, x_end - 10, y_end - 10, fill="red", width=2)
                self.canvas.create_line(x_end, y_end, x_end + 10, y_end - 10, fill="red", width=2)

    def _collect_path_coords(self, index, x, y, path_coords):
        """Coleta as coordenadas (x, y) de cada nó no heap em ordem da esquerda para a direita."""
        if index < len(self.heap.heap):
            path_coords.append((x, y))

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            # Primeiro coleta as coordenadas da subárvore da esquerda
            if left_child_index < len(self.heap.heap):
                x_left = x - self.horizontal_spacing / (2 ** (math.floor(math.log2(left_child_index + 1))))
                y_left = y + self.vertical_spacing
                self._collect_path_coords(left_child_index, x_left, y_left, path_coords)

            # Depois coleta as coordenadas da subárvore da direita
            if right_child_index < len(self.heap.heap):
                x_right = x + self.horizontal_spacing / (2 ** (math.floor(math.log2(right_child_index + 1))))
                y_right = y + self.vertical_spacing
                self._collect_path_coords(right_child_index, x_right, y_right, path_coords)


    

    def update_heap_label(self):
        self.heap_label.config(text=f"Heap: {self.heap.heap}")
        self.draw_heap()

app = MinHeapGUI()
app.mainloop()
