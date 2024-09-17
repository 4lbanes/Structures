import tkinter as tk
from tkinter import messagebox

class StaticQueue:
    def __init__(self, max_size):
        self.itens = []
        self.size_max = max_size
    
    def enqueue(self, item):  # Adiciona um item à fila (inserção no final)
        if not self.is_full():
            self.itens.append(item)
            print(f"{item} foi adicionado à fila.")
        else:
            print("A fila está cheia.")
    
    def dequeue(self):  # Remove um item da fila (remoção no início)
        if not self.is_empty():
            item = self.itens.pop(0)
            print(f"{item} foi removido da fila.")
            return item
        else:
            print("A fila está vazia.")
            return None
    
    def is_empty(self):
        return len(self.itens) == 0
    
    def is_full(self):
        return len(self.itens) == self.size_max
    
    def peek(self):  # Mostra o primeiro elemento da fila sem removê-lo
        if not self.is_empty():
            return self.itens[0]
        else:
            return None
    
    def size(self):
        return len(self.itens)
    
    def print_queue(self):
        if self.is_empty():
            return []
        
        queue_list = []
        for i in range(len(self.itens)):
            queue_list.append(self.itens[i])
        return queue_list

    def sort_queue(self):
        # Ordena a fila priorizando strings
        self.itens.sort(key=lambda x: (isinstance(x, str), x))
        print("A fila foi ordenada.")

# Interface com Tkinter
class StaticQueueGUI:
    def __init__(self, root, max_size):
        self.queue = StaticQueue(max_size)  # Tamanho máximo da fila fornecido na inicialização
        self.root = root
        self.root.title("Fila Estática: ")
        
        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da fila: {max_size}")
        self.label_max_size.grid(row=0, column=0, columnspan=2)
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=1, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=1, column=1)
        
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)
        self.button_enqueue.grid(row=2, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)
        self.button_dequeue.grid(row=3, column=0, columnspan=2)

        self.button_sort = tk.Button(root, text="Ordenar a Fila", command=self.sort_queue)
        self.button_sort.grid(row=3, column=2)  # Adiciona o botão de ordenação à grade
        
        self.queue_display = tk.Text(root, height=10, width=30)
        self.queue_display.grid(row=4, column=0, columnspan=2)
        
        self.update_queue_display()
        self.update_buttons_visibility() 
    
    def enqueue(self):
        data = self.entry_data.get()
        
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        if self.queue.is_full():
            messagebox.showwarning("Aviso", "A fila está cheia.")
            return
        
        self.queue.enqueue(data)
        self.update_queue_display()
        self.entry_data.delete(0, tk.END)
        
        self.update_buttons_visibility() 

    def dequeue(self):
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        self.update_queue_display()
        
        self.update_buttons_visibility()  

    def sort_queue(self):
        if not self.queue.is_empty():
            self.queue.sort_queue()  
            self.update_queue_display()
            messagebox.showinfo("Ordenação", "A fila foi ordenada.")

    def update_queue_display(self):
        self.queue_display.delete(1.0, tk.END)
        queue_list = self.queue.print_queue()
        if not queue_list:
            self.queue_display.insert(tk.END, "Fila estática está vazia.")
        else:
            for index, data in enumerate(queue_list):
                if index == 0:
                    self.queue_display.insert(tk.END, f"Topo -> {data}\n")
                elif index == len(queue_list) - 1:
                    self.queue_display.insert(tk.END, f"Base -> {data}\n")
                else:
                    self.queue_display.insert(tk.END, f"        {data}\n")
    
    def update_buttons_visibility(self):    
        if self.queue.is_empty():
            # Se a fila estiver vazia, ocultar o botão de remoção e de ordenação
            self.button_dequeue.grid_remove()
            self.button_sort.grid_remove()
        else:
            self.button_dequeue.grid()  # Mostra o botão de remoção se a fila não estiver vazia
            self.button_sort.grid()      # Mostra o botão de ordenação se a fila não estiver vazia

        if self.queue.is_full():
            # Se a fila estiver cheia, ocultar o botão de inserção
            self.button_enqueue.grid_remove()
            self.label_data.grid_remove()
            self.entry_data.grid_remove()
        else:
            # Se a fila não estiver cheia, garantir que o botão de inserção apareça
            self.button_enqueue.grid()
            self.label_data.grid()
            self.entry_data.grid()

# Criação da fila e da interface
root = tk.Tk()
app = StaticQueueGUI(root, 5)
root.mainloop()

