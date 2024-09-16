import tkinter as tk
import math
import time

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
        self.title("Graph Visualization with Direction and Dijkstra")
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.vertices_pos = self.calculate_positions()
        self.selected_vertex = None
        self.start_vertex = None
        self.end_vertex = None
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_graph()

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

    def on_click(self, event):
     clicked_vertex = self.get_clicked_vertex(event.x, event.y)
     if clicked_vertex:
        # Caso o nó clicado seja o start_vertex ou end_vertex, resetar ambos
        if clicked_vertex == self.start_vertex or clicked_vertex == self.end_vertex:
            self.start_vertex = None
            self.end_vertex = None
        else:
            # Se o start_vertex e o end_vertex ainda não foram definidos
            if not self.start_vertex:
                self.start_vertex = clicked_vertex
            elif not self.end_vertex:
                self.end_vertex = clicked_vertex
            else:
                # Caso ambos já estejam definidos, resetar e definir o novo start_vertex
                self.start_vertex = clicked_vertex
                self.end_vertex = None

        # Se o start_vertex ou o end_vertex forem apagados, recalcula o caminho
        if self.start_vertex and self.end_vertex:
            self.draw_graph()
        else:
            # Anima a remoção e remove o nó clicado
            self.animate_removal(clicked_vertex)
            self.graph.remove_vertex(clicked_vertex)
            self.vertices_pos = self.calculate_positions()
            self.draw_graph()


    def get_clicked_vertex(self, x, y):
        for vertex, (vx, vy) in self.vertices_pos.items():
            if (vx - 20) < x < (vx + 20) and (vy - 20) < y < (vy + 20):
                return vertex
        return None

    def animate_removal(self, vertex):
        for i in range(5):
            self.canvas.delete("all")
            edges = self.graph.get_edges()
            for vertex1, vertex2 in edges:
                x1, y1 = self.vertices_pos[vertex1]
                x2, y2 = self.vertices_pos[vertex2]
                self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

            for v, (x, y) in self.vertices_pos.items():
                size = 20 - i*4 if v == vertex else 20
                self.canvas.create_oval(x-size, y-size, x+size, y+size, fill="lightblue", outline="black")
                self.canvas.create_text(x, y, text=v)
            self.update()
            time.sleep(0.1)  

# Exemplo de uso
g = Graph()
g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')
g.add_vertex('D')
g.add_vertex('E')
g.add_vertex('F')


g.add_edge('A', 'B', 2)
g.add_edge('B', 'A', 2) 
g.add_edge('C', 'B', 1)
g.add_edge('A', 'C', 3)
g.add_edge('D', 'A', 1)
g.add_edge('A', 'D', 1)
g.add_edge('E', 'C', 12)
g.add_edge('E', 'B', 30)
g.add_edge('C', 'D', 0)
g.add_edge('D','F', 0)

app = GraphGUI(g)
app.start_vertex = 'E' 
app.end_vertex = 'F'   
app.draw_graph()        
app.mainloop()
