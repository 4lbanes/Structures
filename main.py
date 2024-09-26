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

        # Botões para cada tipo de estrutura de dados
        buttons = [
            ("Filas", self.open_queue_menu),
            ("Pilhas", self.open_stack_menu),
            ("Listas Encadeadas", self.open_linked_list_menu),
            ("Tabelas Hash", self.open_hash_table_menu),
            ("Grafos", self.open_graph_menu),
            ("Deque", self.open_deque_menu),
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
            button = tk.Button(new_win, text=text, width=20, command=lambda cmd=command, w=new_win: self.open_structure(lambda: cmd(), w))
            button.pack(pady=5)

        # Botão de voltar para a tela principal
        back_button = tk.Button(new_win, text="Voltar", width=20, command=new_win.destroy)
        back_button.pack(pady=10)

    def open_structure(self, command, window):
        window.destroy()  # Fecha a janela de menu após escolher a estrutura
        command()  # Abre a janela da estrutura selecionada

    # Funções de abertura das GUIs para estruturas de dados com o caminho completo
    def open_static_queue(self):
        root = tk.Toplevel(self.root)
        queues.static_queue.StaticQueueGUI(root, 5)  # Caminho correto para StaticQueueGUI

    def open_dynamic_queue(self):
        root = tk.Toplevel(self.root)
        queues.dynamic_queue.DynamicQueueGUI(root, 5)  # Caminho correto para DynamicQueueGUI

    def open_priority_queue(self):
        root = tk.Toplevel(self.root)
        queues.priority_queue.PriorityQueueGUI(root)  # Caminho correto para PriorityQueueGUI

    def open_circular_static_queue(self):
        root = tk.Toplevel(self.root)
        circular_queues.circular_static_queue.CircularQueueGUI(root)  # Caminho correto para CircularQueueGUI (estática)

    def open_circular_dynamic_queue(self):
        root = tk.Toplevel(self.root)
        circular_queues.circular_linked_queue.CircularQueueGUI(root)  # Caminho correto para CircularQueueGUI (dinâmica)

    def open_static_stack(self):
        root = tk.Toplevel(self.root)
        stacks.static_stack.StaticStackGUI(root, 5)  # Caminho correto para StaticStackGUI

    def open_dynamic_stack(self):
        root = tk.Toplevel(self.root)
        stacks.dynamic_stack.DynamicStackGUI(root)  # Caminho correto para DynamicStackGUI

    def open_linked_list(self):
        root = tk.Toplevel(self.root)
        lists.linked_list.LinkedListGUI(root, 10)  # Caminho correto para LinkedListGUI

    def open_doubly_linked_list(self):
        root = tk.Toplevel(self.root)
        lists.doubly_linked_list.DoublyLinkedListGUI(root, 10)  # Caminho correto para DoublyLinkedListGUI

    def open_hash_table_menu(self):
        root = tk.Toplevel(self.root)
        hash_table.hash_table.HashTableGUI(root)  # Caminho correto para HashTableGUI

    def open_graph_menu(self):
        root = tk.Toplevel(self.root)
        graphs.graph.GraphGUI(graphs.graph.Graph())  # Caminho correto para GraphGUI
      
    def open_deque_menu(self):
        root = tk.Toplevel(self.root)
        deque.static_deque.DequeGUI(root)

    def open_min_heap_menu(self):
        root = tk.Toplevel(self.root)
        heap.min_heap.MinHeapGUI()  # Caminho correto para MinHeapGUI

    def open_avl_tree(self):
        avl_tree = trees.AVL_tree.AVLTree()  # Caminho correto para AVLTree
        trees.AVL_tree.AVLGUI(avl_tree)  # Caminho correto para AVLGUI

    def open_bst(self):
        bst = trees.binary_search_tree.BinarySearchTree()  # Caminho correto para BinarySearchTree
        trees.binary_search_tree.BSTGUI(bst)  # Caminho correto para BSTGUI

# Execução da aplicação principal
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
