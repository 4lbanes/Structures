class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, key):
        # Adiciona o novo elemento ao final do heap
        self.heap.append(key)
        # Mantém a propriedade do min-heap ajustando o heap
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            print("Heap está vazio")
            return
        
        # Armazena o menor elemento (raiz)
        min_elem = self.heap[0]
        
        # Move o último elemento para a raiz e remove o último elemento
        last_elem = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = last_elem
            # Ajusta o heap
            self._heapify_down(0)
        
        return min_elem

    def get(self, index):
        if index < 0 or index >= len(self.heap):
            print("Índice fora dos limites")
            return
        
        return self.heap[index]

    def get_min(self):
        if len(self.heap) == 0:
            raise IndexError("Heap está vazio")
        return self.heap[0]

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            # Troca o elemento com seu pai
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            # Continua ajustando o heap
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index
        
        # Verifica se o filho da esquerda é menor que o nó atual
        if (left_child_index < len(self.heap) and 
                self.heap[left_child_index] < self.heap[smallest]):
            smallest = left_child_index

        # Verifica se o filho da direita é menor que o nó atual
        if (right_child_index < len(self.heap) and 
                self.heap[right_child_index] < self.heap[smallest]):
            smallest = right_child_index

        # Se o menor não for o nó atual, troca e ajusta o heap
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def __str__(self):
        return str(self.heap)

# Teste do MinHeap
if __name__ == "__main__":
    min_heap = MinHeap()
    
    print("Inserindo elementos:")
    for value in [10, 20, 5, 6, 1, 8]:
        min_heap.insert(value)
    
    print(min_heap)
    
    print("\nObtendo valor no índice 3:")
    print(min_heap.get(3))  # Testando o método get
    
    print("\nExtraindo elementos:")
    while len(min_heap.heap) > 0:
        min_val = min_heap.extract_min()
        print(f"Extraído {min_val}")
        print(min_heap)
