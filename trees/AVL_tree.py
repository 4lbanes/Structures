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
        # Caso 1: Nó com apenas um filho ou nenhum
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        
        # Caso 2: Nó com dois filhos
        # Substituir o nó atual pelo maior valor da subárvore esquerda (predecessor in-order)
        temp = self.get_max_value_node(node.left)  # Encontra o maior valor na subárvore esquerda
        node.value = temp.value  # Substitui o valor do nó atual pelo do predecessor
        node.left = self._delete(node.left, temp.value, gui)  # Remove o predecessor da subárvore esquerda

     # Atualizar a altura e balancear o nó
     self.update_height(node)
     balanced_node = self.balance(node)

     if gui and balanced_node != node:
        gui.highlight_node(node.value, "red")
        gui.update()
        time.sleep(1)

     return balanced_node
 
    def get_max_value_node(self, node):
     current = node
     while current.right is not None:
        current = current.right
     return current

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
        self.title("Árvore AVL: ")

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
                                    fill='lightblue', outline='black', width=3)  # Fundo azul claro

            # Texto do nó
            self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 16, "bold"))

            # Margens para o desenho
            margin_x = 20  # Margem horizontal
            margin_y = 40  # Margem vertical

            if node.left:
                self.canvas.create_line(x, y + self.node_radius, x - (self.horizontal_spacing / level) - margin_x,
                                        y + self.vertical_spacing - self.node_radius)
                self._draw_tree(node.left, x - (self.horizontal_spacing / level) - margin_x, y + self.vertical_spacing, level + 1)

            if node.right:
                self.canvas.create_line(x, y + self.node_radius, x + (self.horizontal_spacing / level) + margin_x,
                                        y + self.vertical_spacing - self.node_radius)
                self._draw_tree(node.right, x + (self.horizontal_spacing / level) + margin_x, y + self.vertical_spacing, level + 1)

    def on_click(self, event):
        clicked_value = self.get_clicked_node_value(event.x, event.y)
        if clicked_value:
            self.output_text.insert(tk.END, f"Nó {clicked_value} clicado.\n")
            self.output_text.see(tk.END)

    def get_clicked_node_value(self, x, y):
        for node_value, (node_x, node_y) in self.node_positions.items():
            if (node_x - self.node_radius <= x <= node_x + self.node_radius) and (node_y - self.node_radius <= y <= node_y + self.node_radius):
                return node_value
        return None

    def insert_node(self):
        try:
            value = int(self.insert_entry.get())
            self.avl_tree.insert(value, gui=self)
            self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
            self.update_buttons_visibility()
        except ValueError:
            self.output_text.insert(tk.END, "Entrada inválida. Por favor, insira um número.\n")
            self.output_text.see(tk.END)

    def remove_node(self):
        try:
            value = int(self.remove_entry.get())
            self.avl_tree.delete(value, gui=self)
            self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
            self.update_buttons_visibility()
        except ValueError:
            self.output_text.insert(tk.END, "Entrada inválida. Por favor, insira um número.\n")
            self.output_text.see(tk.END)

    def highlight_node(self, value, color):
        if value in self.node_positions:
            x, y = self.node_positions[value]
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    fill=color)

    def show_comparison(self, node_value, inserted_value, comparison):
        self.output_text.insert(tk.END, f"{node_value} {comparison} {inserted_value}\n")
        self.output_text.see(tk.END)

    def show_inorder(self):
        inorder_list = self.avl_tree.inorder()
        self.output_text.insert(tk.END, f"In-order traversal: {inorder_list}\n")
        self.output_text.see(tk.END)

    def show_preorder(self):
        preorder_list = self.avl_tree.preorder()
        self.output_text.insert(tk.END, f"Pre-order traversal: {preorder_list}\n")
        self.output_text.see(tk.END)

    def show_postorder(self):
        postorder_list = self.avl_tree.postorder()
        self.output_text.insert(tk.END, f"Post-order traversal: {postorder_list}\n")
        self.output_text.see(tk.END)

    def invert_tree(self):
        self.avl_tree.invert()
        self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)

    def update_buttons_visibility(self):
        if self.avl_tree.is_empty():
            self.invert_button.pack_forget()
            self.remove_button.pack_forget()
        else:
            self.invert_button.pack()
            self.remove_button.pack()

# Main
if __name__ == "__main__":
    avl_tree = AVLTree()
    gui = AVLGUI(avl_tree)
    gui.mainloop()  

