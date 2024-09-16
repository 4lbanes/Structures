import tkinter as tk
from tkinter import simpledialog, messagebox

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

# Interface com Tkinter
class StaticQueueGUI:
    def __init__(self, root, max_size):
        self.queue = StaticQueue(max_size)  # Tamanho máximo da fila fornecido na inicialização
        self.root = root
        self.root.title("Fila Estática")
        
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
        
        self.queue_display = tk.Text(root, height=10, width=30)
        self.queue_display.grid(row=4, column=0, columnspan=2)
        
        self.update_queue_display()
    
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
        
        if self.queue.is_full():
            self.label_data.grid_remove()
            self.entry_data.grid_remove()
            self.button_enqueue.grid_remove()

    def dequeue(self):
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        self.update_queue_display()
    
        if not self.queue.is_full():
            self.label_data.grid()
            self.entry_data.grid()
            self.button_enqueue.grid()

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
                    
def start_app():
    root = tk.Tk()

    max_size = simpledialog.askinteger("Tamanho da Fila", "Digite o tamanho máximo da fila:", minvalue=1)

    if max_size is None:
        messagebox.showerror("Erro", "Você precisa inserir um tamanho válido!")
        root.destroy() 
    else:
        app = StaticQueueGUI(root, max_size)
        root.mainloop()

# Execução da aplicação
start_app()
