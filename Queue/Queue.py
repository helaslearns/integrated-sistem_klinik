import typing

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next: typing.Any = None

class Queue:
    def __init__(self):
        self.front = self.rear = None

    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.rear is None:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def peek(self):
        return self.front.data if self.front else None

    def display(self):
        if self.front is None:
            print("Antrean registrasi kosong.")
            return
        temp = self.front
        print("Antrean Registrasi:")
        while temp:
            print(f" -> {temp.data.nama}", end="")
            temp = temp.next
        print()