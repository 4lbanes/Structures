import tkinter as tk

# Classe que representa um nó da Árvore Binária de Busca
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key

# Classe que representa a Árvore Binária de Busca
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert(self.root, key)

    def _insert(self, root, key):
        if key < root.value:
            if root.left is None:
                root.left = Node(key)
            else:
                self._insert(root.left, key)
        else:
            if root.right is None:
                root.right = Node(key)
            else:
                self._insert(root.right, key)

    def delete(self, key):
        if self.is_empty():
            print("A árvore está vazia!")
            return
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if root is None:
            return root

        if key < root.value:
            root.left = self._delete(root.left, key)
        elif key > root.value:
            root.right = self._delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            max_smaller_node = self._get_max(root.left)
            root.value = max_smaller_node.value
            root.left = self._delete(root.left, max_smaller_node.value)

        return root

    def _get_max(self, node):
        current = node
        while current.right is not None:
            current = current.right
        return current

    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, root, result):
        if root:
            self._inorder(root.left, result)
            result.append(root.value)
            self._inorder(root.right, result)
        return result

    def preorder(self):
        return self._preorder(self.root, [])

    def _preorder(self, root, result):
        if root:
            result.append(root.value)
            self._preorder(root.left, result)
            self._preorder(root.right, result)
        return result

    def postorder(self):
        return self._postorder(self.root, [])

    def _postorder(self, root, result):
        if root:
            self._postorder(root.left, result)
            self._postorder(root.right, result)
            result.append(root.value)
        return result

    def invert(self):
        self._invert(self.root)

    def _invert(self, root):
        if root:
            root.left, root.right = root.right, root.left
            self._invert(root.left)
            self._invert(root.right)

# Classe que representa a Interface Gráfica
class BSTGUI(tk.Tk):
    def __init__(self, bst):
        super().__init__()
        self.bst = bst
        self.title("Visualização da Árvore Binária de Busca")
        
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.insert_label = tk.Label(self.left_frame, text="Inserir elemento:")
        self.insert_label.pack()
        self.insert_entry = tk.Entry(self.left_frame)
        self.insert_entry.pack()
        self.insert_button = tk.Button(self.left_frame, text="Inserir", command=self.insert_node)
        self.insert_button.pack()
        
        self.remove_label = tk.Label(self.left_frame, text="Remover elemento:")
        self.remove_label.pack()
        self.remove_entry = tk.Entry(self.left_frame)
        self.remove_entry.pack()
        self.remove_button = tk.Button(self.left_frame, text="Remover", command=self.remove_node)
        self.remove_button.pack()

        self.invert_button = tk.Button(self.left_frame, text="Inverter Árvore", command=self.invert_tree)
        self.invert_button.pack()

        self.inorder_button = tk.Button(self.left_frame, text="In-order", command=self.show_inorder)
        self.inorder_button.pack()
        
        self.preorder_button = tk.Button(self.left_frame, text="Pre-order", command=self.show_preorder)
        self.preorder_button.pack()
        
        self.postorder_button = tk.Button(self.left_frame, text="Post-order", command=self.show_postorder)
        self.postorder_button.pack()

        self.output_text = tk.Text(self.left_frame, height=10, width=30)
        self.output_text.pack()

        self.node_radius = 20
        self.horizontal_spacing = 50
        self.vertical_spacing = 50
        self.x_start = 400
        self.y_start = 50
        self.node_positions = {}
        self.current_lines = []  # Armazena as linhas da travessia para apagá-las depois
        self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
        self.canvas.bind("<Button-1>", self.on_click)

        self.update_button_visibility()  # Verificar visibilidade ao iniciar

    def draw_tree(self, node, x, y, level):
        self.canvas.delete("all")
        self.node_positions.clear()
        self._draw_tree(node, x, y, level)

    def _draw_tree(self, node, x, y, level):
        if node:
            self.node_positions[node.value] = (x, y)
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    fill='lightblue', outline='black')
            self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12))
            
            if node.left:
                self.canvas.create_line(x, y + self.node_radius, x - self.horizontal_spacing / level, y + self.vertical_spacing - self.node_radius)
                self._draw_tree(node.left, x - self.horizontal_spacing / level, y + self.vertical_spacing, level + 1)
                
            if node.right:
                self.canvas.create_line(x, y + self.node_radius, x + self.horizontal_spacing / level, y + self.vertical_spacing - self.node_radius)
                self._draw_tree(node.right, x + self.horizontal_spacing / level, y + self.vertical_spacing, level + 1)

    def on_click(self, event):
        clicked_value = self.get_clicked_node(event.x, event.y)
        if clicked_value:
            print(f"Nó clicado: {clicked_value}")
            self.bst.delete(clicked_value)
            self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
            self.update_button_visibility()

    def get_clicked_node(self, x, y):
        for value, (vx, vy) in self.node_positions.items():
            if (vx - self.node_radius) < x < (vx + self.node_radius) and (vy - self.node_radius) < y < (vy + self.node_radius):
                return value
        return None

    def insert_node(self):
        value = self.insert_entry.get()
        if value.isdigit():
            self.bst.insert(int(value))
            self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
            self.insert_entry.delete(0, tk.END)
            self.update_button_visibility()

    def remove_node(self):
        value = self.remove_entry.get()
        if value.isdigit():
            self.bst.delete(int(value))
            self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
            self.remove_entry.delete(0, tk.END)
            self.update_button_visibility()
    
    def update_button_visibility(self):
        if self.bst.is_empty():
            self.remove_button.pack_forget()
            self.invert_button.pack_forget()
            self.inorder_button.pack_forget()
            self.preorder_button.pack_forget()
            self.postorder_button.pack_forget()
        else:
            self.remove_button.pack()
            self.invert_button.pack()
            self.inorder_button.pack()
            self.preorder_button.pack()
            self.postorder_button.pack()

    def invert_tree(self):
        self.bst.invert()
        self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)

    def show_inorder(self):
        self.show_traversal(self.bst.inorder(), 'red')

    def show_preorder(self):
        self.show_traversal(self.bst.preorder(), 'blue')

    def show_postorder(self):
        self.show_traversal(self.bst.postorder(), 'green')

    def show_traversal(self, traversal, color):
        self.output_text.delete(1.0, tk.END)
        for step in traversal:
            self.output_text.insert(tk.END, f"{step}\n")
        self.clear_previous_lines()  
        self.animate_traversal(traversal, color)

    def clear_previous_lines(self):
        for line in self.current_lines:
            self.canvas.delete(line)
        self.current_lines.clear()

    def animate_traversal(self, traversal, color):
        for i in range(len(traversal) - 1):
            x1, y1 = self.node_positions[traversal[i]]
            x2, y2 = self.node_positions[traversal[i + 1]]
            line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, arrow=tk.LAST)
            self.current_lines.append(line)

if __name__ == "__main__":
    bst = BinarySearchTree()
    gui = BSTGUI(bst)
    gui.mainloop()
