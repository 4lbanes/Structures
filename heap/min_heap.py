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
        self.node_radius = 20
        self.horizontal_spacing = 80
        self.vertical_spacing = 50

    def insert_value(self):
        value = self.entry.get()
        if value.isdigit():
            self.heap.insert(int(value))
            self.entry.delete(0, tk.END)
            self.update_heap_label()  # Atualiza o label com o conteúdo do heap
            self.draw_heap()

    def extract_min(self):
        self.heap.extract_min()
        self.update_heap_label()  # Atualiza o label com o conteúdo do heap
        self.draw_heap()

    def draw_heap(self):
        self.canvas.delete("all")
        if len(self.heap.heap) > 0:
            levels = math.floor(math.log2(len(self.heap.heap) + 1))
            self._draw_nodes(0, 300, 50, levels)  # Ajustei a posição inicial para centralizar

    def _draw_nodes(self, index, x, y, levels):
        if index < len(self.heap.heap):
            # Desenha o nó
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(self.heap.heap[index]))

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            if left_child_index < len(self.heap.heap):
                x_left = x - self.horizontal_spacing * (levels - 1)
                y_left = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_left, y_left - self.node_radius)
                self._draw_nodes(left_child_index, x_left, y_left, levels - 1)

            if right_child_index < len(self.heap.heap):
                x_right = x + self.horizontal_spacing * (levels - 1)
                y_right = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_right, y_right - self.node_radius)
                self._draw_nodes(right_child_index, x_right, y_right, levels - 1)

    def print_heap(self):
        """Desenha o caminho da raiz para os nós da esquerda para a direita em todos os níveis."""
        self.canvas.delete("all")  # Limpa o canvas antes de desenhar o caminho
        if len(self.heap.heap) > 0:
            self._draw_nodes(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)))
            self.draw_traversal_line()

    def draw_traversal_line(self):
        """Desenha a linha da raiz até os níveis inferiores da esquerda para a direita."""
        path_coords = []
        if len(self.heap.heap) > 0:
            self._collect_path_coords(0, 300, 50, path_coords)  # Coleta as coordenadas de cada nó

            for i in range(len(path_coords) - 1):
                x1, y1 = path_coords[i]
                x2, y2 = path_coords[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)  # Desenha a linha vermelha

    def _collect_path_coords(self, index, x, y, path_coords):
        """Coleta as coordenadas (x, y) de cada nó no heap para desenhar a linha."""
        if index < len(self.heap.heap):
            path_coords.append((x, y))  # Guarda as coordenadas do nó atual

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            if left_child_index < len(self.heap.heap):
                x_left = x - self.horizontal_spacing
                y_left = y + self.vertical_spacing
                self._collect_path_coords(left_child_index, x_left, y_left, path_coords)

            if right_child_index < len(self.heap.heap):
                x_right = x + self.horizontal_spacing
                y_right = y + self.vertical_spacing
                self._collect_path_coords(right_child_index, x_right, y_right, path_coords)

    def update_heap_label(self):
        """Atualiza o label para mostrar o conteúdo atual do heap."""
        self.heap_label.config(text=f"Heap: {self.heap.heap}")

if __name__ == "__main__":
    app = MinHeapGUI()
    app.mainloop()

