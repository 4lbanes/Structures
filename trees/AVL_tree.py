import tkinter as tk
import time

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key
        self.height = 1

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
    
    def right_rotation(self, y, gui):
     x = y.left
     T2 = x.right
     gui.show_balance_message(f"Realizando rotação direita. X: {x.value}, Y: {y.value}, T2: {T2.value}")
     x.right = y
     y.left = T2
     self.update_height(y)
     self.update_height(x)
     gui.highlight_node(x.value, "green")
     gui.highlight_node(y.value, "red")
     gui.update()
     time.sleep(1)

     return x

    def left_rotation(self, x, gui):
     y = x.right
     T2 = y.left
     gui.show_balance_message(f"Realizando rotação esquerda. X: {x.value}, Y: {y.value}, T2: {T2.value}")
     y.left = x
     x.right = T2
     self.update_height(x)
     self.update_height(y)
     gui.highlight_node(y.value, "green")
     gui.highlight_node(x.value, "red")
     gui.update()
     time.sleep(1)

     return y

    def balance(self, node, gui):
        bf = self.balance_factor(node)
        if bf > 1:
            if self.balance_factor(node.left) < 0:
                node.left = self.left_rotation(node.left, gui)
            node = self.right_rotation(node, gui)
        elif bf < -1:
            if self.balance_factor(node.right) > 0:
                node.right = self.right_rotation(node.right, gui)
            node = self.left_rotation(node, gui)
        return node

    def insert(self, key, gui=None):
        if self.search(key):
            if gui:
                gui.output_text.insert(tk.END, f"Nó com valor {key} já existe.\n")
                gui.output_text.see(tk.END)
            return
        if self.root is None:
            self.root = Node(key)
        else:
            self.root = self._insert(self.root, key, gui)

    def _insert(self, node, key, gui):
        if node is None:
            return Node(key)
        if gui:
            gui.highlight_node(node.value, "yellow") 
            gui.update()
            time.sleep(1)

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
        balanced_node = self.balance(node, gui)

        if gui and balanced_node != node:
            gui.highlight_node(node.value, "red")
            gui.update()
            time.sleep(1)

        return balanced_node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key == node.value:
            return True
        elif key < node.value:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

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

            temp = self.get_max_value_node(node.left)
            node.value = temp.value
            node.left = self._delete(node.left, temp.value, gui)

        self.update_height(node)
        balanced_node = self.balance(node, gui)

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

class AVLGUI(tk.Tk):
    def __init__(self, avl_tree):
        super().__init__()
        self.avl_tree = avl_tree
        self.title("Árvore AVL")

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
        self.horizontal_spacing = 100 
        self.vertical_spacing = 80 
        self.x_start = 400
        self.y_start = 50
        self.node_positions = {}
        self.current_lines = []
        self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_tree(self, node, x, y, level):
        if node:
            self.node_positions[node.value] = (x, y)
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))

            if node.left:
                new_x = x - self.horizontal_spacing
                new_y = y + self.vertical_spacing
                self.canvas.create_line(x, y, new_x, new_y, arrow=tk.LAST)
                self.draw_tree(node.left, new_x, new_y, level + 1)

            if node.right:
                new_x = x + self.horizontal_spacing
                new_y = y + self.vertical_spacing
                self.canvas.create_line(x, y, new_x, new_y, arrow=tk.LAST)
                self.draw_tree(node.right, new_x, new_y, level + 1)

    def highlight_node(self, value, color):
        if value in self.node_positions:
            x, y = self.node_positions[value]
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, outline=color, width=3)

    def show_balance_message(self, message):
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)

    def show_comparison(self, node_value, key_value, operator):
        self.output_text.insert(tk.END, f"{node_value} {operator} {key_value}\n")
        self.output_text.see(tk.END)

    def update(self):
        self.canvas.update()

    def insert_node(self):
        key = int(self.insert_entry.get())
        self.avl_tree.insert(key, self)
        self.canvas.delete("all")
        self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)

    def remove_node(self):
        key = int(self.remove_entry.get())
        self.avl_tree.delete(key, self)
        self.canvas.delete("all")
        self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)

    def invert_tree(self):
        self.avl_tree.invert()
        self.canvas.delete("all")
        self.draw_tree(self.avl_tree.root, self.x_start, self.y_start, 1)

    def show_inorder(self):
        result = self.avl_tree.inorder()
        self.output_text.insert(tk.END, f"In-order: {result}\n")
        self.output_text.see(tk.END)

    def show_preorder(self):
        result = self.avl_tree.preorder()
        self.output_text.insert(tk.END, f"Pre-order: {result}\n")
        self.output_text.see(tk.END)

    def show_postorder(self):
        result = self.avl_tree.postorder()
        self.output_text.insert(tk.END, f"Post-order: {result}\n")
        self.output_text.see(tk.END)

avl_tree = AVLTree()
app = AVLGUI(avl_tree)
app.mainloop()
