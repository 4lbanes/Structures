import tkinter as tk
import time

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

    def insert(self, key, gui=None):
        if self.root is None:
            self.root = Node(key)
        else:
            self.root = self._insert(self.root, key, gui)

    def _insert(self, node, key, gui):
     if node is None:
        return Node(key)
    
     # Destacar o nó atual e mostrar comparação, se a GUI estiver ativada
     if gui:
        gui.highlight_node(node.value, "yellow")  # Destaca o nó atual
        gui.update()
        time.sleep(1)  # Pausa para o usuário ver a comparação

        # Exibe comparação entre o valor atual e o valor inserido
        if key < node.value:
            gui.show_comparison(node.value, key, ">")
            time.sleep(1)
        elif key > node.value:
            gui.show_comparison(node.value, key, "<")
            time.sleep(1)
        else:
            gui.show_comparison(node.value, key, "=")
            time.sleep(1)
            # Exibe mensagem de valor duplicado
            gui.output_text.insert(tk.END, "Valor duplicado não pode ser inserido!\n")
            return node

     if key < node.value:
        node.left = self._insert(node.left, key, gui)
     elif key > node.value:
        node.right = self._insert(node.right, key, gui)

     return node

    def delete(self, key, gui=None):
        if self.is_empty():
            print("A árvore está vazia!")
            return
        self.root = self._delete(self.root, key, gui)
        
    def _delete(self, node, key, gui):
        if node is None:
            return node

        if gui:
            # Destaca o nó atual e exibe comparação
            gui.highlight_node(node.value, "yellow")
            gui.update()
            time.sleep(1)

            # Exibe comparação entre o valor atual e o valor a ser removido
            if key < node.value:
                gui.show_comparison(node.value, key, ">")
                time.sleep(1)
            elif key > node.value:
                gui.show_comparison(node.value, key, "<")
                time.sleep(1)
            else:
                gui.show_comparison(node.value, key, "=")
                time.sleep(1)

        if key < node.value:
            node.left = self._delete(node.left, key, gui)
        elif key > node.value:
            node.right = self._delete(node.right, key, gui)
        else:
            # Caso o nó a ser removido tenha dois filhos
            if node.left is not None and node.right is not None:
                # Encontrar o maior nó na subárvore esquerda (substituto)
                max_smaller_node = self._get_max(node.left)
                
                if gui:
                    # Destacar o nó substituto em vermelho
                    gui.highlight_node(max_smaller_node.value, "red")
                    gui.update()
                    time.sleep(1)
                
                # Substituir o valor do nó removido pelo valor do substituto
                node.value = max_smaller_node.value
                
                # Remover o nó substituto da subárvore esquerda
                node.left = self._delete(node.left, max_smaller_node.value, gui)

            # Caso o nó tenha apenas um filho ou nenhum
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left

        return node

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
        self.title("Árvore Binária de Busca: ")
        
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.insert_label = tk.Label(self.left_frame, text="Inserir elemento:")
        self.insert_label.pack()
        self.insert_entry = tk.Entry(self.left_frame)
        self.insert_entry.pack()
        self.insert_button = tk.Button(self.left_frame, text="Inserir", command=self.insert_node, bg="lightblue", fg="black")
        self.insert_button.pack()
        
        self.remove_label = tk.Label(self.left_frame, text="Remover elemento:")
        self.remove_label.pack()
        self.remove_entry = tk.Entry(self.left_frame)
        self.remove_entry.pack()
        self.remove_button = tk.Button(self.left_frame, text="Remover", command=self.remove_node, bg="lightblue", fg="black")
        self.remove_button.pack()

        self.invert_button = tk.Button(self.left_frame, text="Inverter Árvore", command=self.invert_tree, bg="lightblue", fg="black")
        self.invert_button.pack()

        self.inorder_button = tk.Button(self.left_frame, text="In-order", command=self.show_inorder, bg="lightblue", fg="black")
        self.inorder_button.pack()
        
        self.preorder_button = tk.Button(self.left_frame, text="Pre-order", command=self.show_preorder, bg="lightblue", fg="black")
        self.preorder_button.pack()
        
        self.postorder_button = tk.Button(self.left_frame, text="Post-order", command=self.show_postorder, bg="lightblue", fg="black")
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
            # Aumenta o espaçamento horizontal e vertical
            level_spacing = (self.horizontal_spacing / level) * 4  # Aumenta a margem horizontal
            vertical_spacing = self.vertical_spacing * 1.2  # Aumenta a margem vertical
            
            self.node_positions[node.value] = (x, y)
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                     x + self.node_radius, y + self.node_radius,
                                     fill='lightblue', outline='black')
            self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12))
            
            if node.left:
                # Desenha a linha e o nó da subárvore esquerda
                self.canvas.create_line(x, y + self.node_radius, 
                                        x - level_spacing, y + vertical_spacing - self.node_radius)
                self._draw_tree(node.left, x - level_spacing, y + vertical_spacing, level + 1)
                
            if node.right:
                # Desenha a linha e o nó da subárvore direita
                self.canvas.create_line(x, y + self.node_radius, 
                                        x + level_spacing, y + vertical_spacing - self.node_radius)
                self._draw_tree(node.right, x + level_spacing, y + vertical_spacing, level + 1)



    def on_click(self, event):
        clicked_value = self.get_clicked_node(event.x, event.y)
        if clicked_value:
            print(f"Nó clicado: {clicked_value}")
            self.bst.delete(clicked_value)
            self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
            self.update_button_visibility()

    def get_clicked_node(self, x, y):
        for value, (vx, vy) in self.node_positions.items():
            if (vx - self.node_radius <= x <= vx + self.node_radius) and (vy - self.node_radius <= y <= vy + self.node_radius):
                return value
        return None

    def insert_node(self):
        try:
            value = int(self.insert_entry.get())
            self.bst.insert(value, self)
            self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
            self.update_button_visibility()
        except ValueError:
            pass

    def remove_node(self):
        try:
            value = int(self.remove_entry.get())
            self.bst.delete(value, self)
            self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
            self.update_button_visibility()
        except ValueError:
            pass

    def invert_tree(self):
        self.bst.invert()
        self.draw_tree(self.bst.root, self.x_start, self.y_start, 1)
        
    def show_inorder(self):
        self.output_text.delete(1.0, tk.END)
        traversal = self.bst.inorder()
        self.output_text.insert(tk.END, "In-order: " + str(traversal) + "\n")
        
    def show_preorder(self):
        self.output_text.delete(1.0, tk.END)
        traversal = self.bst.preorder()
        self.output_text.insert(tk.END, "Pre-order: " + str(traversal) + "\n")
        
    def show_postorder(self):
        self.output_text.delete(1.0, tk.END)
        traversal = self.bst.postorder()
        self.output_text.insert(tk.END, "Post-order: " + str(traversal) + "\n")

    def highlight_node(self, value, color):
        if value in self.node_positions:
            x, y = self.node_positions[value]
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    fill=color, outline='black')
            self.canvas.create_text(x, y, text=str(value), font=("Arial", 12))

    def show_comparison(self, node_value, value, comparison):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"{node_value} {comparison} {value}\n")

    def update_button_visibility(self):
        if self.bst.is_empty():
            self.invert_button.pack_forget()
            self.remove_button.pack_forget()
            self.postorder_button.pack_forget()
            self.inorder_button.pack_forget()
            self.preorder_button.pack_forget()
        else:
            self.invert_button.pack()
            self.remove_button.pack()
            self.postorder_button.pack()
            self.inorder_button.pack()
            self.preorder_button.pack()

if __name__ == "__main__":
    bst = BinarySearchTree()
    gui = BSTGUI(bst)
    gui.mainloop()