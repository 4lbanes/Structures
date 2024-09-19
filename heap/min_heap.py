import tkinter as tk
import math
import time

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, key, gui=None):
        self.heap.append(key)
        if gui:
            gui.update_heap_label()
        self._heapify_up(len(self.heap) - 1, gui)

    def extract_min(self, gui=None):
        if len(self.heap) == 0:
            return None
        min_elem = self.heap[0]
        last_elem = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = last_elem
            if gui:
                gui.update_heap_label()
            self._heapify_down(0, gui)
        return min_elem

    def _heapify_up(self, index, gui=None):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            if gui:
                gui.show_comparison(self.heap[parent_index], self.heap[index], ">")
                gui.highlight_node(index, "red")
                gui.highlight_node(parent_index, "yellow")
                gui.update()
                time.sleep(1)

            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            if gui:
                gui.update_heap_label()
                gui.draw_heap()
            self._heapify_up(parent_index, gui)

    def _heapify_down(self, index, gui=None):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index

        if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest]:
            smallest = left_child_index

        if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest]:
            smallest = right_child_index

        if smallest != index:
            if gui:
                gui.show_comparison(self.heap[index], self.heap[smallest], "<")
                gui.highlight_node(index, "yellow")
                gui.highlight_node(smallest, "red")
                gui.update()
                time.sleep(1)

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            if gui:
                gui.update_heap_label()
                gui.draw_heap()
            self._heapify_down(smallest, gui)

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

        # Label para exibir comparações em tempo real
        self.comparison_label = tk.Label(control_frame, text="Comparação:")
        self.comparison_label.pack(pady=10)

        # Canvas para desenhar a árvore
        self.canvas = tk.Canvas(self, width=1000, height=600, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=20, pady=20)

        # Configuração dos parâmetros de desenho
        self.node_radius = 15
        self.vertical_spacing = 60
        
        # Dicionário para armazenar as posições dos nós
        self.node_positions = {}

        self.update_heap_label()  # Atualiza o estado inicial dos botões

    def insert_value(self):
        value = self.entry.get()
        if value.isdigit():
            value = int(value)
            self.heap.insert(value, self)
            self.entry.delete(0, tk.END)
            self.draw_heap()

    def extract_min(self):
        if len(self.heap.heap) > 0:
            min_value = self.heap.extract_min(self)
            self.draw_heap()

    def draw_heap(self, highlighted_nodes=None):
        self.canvas.delete("all")
        self.node_positions.clear()  # Limpa as posições antes de desenhar
        if highlighted_nodes is None:
            highlighted_nodes = []
        if len(self.heap.heap) > 0:
            depth = math.floor(math.log2(len(self.heap.heap) + 1))  # Calcula a profundidade da árvore
            self._draw_nodes(0, 500, 50, depth, highlighted_nodes)

    def _draw_nodes(self, index, x, y, levels, highlighted_nodes):
        if index < len(self.heap.heap):
            # Cor de destaque para o nó
            color = "yellow" if index in highlighted_nodes else "lightblue"
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius, fill=color)
            self.canvas.create_text(x, y, text=str(self.heap.heap[index]))
            
            # Armazena a posição do nó
            self.node_positions[index] = (x, y)

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            # Espaçamento dinâmico horizontal com base na profundidade da árvore e direção dos filhos
            horizontal_spacing = 300 / (2 ** (levels - 1))  # Aumenta o espaçamento

            if left_child_index < len(self.heap.heap):
                x_left = x - horizontal_spacing
                y_left = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_left, y_left - self.node_radius)
                self._draw_nodes(left_child_index, x_left, y_left, levels - 1, highlighted_nodes)

            if right_child_index < len(self.heap.heap):
                x_right = x + horizontal_spacing
                y_right = y + self.vertical_spacing
                self.canvas.create_line(x, y + self.node_radius, x_right, y_right - self.node_radius)
                self._draw_nodes(right_child_index, x_right, y_right, levels - 1, highlighted_nodes)

    def show_comparison(self, node_value, value, comparison):
        # Exibe comparações na interface
        self.comparison_label.config(text=f"Comparação: {node_value} {comparison} {value}")

    def highlight_node(self, index, color):
        if index < len(self.heap.heap):
            x, y = self.node_positions.get(index, (None, None))
            if x and y:
                self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                        x + self.node_radius, y + self.node_radius, fill=color)

    def update_heap_label(self):
        self.heap_label.config(text=f"Heap: {self.heap.heap}")

    def print_heap(self):
        self.update_heap_label()
        self.draw_heap()

if __name__ == "__main__":
    app = MinHeapGUI()
    app.mainloop()
