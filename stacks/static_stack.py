import tkinter as tk
from tkinter import messagebox
import time

# Classe que representa um nó da pilha
class Node:
    def __init__(self, data):
        self.data = data  # Dados armazenados no nó
        self.next = None  # Aponta para o próximo nó

# Classe que representa a pilha estática utilizando nós e ponteiros
class StaticStack:
    def __init__(self, max_size):
        """
        Inicializa a pilha estática.

        :param max_size: O tamanho máximo da pilha.
        """
        self.top = None  # O topo da pilha (apontador para o nó do topo)
        self.max_size = max_size  # Tamanho máximo da pilha
        self.size = 0  # Contador do número de elementos na pilha
    
    def push(self, item):
        """
        Adiciona um item ao topo da pilha.

        :param item: O item a ser adicionado à pilha.
        """
        if not self.is_full():  # Verifica se a pilha não está cheia
            try:
                item = float(item)  # Tenta converter para número
            except ValueError:
                pass  # Mantém como string se não for número

            new_node = Node(item)  # Cria um novo nó com o item
            new_node.next = self.top  # O próximo nó será o topo atual
            self.top = new_node  # O novo nó se torna o topo
            self.size += 1  # Incrementa o tamanho da pilha
            print(f"{item} foi adicionado à stack.")
        else:
            print("A stack está cheia.")  # Mensagem se a pilha estiver cheia

    def pop(self):
        """
        Remove e retorna o item do topo da pilha.

        :return: O item removido ou None se a pilha estiver vazia.
        """
        if not self.is_empty():  # Verifica se a pilha não está vazia
            removed_node = self.top  # Pega o nó do topo
            self.top = self.top.next  # Atualiza o topo para o próximo nó
            self.size -= 1  # Decrementa o tamanho da pilha
            print(f"{removed_node.data} foi removido da stack.")
            return removed_node.data
        else:
            print("A stack está vazia.")  # Mensagem se a pilha estiver vazia
            return None

    def is_empty(self):
        """
        Verifica se a pilha está vazia.

        :return: True se a pilha estiver vazia, caso contrário False.
        """
        return self.top is None  # Retorna True se o topo for None
    
    def is_full(self):
        """
        Verifica se a pilha atingiu o tamanho máximo.

        :return: True se a pilha estiver cheia, caso contrário False.
        """
        return self.size == self.max_size  # Verifica se o tamanho atingiu o limite

    def peek(self):
        """
        Retorna o item do topo da pilha sem removê-lo.

        :return: O item no topo ou None se a pilha estiver vazia.
        """
        if not self.is_empty():
            return self.top.data  # Retorna o dado no topo
        else:
            return None

    def get_stack(self):
        """
        Retorna todos os elementos da pilha em uma lista.

        :return: Uma lista com os elementos da pilha do topo à base.
        """
        current = self.top
        stack_items = []
        while current is not None:  # Percorre a pilha
            stack_items.append(current.data)  # Adiciona o dado do nó atual
            current = current.next  # Move para o próximo nó
        return stack_items[::-1]  # Retorna a pilha invertida (base no final)
    
    def sort_stack(self):
        """
        Ordena os elementos da pilha em ordem crescente.
        """
        if self.is_empty():  # Verifica se a pilha está vazia
            return

        # Extrai os elementos da pilha em uma lista
        stack_list = self.get_stack()

        # Converte números para comparação e mantém strings como estão
        def convert(item):
            try:
                return float(item)  # Converte para número se possível
            except ValueError:
                return item  # Mantém como string

        # Ordenar pelo valor numérico e colocar os menores no topo
        stack_list.sort(key=lambda x: convert(x))

        # Reconstrói a pilha ordenada
        self.top = None
        self.size = 0
        for item in stack_list[::-1]:  # Insere os elementos ordenados na pilha
            self.push(item)

