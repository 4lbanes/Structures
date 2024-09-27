import tkinter as tk
from tkinter import messagebox
import time

class DynamicStack:
    class Node:
        def __init__(self, value):
            """
            Inicializa um novo nó da pilha.

            :param value: Valor armazenado no nó.
            """
            self.value = value
            self.next = None

    def __init__(self):
        """
        Inicializa uma pilha dinâmica vazia.
        """
        self.top = None  # O topo da pilha
        self.height = 0  # Altura da pilha

    def push(self, item):
        """
        Adiciona um item ao topo da pilha.

        :param item: Item a ser adicionado.
        """
        try:
            item = float(item)  # Tenta converter para número
        except ValueError:
            pass  # Mantém como string se não for número
        new_node = self.Node(item)  # Cria um novo nó
        new_node.next = self.top  # O novo nó aponta para o topo atual
        self.top = new_node  # Atualiza o topo para o novo nó
        self.height += 1  # Aumenta a altura da pilha
        print(f"{item} foi adicionado à stack.")

    def pop(self):
        """
        Remove e retorna o item do topo da pilha.

        :return: O item removido ou None se a pilha estiver vazia.
        """
        if self.is_empty():  # Verifica se a pilha está vazia
            print("A stack está vazia.")
            return None
        value = self.top.value  # Armazena o valor do topo
        self.top = self.top.next  # Atualiza o topo para o próximo nó
        self.height -= 1  # Diminui a altura da pilha
        print(f"{value} foi removido da stack.")
        return value

    def is_empty(self):
        """
        Verifica se a pilha está vazia.

        :return: True se a pilha estiver vazia, False caso contrário.
        """
        return self.top is None

    def peek(self):
        """
        Retorna o item do topo da pilha sem removê-lo.

        :return: O item do topo ou None se a pilha estiver vazia.
        """
        if not self.is_empty():
            return self.top.value
        else:
            return None

    def size(self):
        """
        Retorna o número de itens na pilha.

        :return: A altura da pilha.
        """
        return self.height

    def get_stack(self):
        """
        Retorna uma lista com os elementos da pilha do fundo para o topo.

        :return: Lista de elementos da pilha.
        """
        stack_elements = []  # Lista para armazenar os elementos
        current = self.top
        while current is not None:  # Percorre a pilha
            stack_elements.append(current.value)
            current = current.next
        return stack_elements[::-1]  # Retorna a pilha invertida (base no final)

    def sort_stack(self):
        """
        Ordena os elementos da pilha em ordem crescente.
        """
        if self.is_empty():  # Se a pilha estiver vazia
            return

        # Função para converter elementos para comparação
        def convert(item):
            try:
                return float(item)  # Tenta converter para float
            except ValueError:
                return item  # Retorna o item se não for numérico

        # Coleta todos os itens em uma lista temporária
        temp_list = []
        current = self.top
        while current:
            temp_list.append(current.value)  # Adiciona o valor à lista
            current = current.next

        # Ordena a lista e reconstrói a pilha
        temp_list.sort(key=convert)  # Ordena a lista
        self.top = None  # Reseta o topo
        self.height = 0  # Reseta a altura
        for item in reversed(temp_list):  # Insere os itens de volta na pilha
            self.push(item)

