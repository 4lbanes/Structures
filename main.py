import circular_queues.circular_linked_queue, circular_queues.circular_static_queue
import deque.static_deque
import graphs.graph
import hash_table.hash_table
import heap.min_heap
import lists.doubly_linked_list, lists.linked_list
import queues.dynamic_queue, queues.priority_queue, queues.static_queue
import stacks.dynamic_stack, stacks.static_stack
import trees.AVL_tree, trees.binary_search_tree

import tkinter as tk
from tkinter import ttk

# Tela principal do visualizador
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Estruturas de Dados")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="Escolha uma Estrutura de Dados", font=("Arial", 16))
        label.pack(pady=10)

        # Frame principal para organizar os botões em duas colunas
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Botões para cada tipo de estrutura de dados, divididos em duas colunas
        buttons = [
            ("Filas", self.open_queue_menu),
            ("Pilhas", self.open_stack_menu),
            ("Listas", self.open_list_menu),
            ("Tabelas Hash", self.open_hash_table_menu),
            ("Grafos", self.open_graph_menu),
            ("Deque", self.open_deque_menu),
            ("Árvores", self.open_tree_menu),
            ("MinHeap", self.open_min_heap_menu)
        ]

        # Configurando os botões em duas colunas
        for i, (text, command) in enumerate(buttons):
            row = i // 2  # Dividindo a lista de botões em duas colunas
            column = i % 2
            button = tk.Button(button_frame, text=text, width=20, command=command, bg="lightblue", fg="black")
            button.grid(row=row, column=column, padx=10, pady=5)

    def open_queue_menu(self):
        self.new_menu("Fila", [
            ("Estática", lambda: queues.static_queue.StaticQueueGUI(tk.Toplevel(self.root), 5)),
            ("Dinâmica", lambda: queues.dynamic_queue.DynamicQueueGUI(tk.Toplevel(self.root), 5)),
            ("Fila de Prioridade", lambda: queues.priority_queue.PriorityQueueGUI(tk.Toplevel(self.root))),
            ("Fila Circular Estática", lambda: circular_queues.circular_static_queue.CircularQueueGUI(tk.Toplevel(self.root))),
            ("Fila Circular Dinâmica", lambda: circular_queues.circular_linked_queue.CircularQueueGUI(tk.Toplevel(self.root)))
        ])

    def open_stack_menu(self):
        self.new_menu("Pilha", [
            ("Estática", lambda: stacks.static_stack.StaticStackGUI(tk.Toplevel(self.root), 5)),
            ("Dinâmica", lambda: stacks.dynamic_stack.DynamicStackGUI(tk.Toplevel(self.root)))
        ])

    def open_list_menu(self):
        self.new_menu("Listas", [
            ("Simplesmente Encadeada", lambda: lists.linked_list.LinkedListGUI(tk.Toplevel(self.root), 10)),
            ("Duplamente Encadeada", lambda: lists.doubly_linked_list.DoublyLinkedListGUI(tk.Toplevel(self.root), 10))
        ])

    def open_tree_menu(self):
        self.new_menu("Árvores", [
            ("AVL", lambda: trees.AVL_tree.AVLGUI(tk.Toplevel(self.root), trees.AVL_tree.AVLTree())),
            ("Árvore Binária de Busca", lambda: trees.binary_search_tree.BSTGUI(tk.Toplevel(self.root), trees.binary_search_tree.BinarySearchTree()))
        ])

    def open_hash_table_menu(self):
        self.new_menu("Tabelas Hash", [
            ("Tabela Hash", lambda: hash_table.hash_table.HashTableGUI(tk.Toplevel(self.root)))
        ])

    def open_graph_menu(self):
        self.new_menu("Grafos", [
            ("Grafo", lambda: graphs.graph.GraphGUI(tk.Toplevel(self.root), graphs.graph.Graph()))
        ])

    def open_deque_menu(self):
        self.new_menu("Deque", [
            ("Deque Estático", lambda: deque.static_deque.DequeGUI(tk.Toplevel(self.root)))
        ])

    def open_min_heap_menu(self):
        self.new_menu("MinHeap", [
            ("MinHeap", lambda: heap.min_heap.MinHeapGUI(tk.Toplevel(self.root)))
        ])

    def new_menu(self, title, options):
        new_win = tk.Toplevel(self.root)
        new_win.title(title)

        label = tk.Label(new_win, text=f"Escolha uma opção de {title.lower()}:", font=("Arial", 14))
        label.pack(pady=10)

        for (text, command) in options:
            button = tk.Button(new_win, text=text, width=20, command=command, bg="lightblue", fg="black")
            button.pack(pady=5)

        back_button = tk.Button(new_win, text="Voltar", width=20, command=new_win.destroy, bg="lightblue", fg="black")
        back_button.pack(pady=10)


# Execução da aplicação principal
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
