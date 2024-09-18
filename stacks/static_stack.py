import tkinter as tk
from tkinter import messagebox

class StaticStack:
    def __init__(self, max_size):
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        if not self.is_full():
            # Tenta converter o item para float, se não for um número mantém como string
            try:
                item = float(item)
            except ValueError:
                pass  # Mantém como string se não puder ser convertido

            self.items.append(item)
            print(f"{item} foi adicionado à stack.")
        else:
            print("A stack está cheia.")

    def pop(self):
        if not self.is_empty():
            item = self.items.pop()
            print(f"{item} foi removido da stack.")
            return item
        else:
            print("A stack está vazia.")
            return None

    def is_empty(self):
        return len(self.items) == 0
    
    def is_full(self):
        return len(self.items) == self.max_size

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def size(self):
        return len(self.items)

    def get_stack(self):
        return self.items[::-1]  # Retorna uma cópia invertida da pilha para mostrar o topo primeiro
    
    def sort_stack(self):  # Renomeando para sort_stack
        if self.is_empty():
            return
        
        # Tenta converter os dados para inteiros, se não conseguir, mantém como string
        def convert(item):
            try:
                return int(item)
            except ValueError:
                return item
        
        # Ordena priorizando números antes de strings
        self.items.sort(key=lambda x: (isinstance(convert(x), str), convert(x)))

    
    
class StaticStackGUI:    
    def __init__(self, root, max_size):
        self.stack = StaticStack(max_size)  
        self.root = root
        self.root.title("Pilha Estática: ")
        
        self.label_max_size = tk.Label(root, text=f"Tamanho máximo da pilha: {self.stack.max_size}")
        self.label_max_size.grid(row=0, column=0, columnspan=2)
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=1, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=1, column=1)
        
        self.button_push = tk.Button(root, text="Inserir na Pilha", command=self.push)
        self.button_push.grid(row=2, column=0, columnspan=2)
        
        self.button_pop = tk.Button(root, text="Remover da Pilha", command=self.pop)
        self.button_pop.grid(row=3, column=0, columnspan=2)
        
        self.button_sort = tk.Button(root, text="Ordenar a Pilha", command=self.sort_stack)
        self.button_sort.grid(row=4, column=0, columnspan=2)
    
        self.stack_display = tk.Text(root, height=10, width=30)
        self.stack_display.grid(row=5, column=0, columnspan=2)
        
        self.update_stack_display()
        self.update_buttons_visibility()
    
    def push(self):
        data = self.entry_data.get()
        
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        self.stack.push(data)
        self.update_stack_display()
        self.entry_data.delete(0, tk.END)
        
        self.update_buttons_visibility()

    def pop(self):
        removed = self.stack.pop()
        if removed:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A pilha está vazia.")
        
        self.update_stack_display()
        self.update_buttons_visibility()

    def sort_stack(self):
        if not self.stack.is_empty():
            self.stack.sort_stack()  
            self.update_stack_display()

    def update_stack_display(self):
        self.stack_display.delete(1.0, tk.END)
        stack_list = self.stack.get_stack()
        if not stack_list:
            self.stack_display.insert(tk.END, "Pilha estática está vazia.")
        else:
            for index, data in enumerate(stack_list):
                if index == 0:
                    self.stack_display.insert(tk.END, f"Topo -> {data}\n")
                elif index == len(stack_list) - 1:
                    self.stack_display.insert(tk.END, f"Base -> {data}\n")
                else:
                    self.stack_display.insert(tk.END, f"        {data}\n")
    
    def update_buttons_visibility(self):
        if self.stack.is_empty():
            self.button_pop.grid_remove()
            self.button_sort.grid_remove()
        else:
            self.button_pop.grid()
            self.button_sort.grid()
        
        if self.stack.is_full():
            self.button_push.grid_remove()
        else:
            self.button_push.grid()

# Criação da pilha e da interface
root = tk.Tk()
app = StaticStackGUI(root, 5)
root.mainloop()
