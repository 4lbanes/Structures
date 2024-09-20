import tkinter as tk
import math

class Graph:
    def __init__(self):
        self.graph = {}
        self.weights = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2, weight=1):
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1].append(vertex2)
            self.weights[(vertex1, vertex2)] = weight

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.graph and vertex2 in self.graph and vertex2 in self.graph[vertex1]:
            self.graph[vertex1].remove(vertex2)
            del self.weights[(vertex1, vertex2)]

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            for v in self.graph:
                if vertex in self.graph[v]:
                    self.graph[v].remove(vertex)
                    del self.weights[(v, vertex)]
            del self.graph[vertex]

    def get_vertices(self):
        return list(self.graph.keys())

    def get_edges(self):
        edges = []
        for vertex, neighbors in self.graph.items():
            for neighbor in neighbors:
                edges.append((vertex, neighbor))
        return edges

    def dijkstra(self, start_vertex, end_vertex):
        distances = {vertex: float('infinity') for vertex in self.graph}
        previous_vertices = {vertex: None for vertex in self.graph}
        distances[start_vertex] = 0

        unvisited_vertices = set(self.graph.keys())

        while unvisited_vertices:
            current_vertex = min(unvisited_vertices, key=lambda vertex: distances[vertex])
            unvisited_vertices.remove(current_vertex)

            if distances[current_vertex] == float('infinity'):
                break

            for neighbor in self.graph[current_vertex]:
                weight = self.weights.get((current_vertex, neighbor), 1)
                distance = distances[current_vertex] + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex

        path = []
        current_vertex = end_vertex

        while current_vertex is not None:
            path.append(current_vertex)
            current_vertex = previous_vertices[current_vertex]

        path = path[::-1]

        return path

