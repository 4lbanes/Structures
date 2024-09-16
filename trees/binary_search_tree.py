import tkinter as tk
import math

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

    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, root, result):
        if root:
            self._inorder(root.left, result)
            result.append(root.value)
            self._inorder(root.right, result)
        return result

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
        # Caso em que o nó tem dois filhos
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        # Encontra o maior nó da subárvore esquerda (predecessor)
        max_smaller_node = self._get_max(root.left)
        
        # Copia o valor do predecessor para o nó atual
        root.value = max_smaller_node.value
        
        # Remove o predecessor da subárvore esquerda
        root.left = self._delete(root.left, max_smaller_node.value)
        
     return root
 
    def _get_max(self, node):
      current = node
      while current.right is not None:
        current = current.right
      return current


    def invert(self):
        self._invert(self.root)

    def _invert(self, root):
        if self.is_empty():
            print("A árvore está vazia!")
            return
        else:
         if root:
            root.left, root.right = root.right, root.left
            self._invert(root.left)
            self._invert(root.right)
            
    def contains(self, data):
        return self._contains(self.root, data)

    def _contains(self, root, data):
        while root is not None:
            if data < root.value:
                root = root.left
            elif data > root.value:
                root = root.right
            else:
                return True
        return False
    
    def height(self):
     return self._height(self.root)

    def _height(self, node):
     if node is None:
        return 0
     left_height = self._height(node.left)
     right_height = self._height(node.right)
     return max(left_height, right_height) + 1
 
    def get_level(self, data):
     return self._get_level(self.root, data, 0)

    def _get_level(self, node, data, level):
     if node is None:
        return "Valor não encontrado na árvore!"
    
     if node.value == data:
        return level
     elif data < node.value:
        return self._get_level(node.left, data, level + 1)
     else:
        return self._get_level(node.right, data, level + 1)

# Classe que representa a Interface Gráfica
class BSTGUI(tk.Tk):
    def __init__(self, bst):
        super().__init__()
        self.bst = bst
        self.title("Visualização da Árvore Binária de Busca")
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Adicionando o botão para inverter a árvore
        self.invert_button = tk.Button(self, text="Inverter Árvore", command=self.invert_tree)
        self.invert_button.pack()
        
        self.node_radius = 20
        self.horizontal_spacing = 50
        self.vertical_spacing = 50
        self.x_start = 400
        self.y_start = 50
        self.node_positions = {}
        self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
        self.canvas.bind("<Button-1>", self.on_click)

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

    def get_clicked_node(self, x, y):
        for value, (vx, vy) in self.node_positions.items():
            if (vx - self.node_radius) < x < (vx + self.node_radius) and (vy - self.node_radius) < y < (vy + self.node_radius):
                return value
        return None

    def invert_tree(self):
        self.bst.invert()
        self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)

# Caso de teste para o método contains
if __name__ == "__main__":
    bst = BinarySearchTree()
    elements = [50, 30, 70, 20, 40, 60, 80]

    for el in elements:
        bst.insert(el)
        
    app = BSTGUI(bst)
    app.mainloop()

    # Testes para o método contains
    print(bst.contains(50))   
    print(bst.contains(30))   
    print(bst.contains(80))   
    print(bst.contains(25)) 
    print(bst.contains(90)) 
    
    print(bst.get_level(30))
    print(bst.height())