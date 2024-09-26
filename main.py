
import tkinter as tk
from tkinter import ttk

# Definição fictícia das classes das GUIs para estruturas de dados
class CircularQueueGUI:
    def __init__(self, root): pass

class DequeGUI:
    def __init__(self, root): pass

class GraphGUI:
    def __init__(self, graph): pass

class HashTableGUI:
    def __init__(self, root): pass

class MinHeapGUI:
    def __init__(self): pass

class DoublyLinkedListGUI:
    def __init__(self, root, size): pass

class LinkedListGUI:
    def __init__(self, root, size): pass

class DynamicQueueGUI:
    def __init__(self, root, size): pass

class PriorityQueueGUI:
    def __init__(self, root): pass

class StaticQueueGUI:
    def __init__(self, root, size): pass

class DynamicStackGUI:
    def __init__(self, root): pass

class StaticStackGUI:
    def __init__(self, root, size): pass

class AVLTree: pass
class AVLGUI:
    def __init__(self, avl_tree): pass

class BinarySearchTree: pass
class BSTGUI:
    def __init__(self, bst): pass

class Graph:
    def __init__(self): pass


# Tela principal do visualizador
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Estruturas de Dados")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="Escolha uma Estrutura de Dados", font=("Arial", 16))
        label.pack(pady=10)

        # Botões para cada tipo de estrutura de dados
        buttons = [
            ("Filas", self.open_queue_menu),
            ("Pilhas", self.open_stack_menu),
            ("Listas Encadeadas", self.open_linked_list_menu),
            ("Tabelas Hash", self.open_hash_table_menu),
            ("Grafos", self.open_graph_menu),
            ("Árvores", self.open_tree_menu),
            ("MinHeap", self.open_min_heap_menu)
        ]

        for (text, command) in buttons:
            button = tk.Button(self.root, text=text, width=20, command=command)
            button.pack(pady=5)

    def open_queue_menu(self):
        self.new_menu("Fila", [
            ("Estática", self.open_static_queue),
            ("Dinâmica", self.open_dynamic_queue),
            ("Fila de Prioridade", self.open_priority_queue),
            ("Fila Circular Estática", self.open_circular_static_queue),
            ("Fila Circular Dinâmica", self.open_circular_dynamic_queue)
        ])

    def open_stack_menu(self):
        self.new_menu("Pilha", [
            ("Estática", self.open_static_stack),
            ("Dinâmica", self.open_dynamic_stack)
        ])

    def open_linked_list_menu(self):
        self.new_menu("Listas Encadeadas", [
            ("Simplesmente Encadeada", self.open_linked_list),
            ("Duplamente Encadeada", self.open_doubly_linked_list)
        ])

    def open_tree_menu(self):
        self.new_menu("Árvores", [
            ("AVL", self.open_avl_tree),
            ("Árvore Binária de Busca", self.open_bst)
        ])

    def new_menu(self, title, options):
        # Nova janela de menu de interação com o usuário
        new_win = tk.Toplevel(self.root)
        new_win.title(title)

        label = tk.Label(new_win, text=f"Escolha uma opção de {title.lower()}:", font=("Arial", 14))
        label.pack(pady=10)

        for (text, command) in options:
            button = tk.Button(new_win, text=text, width=20, command=lambda cmd=command, w=new_win: self.open_structure(cmd, w))
            button.pack(pady=5)

        # Botão de voltar para a tela principal
        back_button = tk.Button(new_win, text="Voltar", width=20, command=new_win.destroy)
        back_button.pack(pady=10)

    def open_structure(self, command, window):
        window.destroy()  # Fecha a janela de menu após escolher a estrutura
        command()  # Abre a janela da estrutura selecionada

    # Funções de abertura das GUIs para estruturas de dados
    def open_static_queue(self):
        root = tk.Toplevel(self.root)
        StaticQueueGUI(root, 5)  # Exemplo de inicialização

    def open_dynamic_queue(self):
        root = tk.Toplevel(self.root)
        DynamicQueueGUI(root, 5)

    def open_priority_queue(self):
        root = tk.Toplevel(self.root)
        PriorityQueueGUI(root)

    def open_circular_static_queue(self):
        root = tk.Toplevel(self.root)
        CircularQueueGUI(root)

    def open_circular_dynamic_queue(self):
        root = tk.Toplevel(self.root)
        CircularQueueGUI(root)

    def open_static_stack(self):
        root = tk.Toplevel(self.root)
        StaticStackGUI(root, 5)

    def open_dynamic_stack(self):
        root = tk.Toplevel(self.root)
        DynamicStackGUI(root)

    def open_linked_list(self):
        root = tk.Toplevel(self.root)
        LinkedListGUI(root, 10)

    def open_doubly_linked_list(self):
        root = tk.Toplevel(self.root)
        DoublyLinkedListGUI(root, 10)

    def open_hash_table_menu(self):
        root = tk.Toplevel(self.root)
        HashTableGUI(root)

    def open_graph_menu(self):
        root = tk.Toplevel(self.root)
        GraphGUI(Graph())

    def open_min_heap_menu(self):
        root = tk.Toplevel(self.root)
        MinHeapGUI()

    def open_avl_tree(self):
        avl_tree = AVLTree()
        AVLGUI(avl_tree)

    def open_bst(self):
        bst = BinarySearchTree()
        BSTGUI(bst)

# Execução da aplicação principal
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