class DynamicStackGUI:
    def __init__(self, root):
        """
        Inicializa a interface gráfica para a pilha dinâmica.

        :param root: A janela principal da interface gráfica.
        """
        self.stack = DynamicStack()  # Cria uma nova pilha dinâmica
        self.root = root
        self.root.title("Pilha Dinâmica: ")

        self.root.geometry("800x600")  # Define o tamanho da janela

        self.canvas = tk.Canvas(root, bg="white")  # Cria um canvas para desenhar a pilha
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Usando pack() para todos os widgets
        self.label_data = tk.Label(root, text="Elemento:")  # Rótulo para o campo de entrada
        self.label_data.pack(side=tk.LEFT, padx=10, pady=10)

        self.entry_data = tk.Entry(root)  # Campo de entrada para novos elementos
        self.entry_data.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_push = tk.Button(root, text="Inserir na Pilha", command=self.push, bg="lightblue", fg="black")  # Botão para inserir
        self.button_push.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_pop = tk.Button(root, text="Remover da Pilha", command=self.pop, bg="lightblue", fg="black")  # Botão para remover
        self.button_pop.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_sort = tk.Button(root, text="Ordenar a Pilha", command=self.sort_stack, bg="lightblue", fg="black")  # Botão para ordenar
        self.button_sort.pack(side=tk.LEFT, padx=10, pady=10)

        self.stack_items = []  # Lista para armazenar referências aos elementos da pilha
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def push(self):
        """
        Adiciona um novo elemento à pilha e atualiza a interface.
        """
        data = self.entry_data.get()  # Obtém o dado do campo de entrada
        if not data:  # Verifica se o campo está vazio
            messagebox.showerror("Erro", "Preencha o campo de elemento!")  # Exibe erro
            return

        self.stack.push(data)  # Adiciona o elemento à pilha
        self.update_stack_display()  # Atualiza a exibição da pilha
        self.entry_data.delete(0, tk.END)  # Limpa o campo de entrada
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def pop(self):
        """
        Remove o elemento do topo da pilha e atualiza a interface.
        """
        removed = self.stack.pop()  # Remove o elemento do topo
        if removed is not None:  # Verifica se o elemento foi removido
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")  # Exibe informação
            self.update_stack_display()  # Atualiza a exibição da pilha
        else:
            messagebox.showwarning("Aviso", "A pilha está vazia.")  # Aviso se a pilha estiver vazia
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def sort_stack(self):
        """
        Ordena os elementos da pilha e atualiza a interface.
        """
        if not self.stack.is_empty():  # Verifica se a pilha não está vazia
            self.stack.sort_stack()  # Ordena a pilha
            self.update_stack_display()  # Atualiza a exibição da pilha
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def update_stack_display(self):
        """
        Atualiza a exibição visual da pilha no canvas.
        """
        self.canvas.delete("all")  # Limpa os quadrados antigos
        self.stack_items = []  # Reinicia a lista de itens

        # Define a posição inicial do topo, calculando dinamicamente para centralizar na tela
        canvas_width = self.canvas.winfo_width()  # Obtém a largura do canvas
        x_center = canvas_width // 2  # Calcula a posição central
        y_top = 50  # Posição vertical inicial

        stack_elements = self.stack.get_stack()  # Pega a pilha como uma lista para desenhar

        for index, item in enumerate(reversed(stack_elements)):  # Corrige a ordem invertendo a lista para exibir como LIFO
            y_position = y_top + index * 50  # Ajusta a posição para cada elemento

            item_str = str(item)  # Converte o item para string
            item_width = max(100, len(item_str) * 15)  # Largura mínima de 100, ajusta ao tamanho do texto

            # Desenha o quadrado
            square = self.canvas.create_rectangle(
                x_center - item_width // 2, y_position,
                x_center + item_width // 2, y_position + 40,
                fill="lightblue"
            )

            # Verifica se é o topo ou a base para personalizar o texto
            if index == 0:  # Se for o topo da pilha
                text_str = f"Topo\n{item_str}"
            elif index == len(stack_elements) - 1:
                text_str = f"Base\n{item_str}"
            else:
                text_str = item_str  # Apenas o valor para os demais itens

            # Adiciona o texto dentro do quadrado
            text = self.canvas.create_text(x_center, y_position + 20, text=text_str, font=("Arial", 16))

            self.stack_items.append((square, text))  # Armazena a referência ao quadrado e texto

            # Animação de movimento para cada quadrado
            for step in range(10):  # Faz a animação de queda
                self.canvas.move(square, 0, 3)  # Move o quadrado
                self.canvas.move(text, 0, 3)  # Move o texto
                self.canvas.update()  # Atualiza o canvas
                time.sleep(0.02)  # Pausa para animação suave

    def update_buttons_visibility(self):
        """
        Atualiza a visibilidade dos botões com base no estado da pilha.
        """
        if self.stack.is_empty():  # Verifica se a pilha está vazia
            self.button_pop.pack_forget()  # Esconde o botão de remover
            self.button_sort.pack_forget()  # Esconde o botão de ordenar
        else:
            self.button_pop.pack(side=tk.LEFT, padx=10, pady=10)  # Mostra o botão de remover
            self.button_sort.pack(side=tk.LEFT, padx=10, pady=10)  # Mostra o botão de ordenar


# Criação da interface
root = tk.Tk()  # Cria a janela principal
app = DynamicStackGUI(root)  # Inicializa a GUI da pilha dinâmica
root.mainloop()  # Inicia o loop principal da interface
