import tkinter as tk
from tkinter import simpledialog, messagebox

class DynamicStack:
    def __init__(self, initial_size):
        self.itens = []
        self.size_max = initial_size  

    def push(self, item): 
        # Tenta converter para float, mas se não for possível, mantém o item como está
        try:
            item = float(item)  # Converte o item para float se for um número
        except ValueError:
            pass  # Mantém o item como string se não for um número

        if self.is_full():
            self.resize()  # Redimensiona a pilha quando cheia
        self.itens.append(item)
        print(f"{item} foi adicionado à stack.")

    def pop(self): 
        if not self.is_empty():
            item = self.itens.pop()
            print(f"{item} foi removido da stack.")
            return item
        else:
            print("A stack está vazia.")
            return None

    def is_empty(self):
        return len(self.itens) == 0
    
    def is_full(self):
        return len(self.itens) == self.size_max  
    
    def resize(self):
        self.size_max *= 2  
        print(f"A stack foi redimensionada. Novo tamanho máximo: {self.size_max}")

    def peek(self):
        if not self.is_empty():
            return self.itens[-1]
        else:
            return None

    def size(self):
        return len(self.itens)
    
    def print_stack(self):
        if self.is_empty():
            print("A stack está vazia.")
            return []
        
        stack_list = []
        for i in range(len(self.itens)-1, -1, -1):
            stack_list.append(self.itens[i])
        return stack_list

    # Função de ordenação da pilha
    def sort_stack(self):
        def custom_sort(item):
            # Prioriza strings e numera como float
            if isinstance(item, str):
                return (0, item)  # Strings têm prioridade
            return (1, item)  # Números são secundários

        self.itens.sort(key=custom_sort) 
        print("A stack foi ordenada.")

# Interface com Tkinter
class DynamicStackGUI:
    def __init__(self, root, stack):
        self.stack = stack  
        self.root = root
        self.root.title("Pilha Dinâmica: ")
        
        self.label_data = tk.Label(root, text="Elemento:")
        self.label_data.grid(row=1, column=0)
        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=1, column=1)
        
        self.button_push = tk.Button(root, text="Adicionar na Pilha", command=self.push)
        self.button_push.grid(row=2, column=0, columnspan=2)
        
        self.button_pop = tk.Button(root, text="Remover da Pilha", command=self.pop)
        self.button_pop.grid(row=3, column=0, columnspan=2)
        
        self.button_sort = tk.Button(root, text="Ordenar a Pilha", command=self.sort_stack)
        self.button_sort.grid(row=4, column=0, columnspan=2)
        
        self.stack_display = tk.Text(root, height=10, width=30)
        self.stack_display.grid(row=5, column=0, columnspan=2)
        
        self.update_stack_display()
    
    def push(self):
        data = self.entry_data.get()
        
        if not data:
            messagebox.showerror("Erro", "Preencha o campo de elemento!")
            return
        
        self.stack.push(data)
        self.update_stack_display()
        self.entry_data.delete(0, tk.END)

    def pop(self):
        removed = self.stack.pop()
        if removed is not None:
            messagebox.showinfo("Removido", f"Elemento removido: {removed}")
        else:
            messagebox.showwarning("Aviso", "A pilha está vazia.")
        self.update_stack_display()

    def sort_stack(self):
        self.stack.sort_stack()
        self.update_stack_display()
    
    def update_stack_display(self):
        self.stack_display.delete(1.0, tk.END)
        stack_list = self.stack.print_stack()
        if not stack_list:
            self.stack_display.insert(tk.END, "A pilha está vazia.")
        else:
            for index, data in enumerate(stack_list):
                if index == 0:
                    self.stack_display.insert(tk.END, f"Topo -> {data}\n")
                elif index == len(stack_list) - 1:
                    self.stack_display.insert(tk.END, f"Base -> {data}\n")
                else:
                    self.stack_display.insert(tk.END, f"        {data}\n")

# Criação da pilha e da interface
ds = DynamicStack(5)

# Criação da interface
root = tk.Tk()
app = DynamicStackGUI(root, ds)
root.mainloop()
