import tkinter as tk
from tkinter import messagebox
import time

class Node:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.front = None
        self.size = 0
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, data, priority):
        new_node = Node(data, priority)
        
        if self.is_empty() or self.front.priority > priority:  # Inserção no início
            new_node.next = self.front
            self.front = new_node
        else:
            current = self.front
            while current.next and current.next.priority <= priority:  # Inserção ordenada pela prioridade
                current = current.next
            
            new_node.next = current.next
            current.next = new_node
        
        self.size += 1
        print(f"Elemento '{data}' com prioridade {priority} foi adicionado à fila.")

    def dequeue(self):
        if self.is_empty():
            return None
        
        removed_value = self.front.data
        self.front = self.front.next  # Remove o elemento do topo
        if self.front is None:  # Se a fila ficou vazia
            self.size = 0
        else:
            self.size -= 1
        
        print(f"Elemento '{removed_value}' foi removido da fila.")
        return removed_value
    
    def print_queue(self):
        if self.is_empty():
            return []
        
        current = self.front
        queue_list = []
        while current:
            queue_list.append((current.data, current.priority))
            current = current.next
        return queue_list

# Interface com Tkinter
class PriorityQueueGUI:
    def __init__(self, root):
        self.queue = PriorityQueue()
        self.root = root
        self.root.title("Fila de Prioridade: ")

        # Aumentar a área visível
        self.canvas = tk.Canvas(root, bg="white", height=600, width=1200)  # Aumenta a largura e altura do canvas
        self.canvas.grid(row=0, column=0, columnspan=3)
        
        # Entradas e rótulos para o dado e a prioridade
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=2, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=2, column=1)
        
        self.label_priority = tk.Label(root, text="Prioridade:")
        self.label_priority.grid(row=3, column=0)
        self.entry_priority = tk.Entry(root)
        self.entry_priority.grid(row=3, column=1)
        
        # Botões de interação
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)
        self.button_enqueue.grid(row=4, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)
        self.button_dequeue.grid(row=5, column=0, columnspan=2)

        self.queue_items = []  # Armazena os retângulos e textos na tela
        self.update_queue_display()
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões no início

    def enqueue(self):
        data = self.entry_data.get()
        priority = self.entry_priority.get()
        
        if not data or not priority:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        # Tenta converter a prioridade para um número inteiro
        try:
            priority = int(priority)
        except ValueError:
            messagebox.showerror("Erro", "A prioridade deve ser um número inteiro.")
            return
        
        self.queue.enqueue(data, priority)
        self.entry_data.delete(0, tk.END)  # Limpa o campo de dados
        self.entry_priority.delete(0, tk.END)  # Limpa o campo de prioridade
        
        self.update_queue_display(animated=True)
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após a inserção

    def dequeue(self):
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        
        self.update_queue_display(animated=False)
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após a remoção

    def update_queue_display(self, animated=False):
        # Limpa os retângulos antigos
        self.canvas.delete("all")
        self.queue_items = []

        # Calcula posição inicial para o topo
        x_start = 50
        y_center = self.canvas.winfo_height() // 2

        queue_list = self.queue.print_queue()

        # Desenha cada elemento da fila
        for index, (data, priority) in enumerate(queue_list):
            item_str = f"E: {data}, P: {priority}"  # Formatação atualizada
            item_width = 150  # Define uma largura fixa
            x_position = x_start + index * (item_width + 50)  # Espaço fixo entre os elementos

            square = self.canvas.create_rectangle(
                x_position, y_center - 20, 
                x_position + item_width, y_center + 20,
                fill="lightblue"
            )

            if index == 0:
                text_str = f"Topo\n{item_str}"
            elif index == len(queue_list) - 1:
                text_str = f"Base\n{item_str}"
            else:
                text_str = item_str

            # Diminuir o tamanho da fonte
            text = self.canvas.create_text(
                x_position + item_width // 2, y_center,
                text=text_str, font=("Arial", 10)  # Reduzindo o tamanho da fonte
            )

            self.queue_items.append((square, text))

            # Se for para animar, move o quadrado da direita para a esquerda
            if animated:
                for step in range(10):
                    self.canvas.move(square, -2, 0)
                    self.canvas.move(text, -2, 0)
                    self.canvas.update()
                    time.sleep(0.02)

    def update_buttons_visibility(self):
        if self.queue.is_empty():
            self.button_dequeue.grid_remove()
        else:
            self.button_dequeue.grid(row=5, column=0, columnspan=2)
        
        # Não há uma função para verificar se a fila está cheia, então removi o controle relacionado à fila cheia
        self.button_enqueue.grid(row=4, column=0, columnspan=2)
        self.label_data.grid(row=2, column=0)
        self.entry_data.grid(row=2, column=1)
        self.label_priority.grid(row=3, column=0)
        self.entry_priority.grid(row=3, column=1)

# Execução da interface gráfica
root = tk.Tk()
app = PriorityQueueGUI(root)
root.mainloop()
