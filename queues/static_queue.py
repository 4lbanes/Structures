import tkinter as tk
from tkinter import messagebox
import time

class StaticQueue:
    def __init__(self, max_size):
        self.queue = [None] * max_size  # Cria uma lista com tamanho máximo
        self.size = 0                   # Tamanho atual da fila
        self.size_max = max_size        # Tamanho máximo da fila

    def is_empty(self):
        """Verifica se a fila está vazia."""
        return self.size == 0
    
    def is_full(self):
        """Verifica se a fila está cheia."""
        return self.size == self.size_max
    
    def enqueue(self, value):
        """Adiciona um novo valor ao final da fila."""
        if self.is_full():
            print("Queue is Full!")
            return
        
        self.queue[self.size] = value  # Insere o novo valor no final da fila
        self.size += 1
        print(f"{value} foi adicionado à fila.")
    
    def dequeue(self):
        """Remove o primeiro elemento da fila."""
        if self.is_empty():
            print("Queue is Empty")
            return None
        
        removed_element = self.queue[0]  # Remove o primeiro elemento da fila

        # Move os elementos restantes para a esquerda
        for i in range(self.size - 1):
            self.queue[i] = self.queue[i + 1]

        self.queue[self.size - 1] = None  # Limpa o último valor
        self.size -= 1

        print(f"{removed_element} foi removido da fila.")
        return removed_element
    
    def peek(self):
        """Mostra o primeiro elemento da fila sem removê-lo."""
        if self.is_empty():
            print("Queue is Empty")
            return None
        return self.queue[0]

    def print_queue(self):
        """Retorna os elementos válidos da fila."""
        if self.is_empty():
            return []
        return self.queue[:self.size]  # Retorna apenas os elementos válidos da fila

    def sort_queue(self):
        """Ordena a fila do menor para o maior."""
        if self.is_empty():
            return
        
        # Converter os elementos para inteiros para ordenar corretamente
        elements_to_sort = [int(item) for item in self.queue if item is not None]

        # Algoritmo de ordenação bolha
        for i in range(len(elements_to_sort) - 1):
            for j in range(len(elements_to_sort) - 1 - i):
                if elements_to_sort[j] > elements_to_sort[j + 1]:
                    elements_to_sort[j], elements_to_sort[j + 1] = elements_to_sort[j + 1], elements_to_sort[j]
        
        # Atualizar a fila com os elementos ordenados
        for i in range(len(elements_to_sort)):
            self.queue[i] = str(elements_to_sort[i])  # Convertendo de volta para string

        # Preencher o restante da fila com None
        for i in range(len(elements_to_sort), self.size_max):
            self.queue[i] = None

class StaticQueueGUI:
    def __init__(self, root, max_size):
        self.queue = StaticQueue(max_size)  # Cria uma nova fila estática
        self.root = root
        self.root.title("Fila Estática")

        # Configuração do canvas para visualização
        self.canvas = tk.Canvas(root, bg="white", height=400, width=800)
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Labels e campos de entrada
        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da fila: {max_size}")
        self.label_max_size.grid(row=1, column=0, columnspan=2)
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=2, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=2, column=1)
        
        # Botões para operações na fila
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)
        self.button_enqueue.grid(row=3, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)
        self.button_dequeue.grid(row=4, column=0, columnspan=2)

        self.button_sort = tk.Button(root, text="Ordenar a Fila", command=self.sort_queue)
        self.button_sort.grid(row=4, column=2)

        self.queue_items = []  # Armazena os retângulos e textos na tela
        self.update_queue_display()
        self.update_buttons_visibility()

    def enqueue(self):
        """Adiciona um novo elemento à fila e atualiza a exibição."""
        data = self.entry_data.get()

        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        if self.queue.is_full():
            messagebox.showwarning("Aviso", "A fila está cheia.")
            return
        
        self.queue.enqueue(data)  # Insere o elemento na fila
        self.entry_data.delete(0, tk.END)
        
        self.update_queue_display(animated=True)  # Atualiza a exibição da fila com animação
        self.update_buttons_visibility()

    def dequeue(self):
        """Remove o elemento do início da fila e atualiza a exibição."""
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        
        self.update_queue_display(animated=False)  # Atualiza a exibição da fila sem animação
        self.update_buttons_visibility()

    def sort_queue(self):
        """Ordena a fila e atualiza a exibição."""
        if not self.queue.is_empty():
            self.queue.sort_queue()  
            self.update_queue_display(animated=False)  # Atualiza a exibição da fila sem animação
            messagebox.showinfo("Ordenação", "A fila foi ordenada.")
    
    def update_queue_display(self, animated=False):
        """Desenha a fila na interface gráfica."""
        self.canvas.delete("all")  # Limpa os retângulos antigos
        self.queue_items = []

        # Calcula posição inicial para o topo
        x_start = 50
        y_center = self.canvas.winfo_height() // 2

        queue_list = self.queue.print_queue()  # Pega os elementos da fila

        # Desenha cada elemento da fila
        for index, item in enumerate(queue_list):
            item_str = str(item)
            item_width = max(100, len(item_str) * 15)  # Largura ajustável com base no texto
            x_position = x_start + index * (item_width + 20)  # Espaço entre os elementos

            square = self.canvas.create_rectangle(
                x_position, y_center - 20, 
                x_position + item_width, y_center + 20,
                fill="lightblue"
            )

            text = self.canvas.create_text(
                x_position + item_width // 2, y_center,
                text=item_str, font=("Arial", 16)
            )

            self.queue_items.append((square, text))  # Armazena o item

            # Se for para animar, move o quadrado da direita para a esquerda
            if animated and index == len(queue_list) - 1:
                self.animate_insertion(square, text, x_position)

    def animate_insertion(self, square, text, final_x):
        """Anima a inserção de um novo elemento na fila."""
        initial_x = 800  # Começa do lado direito fora da tela
        y_center = self.canvas.winfo_height() // 2
        
        # Divide o movimento em etapas menores para simular a curva
        steps = 70  # Mais passos para diminuir a velocidade
        for step in range(steps):
            progress = step / steps  # Progresso da animação
            x_step = initial_x + (final_x - initial_x) * progress
            y_offset = -30 * (1 - progress)  # A curva vai suavizando
            
            self.canvas.coords(square, x_step, y_center - 20 + y_offset, x_step + 100, y_center + 20 + y_offset)
            self.canvas.coords(text, x_step + 50, y_center + y_offset)
            self.canvas.update()
            time.sleep(0.03)  # Mais tempo para diminuir a velocidade 

    def update_buttons_visibility(self):
        """Atualiza a visibilidade dos botões de acordo com o estado da fila."""
        if self.queue.is_empty():
            self.button_dequeue.grid_remove()
            self.button_sort.grid_remove()
        else:
            self.button_dequeue.grid()
            self.button_sort.grid()

        if self.queue.is_full():
            self.button_enqueue.grid_remove()
            self.label_data.grid_remove()
            self.entry_data.grid_remove()
        else:
            self.button_enqueue.grid()
            self.label_data.grid()
            self.entry_data.grid()

# Criação da interface
root = tk.Tk()
app = StaticQueueGUI(root, 5)  # Cria uma instância da GUI com um tamanho máximo de 5
root.mainloop()  # Inicia o loop da interface
