import time 
import typing

class NodeStack:
    def __init__(self, data):
        self.data = data
        self.next = None 

class Stack:
    def __init__(self):
        self.top = None 
        self._size = 0
    
    def isEmpty(self):
        return self.top is None
    
    def push(self, data):
        node = NodeStack(data)
        node.next = self.top    #type: ignore
        self.top = node
        self._size += 1
    
    def pop(self):
        if self.isEmpty():
            return None
        
        node = self.top
        self.top = self.top.next #type: ignore
        self._size -= 1

        return node.data         #type: ignore
    
    def peek(self):
        return self.top.data if self.top else None #type: ignore
    
    def size(self):
        return self._size
    
    def display(self):
        if self.isEmpty():
            print("Stack is empty || Tumpukan Kosong || Size: 0")
            return
        
        current = self.top
        idx = 0
        while current:
            p = current.data #type: ignore
            print(f"Index: {idx} || Data: {p} || Size: {self._size}")
            current = current.next #type: ignore
            idx += 1


##  TESTING STACK ALGORITHM

def main():
    stack = Stack()
    stack.push(10)
    stack.push(20)
    stack.push(30)
    stack.display()
    
    print("Peek:", stack.peek())
    
    print("Pop:", stack.pop())
    stack.display()
    
    print("Size:", stack.size())

if __name__ == "__main__":
    main()

            
    

    