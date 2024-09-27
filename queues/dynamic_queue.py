import tkinter as tk
from tkinter import messagebox
import time

# Classe que representa um nó da fila dinâmica
class Node:
    def __init__(self, data):
        self.data = data  # Dados armazenados no nó
        self.next = None  # Referência para o próximo nó

# Classe que implementa uma fila dinâmica
class DynamicQueue:
    def __init__(self):
        self.front = None  # O início da fila (nó da frente)
        self.size = 0      # Tamanho da fila

    def is_empty(self):
        # Retorna True se a fila estiver vazia
        return self.front is None
    
    def enqueue(self, item):
        # Adiciona um item ao final da fila
        new_node = Node(item)  # Cria um novo nó com o item
        if self.front is None:  # Se a fila estiver vazia
            self.front = new_node  # O novo nó é o primeiro
        else:
            current = self.front
            # Percorre até o final da fila
            while current.next:
                current = current.next
            current.next = new_node  # Adiciona o novo nó no final
        
        self.size += 1  # Incrementa o tamanho da fila
        print(f"{item} foi adicionado à fila.")
    
    def dequeue(self):
        # Remove e retorna o primeiro item da fila
        if self.is_empty():
            print("A fila está vazia.")
            return None
        
        removed_value = self.front.data  # Armazena o valor a ser removido
        self.front = self.front.next  # Move o front para o próximo nó
        self.size -= 1  # Decrementa o tamanho da fila
        print(f"{removed_value} foi removido da fila.")
        return removed_value
    
    def peek(self):
        # Retorna o primeiro elemento da fila sem removê-lo
        if self.is_empty():
            print("A fila está vazia.")
            return None
        return self.front.data
    
    def sort_queue(self):
        # Ordena a fila em ordem crescente
        if self.is_empty():
            return
    
        nodes = []
        current = self.front
        # Armazena todos os valores da fila
        while current:
            try:
                nodes.append(int(current.data))  # Converte para inteiro, se possível
            except ValueError:
                nodes.append(current.data)  # Mantém como string
            current = current.next
        
        # Ordena primeiro números, depois strings
        nodes.sort(key=lambda x: (isinstance(x, str), x))
    
        # Reconstrói a fila ordenada
        self.front = None
        self.size = 0
        for data in nodes:
            self.enqueue(data)  # Reinsere os dados na fila
    
    def print_queue(self):
        # Retorna uma lista dos elementos da fila
        if self.is_empty():
            return []
        
        current = self.front
        queue_list = []
        # Percorre a fila e adiciona os elementos à lista
        while current:
            queue_list.append(current.data)
            current = current.next
        return queue_list

# Classe que implementa a interface gráfica usando Tkinter
class DynamicQueueGUI:
    def __init__(self, root, max_size):
        self.queue = DynamicQueue()  # Inicializa a fila dinâmica
        self.root = root
        self.root.title("Fila Dinâmica: ")

        # Criação da área de desenho
        self.canvas = tk.Canvas(root, bg="white", height=400, width=800)
        self.canvas.grid(row=0, column=0, columnspan=3)
        
        # Campo de entrada para o elemento
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=2, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=2, column=1)
        
        # Botão para inserir na fila
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue, bg="lightblue", fg="black")
        self.button_enqueue.grid(row=3, column=0, columnspan=2)
        
        # Botão para remover da fila
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue, bg="lightblue", fg="black")
        self.button_dequeue.grid(row=4, column=0, columnspan=2)

        # Botão para ordenar a fila
        self.button_sort = tk.Button(root, text="Ordenar a Fila", command=self.sort_queue, bg="lightblue", fg="black")
        self.button_sort.grid(row=4, column=2)

        self.queue_items = []  # Armazena os retângulos e textos na tela
        self.update_queue_display()  # Atualiza a visualização da fila
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def enqueue(self):
        # Função para adicionar um elemento à fila
        data = self.entry_data.get()

        if not data:  # Verifica se o campo está vazio
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        self.queue.enqueue(data)  # Chama a função de enqueue
        self.entry_data.delete(0, tk.END)  # Limpa o campo de entrada
        
        self.update_queue_display(animated=True)  # Atualiza a visualização com animação
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def dequeue(self):
        # Função para remover um elemento da fila
        removed = self.queue.dequeue()  # Chama a função de dequeue
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        
        self.update_queue_display()  # Atualiza a visualização da fila
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões

    def sort_queue(self):
        # Função para ordenar a fila
        if not self.queue.is_empty():
            self.queue.sort_queue()  # Chama a função de ordenação
            self.update_queue_display(animated=False)  # Atualiza a visualização sem animação
            messagebox.showinfo("Ordenação", "A fila foi ordenada.")
    
    def update_queue_display(self, animated=False):
        # Atualiza a visualização dos elementos da fila
        self.canvas.delete("all")  # Limpa os retângulos antigos
        self.queue_items = []  # Reinicializa a lista de itens da fila

        # Calcula posição inicial para o topo
        x_start = 50
        y_center = self.canvas.winfo_height() // 2

        queue_list = self.queue.print_queue()  # Obtém a lista atual da fila

        # Desenha cada elemento da fila
        for index, item in enumerate(queue_list):
            item_str = str(item)
            item_width = max(100, len(item_str) * 15)  # Largura ajustável com base no texto
            x_position = x_start + index * (item_width + 20)  # Espaço entre os elementos

            # Criação do retângulo para o elemento
            square = self.canvas.create_rectangle(
                x_position, y_center - 20, 
                x_position + item_width, y_center + 20,
                fill="lightblue"
            )

            # Exibe "Topo" para o primeiro item
            if index == 0:
                text_str = f"Topo\n{item_str}"
            else:
                text_str = item_str

            # Criação do texto do elemento
            text = self.canvas.create_text(
                x_position + item_width // 2, y_center,
                text=text_str, font=("Arial", 16)
            )

            self.queue_items.append((square, text))  # Armazena o retângulo e o texto

            # Anima apenas o novo item adicionado
            if animated and index == len(queue_list) - 1:
                self.animate_insertion(square, text, x_position)

    def animate_insertion(self, square, text, final_x):
        # Anima a inserção de um novo item na fila
        initial_x = 800  # Começa do lado direito fora da tela
        y_center = self.canvas.winfo_height() // 2
        
        # Divide o movimento em etapas menores para simular a curva
        steps = 70  # Mais passos para diminuir a velocidade
        for step in range(steps):
            # Movimento não linear (curvado)
            progress = step / steps
            x_step = initial_x + (final_x - initial_x) * progress
            y_offset = -30 * (1 - progress)  # A curva vai suavizando
            
            # Atualiza a posição do retângulo e do texto
            self.canvas.coords(square, x_step, y_center - 20 + y_offset, x_step + 100, y_center + 20 + y_offset)
            self.canvas.coords(text, x_step + 50, y_center + y_offset)
            self.canvas.update()
            time.sleep(0.03)  # Atraso para diminuir a velocidade

    def update_buttons_visibility(self):
        # Atualiza a visibilidade dos botões com base no estado da fila
        if self.queue.is_empty():
            self.button_dequeue.grid_remove()  # Esconde o botão de remover
            self.button_sort.grid_remove()      # Esconde o botão de ordenar
        else:
            self.button_dequeue.grid()           # Mostra o botão de remover
            self.button_sort.grid()              # Mostra o botão de ordenar

# Criação da interface
root = tk.Tk()
app = DynamicQueueGUI(root, 5)  # Instancia a GUI com um tamanho máximo
root.mainloop()  # Inicia o loop principal da aplicação
