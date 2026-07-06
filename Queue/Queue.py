import time
import typing

class NodeQueue:
    def __init__(self, data):
        self.data = data 
        self.next = None 

class Queue:
    def __init__(self):
        self.front = None 
        self.rear = None 
        self._size = 0
    
    def isEmpty(self):
        return (self.front is None)

    def enqueue(self, data):
        node = NodeQueue(data)
        if self.isEmpty():
            self.front = node
            self.rear = node
        else:
            self.rear.next = node   #type: ignore
            self.rear = node
        self._size += 1

    def dequeue(self):
        if self.isEmpty():
            return None
        
        node = self.front
        self.front = self.front.next #type: ignore
        self._size -= 1

        if self.isEmpty():
            self.rear = None 

        return node.data             #type: ignore
    
    def peek(self):
        return self.front.data if self.front else None #type: ignore
    
    def size(self):
        return self._size
    
    def display(self):
        if self.isEmpty():
            print("Queue is empty || Antrian Kosong || Size: 0")
            return
        
        current = self.front
        idx = 0
        while current:
            p = current.data #type: ignore
            print(f"Index: {idx} || Data: {p} || Size: {self._size}")
            current = current.next #type: ignore
            idx += 1

"""
## TESTING ALGORITHM

def main():
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    queue.display()

    print("Dequeue:", queue.dequeue())
    queue.display()

    print("Peek:", queue.peek())
    print("Size:", queue.size())

if __name__ == "__main__":
    main()
"""