class GraphGUI(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.title("Grafos:")

        # Create a main canvas for graph visualization
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vertices_pos = self.calculate_positions()
        self.start_vertex = None
        self.end_vertex = None
        self.drag_data = {"vertex": None, "x": 0, "y": 0}

        # Create side and bottom frames for organizing the buttons and entries
        self.create_widgets()

        # Bind mouse events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.on_vertex_press)
        self.canvas.bind("<B1-Motion>", self.on_vertex_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_vertex_release)

    def create_widgets(self):
        side_frame = tk.Frame(self)
        side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Inserir vértice
        tk.Label(side_frame, text="Inserir vértice:", font=("Arial", 10)).pack(pady=5)
        self.vertex_entry = tk.Entry(side_frame)
        self.vertex_entry.pack(pady=5)

        tk.Button(side_frame, text="Inserir", command=self.add_vertex).pack(pady=5)

        # Remover vértice
        tk.Label(side_frame, text="Remover vértice:", font=("Arial", 10)).pack(pady=5)
        self.remove_vertex_entry = tk.Entry(side_frame)
        self.remove_vertex_entry.pack(pady=5)

        tk.Button(side_frame, text="Remover", command=self.remove_vertex).pack(pady=5)

        # Área de arestas
        tk.Label(side_frame, text="Aresta sai do vértice:", font=("Arial", 10)).pack(pady=5)
        self.vertex1_entry = tk.Entry(side_frame)
        self.vertex1_entry.pack(pady=5)

        tk.Label(side_frame, text="Aresta vai para o vértice:", font=("Arial", 10)).pack(pady=5)
        self.vertex2_entry = tk.Entry(side_frame)
        self.vertex2_entry.pack(pady=5)

        tk.Label(side_frame, text="Peso da aresta:", font=("Arial", 10)).pack(pady=5)
        self.weight_entry = tk.Entry(side_frame)
        self.weight_entry.pack(pady=5)

        tk.Button(side_frame, text="Adicionar Aresta", command=self.add_edge).pack(pady=5)
        tk.Button(side_frame, text="Remover Aresta", command=self.remove_edge).pack(pady=5)

        # Dijkstra
        tk.Label(side_frame, text="Dijkstra - Vértice de início:", font=("Arial", 10)).pack(pady=5)
        self.start_entry = tk.Entry(side_frame)
        self.start_entry.pack(pady=5)

        tk.Label(side_frame, text="Dijkstra - Vértice de destino:", font=("Arial", 10)).pack(pady=5)
        self.end_entry = tk.Entry(side_frame)
        self.end_entry.pack(pady=5)

        tk.Button(side_frame, text="Encontrar menor caminho", command=self.find_shortest_path).pack(pady=10)

    def calculate_positions(self):
        vertices = self.graph.get_vertices()
        angle = 2 * math.pi / len(vertices) if vertices else 0
        radius = 250
        center = (300, 300)
        positions = {}
        for i, vertex in enumerate(vertices):
            x = center[0] + radius * math.cos(i * angle)
            y = center[1] + radius * math.sin(i * angle)
            positions[vertex] = (x, y)
        return positions

    def draw_graph(self):
        self.canvas.delete("all")
        edges = self.graph.get_edges()

        for vertex1, vertex2 in edges:
            x1, y1 = self.vertices_pos[vertex1]
            x2, y2 = self.vertices_pos[vertex2]

            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx**2 + dy**2)
            norm_dx = dx / dist
            norm_dy = dy / dist
            offset = 20

            arrow_x = x2 - norm_dx * offset
            arrow_y = y2 - norm_dy * offset

            self.canvas.create_line(x1, y1, arrow_x, arrow_y, fill="black", width=2, arrow=tk.LAST)
            weight = self.graph.weights.get((vertex1, vertex2), 1)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(weight), fill="black")

        for vertex, (x, y) in self.vertices_pos.items():
            fill_color = "lightblue" if len(self.graph.graph[vertex]) <= 2 else "lightgreen"
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=fill_color, outline="black")
            self.canvas.create_text(x, y, text=vertex)

        if self.start_vertex and self.end_vertex:
            self.draw_shortest_way(self.start_vertex, self.end_vertex)

    def draw_shortest_way(self, start_vertex, end_vertex):
        path = self.graph.dijkstra(start_vertex, end_vertex)

        if path[0] == start_vertex:
            for i in range(len(path) - 1):
                x1, y1 = self.vertices_pos[path[i]]
                x2, y2 = self.vertices_pos[path[i+1]]

                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    def add_vertex(self):
        vertex = self.vertex_entry.get().strip()
        if vertex:
            self.graph.add_vertex(vertex)
            self.vertex_entry.delete(0, tk.END)
            self.vertices_pos = self.calculate_positions()
            self.draw_graph()

    def add_edge(self):
        vertex1 = self.vertex1_entry.get().strip()
        vertex2 = self.vertex2_entry.get().strip()
        weight = self.weight_entry.get().strip()
        if vertex1 and vertex2:
            self.graph.add_edge(vertex1, vertex2, int(weight) if weight else 1)
            self.vertex1_entry.delete(0, tk.END)
            self.vertex2_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
            self.draw_graph()

    def remove_vertex(self):
        vertex = self.remove_vertex_entry.get().strip()
        if vertex:
            self.graph.remove_vertex(vertex)
            self.remove_vertex_entry.delete(0, tk.END)
            self.vertices_pos = self.calculate_positions()
            self.draw_graph()

    def remove_edge(self):
        vertex1 = self.vertex1_entry.get().strip()
        vertex2 = self.vertex2_entry.get().strip()
        if vertex1 and vertex2:
            self.graph.remove_edge(vertex1, vertex2)
            self.vertex1_entry.delete(0, tk.END)
            self.vertex2_entry.delete(0, tk.END)
            self.draw_graph()

    def find_shortest_path(self):
        start_vertex = self.start_entry.get().strip()
        end_vertex = self.end_entry.get().strip()
        if start_vertex and end_vertex:
            self.start_vertex = start_vertex
            self.end_vertex = end_vertex
            self.draw_graph()

    def on_vertex_press(self, event):
        # Check if the mouse click is inside a vertex
        for vertex, (x, y) in self.vertices_pos.items():
            if (x-20) <= event.x <= (x+20) and (y-20) <= event.y <= (y+20):
                self.drag_data["vertex"] = vertex
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                break

    def on_vertex_motion(self, event):
        # Update the position of the dragged vertex
        vertex = self.drag_data["vertex"]
        if vertex:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            x, y = self.vertices_pos[vertex]
            self.vertices_pos[vertex] = (x + dx, y + dy)

            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            self.draw_graph()

    def on_vertex_release(self, event):
        # Reset the drag data when the mouse is released
        self.drag_data["vertex"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0


if __name__ == "__main__":
    graph = Graph()
    app = GraphGUI(graph)
    app.mainloop()

