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

        self.update_heap_label()  # Atualiza o estado inicial dos botões

    def insert_value(self):
        value = self.entry.get()
        if value.isdigit():
            value = int(value)
            self.heap.insert(value)
            self.entry.delete(0, tk.END)
            self.animate_insert()

    def extract_min(self):
        if len(self.heap.heap) > 0:
            min_value = self.heap.extract_min()
            self.animate_extract(min_value)

    def draw_heap(self, highlighted_nodes=None, highlight_color="yellow", swap_info=None):
        self.canvas.delete("all")
        if highlighted_nodes is None:
            highlighted_nodes = []
        if swap_info is None:
            swap_info = []
        if len(self.heap.heap) > 0:
            self._draw_nodes(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)), highlighted_nodes, highlight_color, swap_info)

    def _draw_nodes(self, index, x, y, levels, highlighted_nodes, highlight_color, swap_info):
        if index < len(self.heap.heap):
            # Cor de destaque para o nó
            color = highlight_color if index in highlighted_nodes else "lightblue"
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius, fill=color)
            self.canvas.create_text(x, y, text=str(self.heap.heap[index]))

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            if left_child_index < len(self.heap.heap):
                x_left = x - self.horizontal_spacing / (2 ** (levels - 1))
                y_left = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_left, y_left - self.node_radius)
                if (index, left_child_index) in swap_info:
                    self.canvas.create_line(x, y, x_left, y_left, fill="red", width=2)
                self._draw_nodes(left_child_index, x_left, y_left, levels - 1, highlighted_nodes, highlight_color, swap_info)

            if right_child_index < len(self.heap.heap):
                x_right = x + self.horizontal_spacing / (2 ** (levels - 1))
                y_right = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_right, y_right - self.node_radius)
                if (index, right_child_index) in swap_info:
                    self.canvas.create_line(x, y, x_right, y_right, fill="red", width=2)
                self._draw_nodes(right_child_index, x_right, y_right, levels - 1, highlighted_nodes, highlight_color, swap_info)

    def animate_insert(self):
        self.canvas.delete("all")
        self._animate_insert(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)), [])

    def _animate_insert(self, index, x, y, levels, highlighted_nodes):
        if index < len(self.heap.heap):
            highlighted_nodes.append(index)
            self.draw_heap(highlighted_nodes=highlighted_nodes)
            self.after(500, self._animate_insert, 2 * index + 1, x - self.horizontal_spacing / (2 ** (levels - 1)), y + self.vertical_spacing, levels - 1, highlighted_nodes)
            self.after(500, self._animate_insert, 2 * index + 2, x + self.horizontal_spacing / (2 ** (levels - 1)), y + self.vertical_spacing, levels - 1, highlighted_nodes)
            if index == len(self.heap.heap) - 1:
                self.after(1000, self.draw_heap)

    def animate_extract(self, min_value):
        self.canvas.delete("all")
        self._animate_extract(0, 300, 50, math.floor(math.log2(len(self.heap.heap) + 1)), min_value, [])

    def _animate_extract(self, index, x, y, levels, min_value, highlighted_nodes):
        if index < len(self.heap.heap):
            highlighted_nodes.append(index)
            self.draw_heap(highlighted_nodes=highlighted_nodes)
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            swap_info = []

            if left_child_index < len(self.heap.heap):
                swap_info.append((index, left_child_index))
            if right_child_index < len(self.heap.heap):
                swap_info.append((index, right_child_index))

            self._draw_nodes(index, x, y, levels, highlighted_nodes, "lightblue", swap_info)
            if len(swap_info) > 0:
                self.after(500, self.draw_heap, highlighted_nodes, "yellow", swap_info)
            if left_child_index < len(self.heap.heap):
                self.after(1000, self._animate_extract, left_child_index, x - self.horizontal_spacing / (2 ** (levels - 1)), y + self.vertical_spacing, levels - 1, min_value, highlighted_nodes)
            if right_child_index < len(self.heap.heap):
                self.after(1000, self._animate_extract, right_child_index, x + self.horizontal_spacing / (2 ** (levels - 1)), y + self.vertical_spacing, levels - 1, min_value, highlighted_nodes)

            if index == 0:
                self.after(2000, self.draw_heap, highlighted_nodes, "lightblue")

    def update_heap_label(self):
        self.heap_label.config(text=f"Heap: {self.heap.heap}")

    def print_heap(self):
        self.update_heap_label()
        self.draw_heap()

if __name__ == "__main__":
    app = MinHeapGUI()
    app.mainloop()
