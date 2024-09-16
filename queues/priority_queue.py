import tkinter as tk
from tkinter import messagebox

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
        
        if self.is_empty() or self.front.priority > priority:
            new_node.next = self.front
            self.front = new_node
        else:
            current = self.front
            while current.next and current.next.priority <= priority:
                current = current.next
            
            new_node.next = current.next
            current.next = new_node
        
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            return None
        
        removed_value = self.front.data
        self.front = self.front.next
        self.size -= 1
        return removed_value
    
    def peek(self):
        if self.is_empty():
            return None
        return self.front.data
    
    def max_priority(self):
        if self.is_empty():
            return None
        return self.front.priority
        
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
        self.root.title("Fila de Prioridade")
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=0, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=0, column=1)
        
        self.label_priority = tk.Label(root, text="Prioridade:")
        self.label_priority.grid(row=1, column=0)
        self.entry_priority = tk.Entry(root)
        self.entry_priority.grid(row=1, column=1)
        
        self.button_enqueue = tk.Button(root, text="Inserir na Fila", command=self.enqueue)
        self.button_enqueue.grid(row=2, column=0, columnspan=2)
        
        self.button_dequeue = tk.Button(root, text="Remover da Fila", command=self.dequeue)
        self.button_dequeue.grid(row=3, column=0, columnspan=2)
        
        self.queue_display = tk.Text(root, height=10, width=30)
        self.queue_display.grid(row=4, column=0, columnspan=2)
        
        self.update_queue_display()
    
    def enqueue(self):
        data = self.entry_data.get()
        priority = self.entry_priority.get()
        
        if not data or not priority:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        try:
            priority = int(priority)
        except ValueError:
            messagebox.showerror("Erro", "Prioridade deve ser um número inteiro!")
            return
        
        self.queue.enqueue(data, priority)
        self.update_queue_display()
        self.entry_data.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)
    
    def dequeue(self):
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A fila está vazia.")
        self.update_queue_display()
    
    def update_queue_display(self):
        self.queue_display.delete(1.0, tk.END)
        queue_list = self.queue.print_queue()
        if not queue_list:
            self.queue_display.insert(tk.END, "Fila de prioridade está vazia.")
        else:
            for index, (data, priority) in enumerate(queue_list):
                if index == 0:
                    self.queue_display.insert(tk.END, f"Topo -> {data}, Prioridade: {priority}\n")
                elif index == len(queue_list) - 1:
                    self.queue_display.insert(tk.END, f"Base -> {data}, Prioridade: {priority}\n")
                else:
                    self.queue_display.insert(tk.END, f"        {data}, Prioridade: {priority}\n")

# Execução da interface gráfica
root = tk.Tk()
app = PriorityQueueGUI(root)
root.mainloop()
