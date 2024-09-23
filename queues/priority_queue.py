import tkinter as tk
from tkinter import messagebox
import time

class Node:
    def __init__(self, data, priority):
        """Inicializa um nó com dados e prioridade.
        
        Args:
            data: O valor armazenado no nó.
            priority: A prioridade do nó.
        """
        self.data = data
        self.priority = priority
        self.next = None

class PriorityQueue:
    def __init__(self):
        """Cria uma fila de prioridade vazia."""
        self.front = None
        self.size = 0
    
    def is_empty(self):
        """Verifica se a fila está vazia.
        
        Returns:
            bool: True se a fila estiver vazia, caso contrário, False.
        """
        return self.front is None
    
    def enqueue(self, data, priority):
        """Adiciona um novo elemento à fila de prioridade.
        
        Args:
            data: O valor a ser inserido na fila.
            priority: A prioridade do valor a ser inserido.
        """
        new_node = Node(data, priority)  # Cria um novo nó com os dados e a prioridade
        
        # Se a fila estiver vazia ou se o novo nó tiver maior prioridade
        if self.is_empty() or self.front.priority > priority:
            new_node.next = self.front  # O novo nó se torna o front
            self.front = new_node
        else:
            current = self.front
            # Encontra a posição correta para o novo nó
            while current.next and current.next.priority <= priority:
                current = current.next
            
            new_node.next = current.next  # Insere o novo nó na posição correta
            current.next = new_node
        
        self.size += 1
        print(f"Elemento '{data}' com prioridade {priority} foi adicionado à fila.")

    def dequeue(self):
        """Remove o elemento de maior prioridade da fila.
        
        Returns:
            O valor do nó removido, ou None se a fila estiver vazia.
        """
        if self.is_empty():
            return None
        
        removed_value = self.front.data  # Guarda o valor a ser removido
        self.front = self.front.next  # Remove o elemento do topo
        if self.front is None:  # Se a fila ficou vazia
            self.size = 0
        else:
            self.size -= 1
        
        print(f"Elemento '{removed_value}' foi removido da fila.")
        return removed_value
    
    def print_queue(self):
        """Retorna a lista de elementos e suas prioridades na fila.
        
        Returns:
            list: Uma lista de tuplas contendo dados e prioridades dos elementos na fila.
        """
        if self.is_empty():
            return []
        
        current = self.front
        queue_list = []
        while current:
            queue_list.append((current.data, current.priority))  # Adiciona o elemento à lista
            current = current.next
        return queue_list

