import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DynamicQueue:
    def __init__(self):
        self.front = None  # O início da fila
        self.rear = None   # O final da fila
        self.size = 0      # Tamanho da fila
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:  # Se a fila estiver vazia
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1
        print(f"{item} foi adicionado à fila.")
    
    def dequeue(self):
        if self.is_empty():
            print("A fila está vazia.")
            return None
        
        removed_value = self.front.data
        self.front = self.front.next
        if self.front is None:  # Se a fila ficou vazia
            self.rear = None
        
        self.size -= 1
        print(f"{removed_value} foi removido da fila.")
        return removed_value
    
    def peek(self):  # Retorna o primeiro elemento da fila
        if self.is_empty():
            print("A fila está vazia.")
            return None
        return self.front.data
    
    def sort_queue(self):
        if self.is_empty():
            return
        
        # Armazena os nós em uma lista
        nodes = []
        current = self.front
        while current:
            nodes.append(current.data)
            current = current.next
        
        # Ordena priorizando strings e depois números
        nodes.sort(key=lambda x: (isinstance(x, str), str(x) if isinstance(x, str) else int(x)))
        
        # Reconstrói a fila ordenada
        self.front = None
        self.rear = None
        self.size = 0
        for data in nodes:
            self.enqueue(data)
    
    def print_queue(self):
        if self.is_empty():
            return []
        
        current = self.front
        queue_list = []
        while current:
            queue_list.append(current.data)
            current = current.next
        return queue_list

# Interface com Tkinter
class DynamicQueueGUI:
    def __init__(self, root):
        self.queue = DynamicQueue()
        self.root = root
        self.root.title("Fila Dinâmica: ")
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=0, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=0, column=1)
        
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)
        self.button_enqueue.grid(row=2, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)
        self.button_dequeue.grid(row=3, column=0, columnspan=2)
        
        self.button_sort = tk.Button(root, text="Ordenar a Fila", command=self.sort_queue)
        self.button_sort.grid(row=3, column=2)  # Adiciona o botão de ordenação à grade
        
        self.queue_display = tk.Text(root, height=10, width=30)
        self.queue_display.grid(row=4, column=0, columnspan=3)
        
        self.update_queue_display()
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões ao iniciar
    
    def enqueue(self):
        data = self.entry_data.get()
        
        if not data:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        self.queue.enqueue(data)
        self.update_queue_display()
        self.entry_data.delete(0, tk.END)  
        
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após inserção
    
    def dequeue(self):
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        self.update_queue_display()
        
        self.update_buttons_visibility()  # Atualiza a visibilidade dos botões após remoção
    
    def sort_queue(self):
        self.queue.sort_queue()  # Chama a função de ordenação da fila
        self.update_queue_display()
        messagebox.showinfo("Ordenação", "A fila foi ordenada.")
    
    def update_queue_display(self):
        self.queue_display.delete(1.0, tk.END)
        queue_list = self.queue.print_queue()
        if not queue_list:
            self.queue_display.insert(tk.END, "Fila dinâmica está vazia.")
        else:
            for index, data in enumerate(queue_list):
                if index == 0:
                    self.queue_display.insert(tk.END, f"Topo -> {data}\n")
                elif index == len(queue_list) - 1:
                    self.queue_display.insert(tk.END, f"Base -> {data}\n")
                else:
                    self.queue_display.insert(tk.END, f"        {data}\n")
    
    def update_buttons_visibility(self):
        """Atualiza a visibilidade dos botões com base no estado da fila."""
        if self.queue.is_empty():
            self.button_dequeue.grid_remove()  # Esconde o botão de remoção se a fila estiver vazia
            self.button_sort.grid_remove()      # Esconde o botão de ordenação se a fila estiver vazia
        else:
            self.button_dequeue.grid()  # Mostra o botão de remoção se a fila não estiver vazia
            self.button_sort.grid()      # Mostra o botão de ordenação se a fila não estiver vazia

# Execução da interface gráfica
root = tk.Tk()
app = DynamicQueueGUI(root)
root.mainloop()
