import tkinter as tk
import time

# Classe que representa um nó da árvore AVL
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key
        self.height = 1

# Classe que representa a Árvore AVL
class AVLTree:
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def right_rotation(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotation(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def balance(self, node):
        bf = self.balance_factor(node)
        if bf > 1:
            if self.balance_factor(node.left) < 0:
                node.left = self.left_rotation(node.left)
            node = self.right_rotation(node)
        elif bf < -1:
            if self.balance_factor(node.right) > 0:
                node.right = self.right_rotation(node.right)
            node = self.left_rotation(node)
        return node

    def insert(self, key, gui=None):
        if self.root is None:
            self.root = Node(key)
        else:
            self.root = self._insert(self.root, key, gui)

    def _insert(self, node, key, gui):
        if node is None:
            return Node(key)
        if gui:
            gui.highlight_node(node.value, "yellow")  # Destaca o nó atual
            gui.update()
            time.sleep(1)  # Pausa para o usuário ver a comparação

            # Exibe comparação entre o valor atual e o valor inserido
            if key < node.value:
                gui.show_comparison(node.value, key, ">")
                time.sleep(1)
            else:
                gui.show_comparison(node.value, key, "<")
                time.sleep(1)

        if key < node.value:
            node.left = self._insert(node.left, key, gui)
        else:
            node.right = self._insert(node.right, key, gui)

        self.update_height(node)
        balanced_node = self.balance(node)

        if gui and balanced_node != node:
            gui.highlight_node(node.value, "red")  # Destaca o nó antes da rotação
            gui.update()
            time.sleep(1)  # Pausa para o usuário ver a rotação
        
        return balanced_node
    
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
    
    def delete(self, key, gui=None):
        self.root = self._delete(self.root, key, gui)
        
    def _delete(self, node, key, gui):
        if node is None:
            return node

        if gui:
            gui.highlight_node(node.value, "yellow")
            gui.update()
            time.sleep(1)

        if key < node.value:
            node.left = self._delete(node.left, key, gui)
        elif key > node.value:
            node.right = self._delete(node.right, key, gui)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self.get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value, gui)

        self.update_height(node)
        balanced_node = self.balance(node)

        if gui and balanced_node != node:
            gui.highlight_node(node.value, "red")
            gui.update()
            time.sleep(1)

        return balanced_node

    def invert(self):
        self._invert(self.root)

    def _invert(self, root):
        if root:
            root.left, root.right = root.right, root.left
            self._invert(root.left)
            self._invert(root.right)

# Classe que representa a Interface Gráfica
class AVLGUI(tk.Tk):
    def __init__(self, avl_tree):
        super().__init__()
        self.avl_tree = avl_tree
        self.title("Visualização da Árvore AVL")

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
        self.current_lines = []
        self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
        self.canvas.bind("<Button-1>", self.on_click)

        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões no início

    def draw_tree(self, node, x, y, level):
        self.canvas.delete("all")
        self.node_positions.clear()
        self._draw_tree(node, x, y, level)

    def _draw_tree(self, node, x, y, level):
     if node:
        self.node_positions[node.value] = (x, y)

        # Cor sólida no fundo
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill='#ADD8E6', outline='black', width=3)  # Fundo azul claro

        # Texto do nó
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 16, "bold"))

        if node.left:
            self.canvas.create_line(x, y + self.node_radius, x - self.horizontal_spacing / level,
                                    y + self.vertical_spacing - self.node_radius)
            self._draw_tree(node.left, x - self.horizontal_spacing / level, y + self.vertical_spacing, level + 1)

        if node.right:
            self.canvas.create_line(x, y + self.node_radius, x + self.horizontal_spacing / level,
                                    y + self.vertical_spacing - self.node_radius)
            self._draw_tree(node.right, x + self.horizontal_spacing / level, y + self.vertical_spacing, level + 1)

            
    def on_click(self, event):
        clicked_value = self.get_clicked_node(event.x, event.y)
        if clicked_value:
            print(f"Nó clicado: {clicked_value}")
            self.avl_tree.delete(clicked_value)
            self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
            self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após a exclusão

    def get_clicked_node(self, x, y):
        for value, (vx, vy) in self.node_positions.items():
            if (vx - self.node_radius) < x < (vx + self.node_radius) and (vy - self.node_radius) < y < (vy + self.node_radius):
                return value
        return None
    
    def invert_tree(self):
        self.avl_tree.invert()
        self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após a inversão
        
    def insert_node(self):
        value = self.insert_entry.get()
        if value.isdigit():
            self.avl_tree.insert(int(value), gui=self)
            self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
            self.insert_entry.delete(0, tk.END)
            self.update_buttons_visibility()  # Atualiza os botões após a inserção
        
    def remove_node(self):
        value = self.remove_entry.get()
        if value.isdigit():
            self.avl_tree.delete(int(value), gui=self)
            self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
            self.remove_entry.delete(0, tk.END)
            self.update_buttons_visibility()  # Atualiza os botões após a remoção

    def show_inorder(self):
        self.show_traversal(self.avl_tree.inorder(), 'red')

    def show_preorder(self):
        self.show_traversal(self.avl_tree.preorder(), 'blue')

    def show_postorder(self):
        self.show_traversal(self.avl_tree.postorder(), 'green')

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
        
    def animate_insertion(self, node_value):
     if node_value in self.node_positions:
        x, y = self.node_positions[node_value]
        for i in range(10):  # Faz a animação em 10 passos
            self.canvas.delete("highlight")  # Remove qualquer destaque anterior
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    outline="green", width=4, tags="highlight")
            self.canvas.update()
            time.sleep(0.1)

    def animate_deletion(self, node_value):  
     if node_value in self.node_positions:
        x, y = self.node_positions[node_value]
        for i in range(10):
            self.canvas.delete("highlight")
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    outline="red", width=4, tags="highlight")
            self.canvas.update()
            time.sleep(0.1)
        # Remove o nó após a animação de exclusão
        self.canvas.delete("highlight")

    def animate_traversal(self, traversal, color):
     self.clear_previous_lines()
     for i in range(len(traversal)):
        x, y = self.node_positions[traversal[i]]
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                outline=color, width=4)
        self.canvas.update()
        time.sleep(0.5)  # Aumenta o tempo para a animação ser mais perceptível


    def highlight_node(self, value, color):
        if value in self.node_positions:
            x, y = self.node_positions[value]
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    fill='white', outline=color, width=4)

    def show_comparison(self, node_value, inserted_value, comparison):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"{node_value} {comparison} {inserted_value}\n")
    
    def update_buttons_visibility(self):
        if self.avl_tree.is_empty():
            self.remove_button.config(state=tk.DISABLED)
            self.invert_button.config(state=tk.DISABLED)
            self.inorder_button.config(state=tk.DISABLED)
            self.preorder_button.config(state=tk.DISABLED)
            self.postorder_button.config(state=tk.DISABLED)
        else:
            self.remove_button.config(state=tk.NORMAL)
            self.invert_button.config(state=tk.NORMAL)
            self.inorder_button.config(state=tk.NORMAL)
            self.preorder_button.config(state=tk.NORMAL)
            self.postorder_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    avl = AVLTree()
    gui = AVLGUI(avl)
    gui.mainloop()