# Classe da interface gráfica da pilha estática
class StaticStackGUI:
    def __init__(self, root, max_size):
        """
        Inicializa a interface gráfica da pilha estática.

        :param root: A janela principal do Tkinter.
        :param max_size: O tamanho máximo da pilha.
        """
        self.stack = StaticStack(max_size)  # Cria a pilha estática
        self.root = root
        self.root.title("Pilha Estática: ")

        self.root.geometry("800x600")  # Define o tamanho da janela

        self.canvas = tk.Canvas(root, bg="white")  # Canvas para desenhar a pilha
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da pilha: {self.stack.max_size}")
        self.label_max_size.pack(pady=10)  # Label que mostra o tamanho máximo

        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.pack(side=tk.LEFT, padx=10, pady=10)  # Label para entrada de elemento

        self.entry_data = tk.Entry(root)  # Campo de entrada para o elemento
        self.entry_data.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_push = tk.Button(root, text="Inserir na Pilha", command=self.push)  # Botão para inserir
        self.button_push.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_pop = tk.Button(root, text="Remover da Pilha", command=self.pop)  # Botão para remover
        self.button_pop.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_sort = tk.Button(root, text="Ordenar a Pilha", command=self.sort_stack)  # Botão para ordenar
        self.button_sort.pack(side=tk.LEFT, padx=10, pady=10)

        self.stack_items = []  # Lista para armazenar os itens da pilha
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def push(self):
        """
        Método chamado ao pressionar o botão de inserção.
        """
        data = self.entry_data.get()  # Obtém o dado do campo de entrada
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")  # Mensagem de erro se vazio
            return

        self.stack.push(data)  # Adiciona o dado à pilha
        self.update_stack_display()  # Atualiza a exibição da pilha
        self.entry_data.delete(0, tk.END)  # Limpa o campo de entrada
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def pop(self):
        """
        Método chamado ao pressionar o botão de remoção.
        """
        removed = self.stack.pop()  # Remove o item do topo da pilha
        if removed is not None:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")  # Mostra o elemento removido
            self.update_stack_display()  # Atualiza a exibição da pilha
        else:
            messagebox.showwarning("Aviso", "A pilha está vazia.")  # Mensagem de aviso se a pilha estiver vazia
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def sort_stack(self):
        """
        Método chamado ao pressionar o botão de ordenação.
        """
        if not self.stack.is_empty():  # Verifica se a pilha não está vazia
            self.stack.sort_stack()  # Ordena a pilha
            self.update_stack_display()  # Atualiza a exibição da pilha
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def update_stack_display(self):
        """
        Atualiza a exibição da pilha na interface gráfica.
        """
        self.canvas.delete("all")  # Limpa o canvas
        self.stack_items = []  # Limpa a lista de itens da pilha

        # Define a posição inicial do topo, centralizado
        canvas_width = self.canvas.winfo_width()  # Largura do canvas
        x_center = canvas_width // 2  # Centro do canvas
        y_top = 50  # Posição inicial do topo

        # Pega os itens da pilha do topo até a base
        stack_items = self.stack.get_stack()  # Obtém os itens da pilha

        # Vamos desenhar do último item ao primeiro (LIFO)
        for index, item in enumerate(reversed(stack_items)):  # Reverter para seguir a ordem LIFO
            y_position = y_top + index * 50  # Calcula a posição vertical

            item_str = str(item)  # Converte o item para string
            item_width = max(100, len(item_str) * 15)  # Define a largura do retângulo

            # Desenha o retângulo que representa o item da pilha
            square = self.canvas.create_rectangle(
                x_center - item_width // 2, y_position,
                x_center + item_width // 2, y_position + 40,
                fill="lightblue"
            )

            # Define o texto a ser exibido
            if index == 0:  
                text_str = f"Topo\n{item_str}"  # O primeiro item desenhado é o topo
            elif index == len(stack_items) - 1:
                text_str = f"Base\n{item_str}"  # O último item desenhado é a base
            else:
                text_str = item_str

            # Cria o texto no canvas
            text = self.canvas.create_text(x_center, y_position + 20, text=text_str, font=("Arial", 16))

            self.stack_items.append((square, text))  # Armazena a referência dos elementos

            # Animação de descida
            for step in range(10):  # Faz a animação de descida
                self.canvas.move(square, 0, 3)  # Move o retângulo para baixo
                self.canvas.move(text, 0, 3)  # Move o texto para baixo
                self.canvas.update()  # Atualiza o canvas
                time.sleep(0.02)  # Aguarda um pequeno intervalo

    def update_buttons_visibility(self):
        """
        Atualiza a visibilidade dos botões com base no estado da pilha.
        """
        if self.stack.is_empty():  # Se a pilha está vazia
            self.button_pop.pack_forget()  # Esconde o botão de remoção
            self.button_sort.pack_forget()  # Esconde o botão de ordenação
        else:
            self.button_pop.pack(side=tk.LEFT, padx=10, pady=10)  # Mostra o botão de remoção
            self.button_sort.pack(side=tk.LEFT, padx=10, pady=10)  # Mostra o botão de ordenação

        if self.stack.is_full():  # Se a pilha está cheia
            self.button_push.pack_forget()  # Esconde o botão de inserção
        else:
            self.button_push.pack(side=tk.LEFT, padx=10, pady=10)  # Mostra o botão de inserção

# Criação da interface
root = tk.Tk()  # Cria a janela principal
app = StaticStackGUI(root, 5)  # Inicializa a GUI com tamanho máximo da pilha de 5
root.mainloop()  # Inicia o loop principal da interface gráfica