# Interface com Tkinter
class PriorityQueueGUI:
    def __init__(self, root):
        """Inicializa a interface gráfica para a fila de prioridade.
        
        Args:
            root: A janela principal da aplicação Tkinter.
        """
        self.queue = PriorityQueue()  # Cria uma instância da fila de prioridade
        self.root = root
        self.root.title("Fila de Prioridade")

        # Aumentar a área visível
        self.canvas = tk.Canvas(root, bg="white", height=600, width=1200)  # Aumenta a largura e altura do canvas
        self.canvas.grid(row=0, column=0, columnspan=3)
        
        # Entradas e rótulos para o dado e a prioridade
        self.label_data = tk.Label(root, text="Elemento:")  # Rótulo para o elemento
        self.label_data.grid(row=2, column=0)
        self.entry_data = tk.Entry(root)  # Campo de entrada para o elemento
        self.entry_data.grid(row=2, column=1)
        
        self.label_priority = tk.Label(root, text="Prioridade:")  # Rótulo para a prioridade
        self.label_priority.grid(row=3, column=0)
        self.entry_priority = tk.Entry(root)  # Campo de entrada para a prioridade
        self.entry_priority.grid(row=3, column=1)
        
        # Botões de interação
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)  # Botão para inserir
        self.button_enqueue.grid(row=4, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)  # Botão para remover
        self.button_dequeue.grid(row=5, column=0, columnspan=2)

        self.queue_items = []  # Armazena os retângulos e textos na tela
        self.update_queue_display()  # Atualiza a exibição da fila no início
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões no início

    def enqueue(self):
        """Adiciona um novo elemento à fila de prioridade e atualiza a exibição."""
        data = self.entry_data.get()  # Obtém o dado do campo de entrada
        priority = self.entry_priority.get()  # Obtém a prioridade do campo de entrada
        
        # Verifica se os campos estão preenchidos
        if not data or not priority:
            messagebox.showerror("Erro", "Preencha todos os campos!")  # Mensagem de erro se campos vazios
            return
        
        # Tenta converter a prioridade para um número inteiro
        try:
            priority = int(priority)
        except ValueError:
            messagebox.showerror("Erro", "A prioridade deve ser um número inteiro.")  # Mensagem de erro se não for um número
            return
        
        self.queue.enqueue(data, priority)  # Insere o elemento na fila
        self.entry_data.delete(0, tk.END)  # Limpa o campo de dados
        self.entry_priority.delete(0, tk.END)  # Limpa o campo de prioridade
        
        self.update_queue_display(animated=True)  # Atualiza a exibição da fila com animação
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após a inserção

    def dequeue(self):
        """Remove o elemento do topo da fila e atualiza a exibição."""
        removed = self.queue.dequeue()  # Remove o elemento do topo da fila
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")  # Mensagem de confirmação
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")  # Mensagem de aviso se a fila estiver vazia
        
        self.update_queue_display(animated=False)  # Atualiza a exibição da fila sem animação
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após a remoção

    def update_queue_display(self, animated=False):
        """Desenha a fila na interface gráfica.
        
        Args:
            animated: Indica se a atualização deve ser animada (padrão é False).
        """
        self.canvas.delete("all")  # Limpa os retângulos antigos
        self.queue_items = []

        # Calcula posição inicial para o topo
        x_start = 50
        y_center = self.canvas.winfo_height() // 2  # Centraliza verticalmente

        queue_list = self.queue.print_queue()  # Pega os elementos da fila

        # Desenha cada elemento da fila
        for index, (data, priority) in enumerate(queue_list):
            item_str = f"E: {data}, P: {priority}"  # Formatação atualizada
            item_width = 150  # Define uma largura fixa
            x_position = x_start + index * (item_width + 50)  # Espaço fixo entre os elementos

            square = self.canvas.create_rectangle(
                x_position, y_center - 20, 
                x_position + item_width, y_center + 20,
                fill="lightblue"  # Cor do retângulo
            )

            # Formata o texto a ser exibido
            if index == 0:
                text_str = f"Topo\n{item_str}"  # Indica o elemento do topo
            else:
                text_str = item_str

            # Diminuir o tamanho da fonte
            text = self.canvas.create_text(
                x_position + item_width // 2, y_center,
                text=text_str, font=("Arial", 10)  # Reduzindo o tamanho da fonte
            )

            self.queue_items.append((square, text))  # Armazena os itens desenhados

            # Se for para animar, move o quadrado da direita para a esquerda
            if animated:
                for step in range(10):  # Animação de movimento
                    self.canvas.move(square, -2, 0)
                    self.canvas.move(text, -2, 0)
                    self.canvas.update()  # Atualiza a tela
                    time.sleep(0.02)  # Espera um pouco entre os passos

    def update_buttons_visibility(self):
        """Atualiza a visibilidade dos botões com base no estado da fila."""
        if self.queue.is_empty():  # Se a fila estiver vazia
            self.button_dequeue.grid_remove()  # Remove o botão de remoção
        else:
            self.button_dequeue.grid(row=5, column=0, columnspan=2)  # Mostra o botão de remoção

        # Sempre exibe o botão de inserção e os campos de entrada
        self.button_enqueue.grid(row=4, column=0, columnspan=2)
        self.label_data.grid(row=2, column=0)
        self.entry_data.grid(row=2, column=1)
        self.label_priority.grid(row=3, column=0)
        self.entry_priority.grid(row=3, column=1)

# Execução da interface gráfica
root = tk.Tk()  # Cria a janela principal
app = PriorityQueueGUI(root)  # Cria uma instância da GUI
root.mainloop()  # Inicia o loop da interface
