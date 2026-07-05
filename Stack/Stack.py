import typing

class StackNode:
    def __init__(self, data):
        self.data = data
        self.next: typing.Any = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        popped = self.top.data
        self.top = self.top.next
        return popped

    def display(self):
        if self.top is None:
            print("Riwayat penanganan kosong.")
            return
        temp = self.top
        print("Riwayat Penanganan Terakhir (LIFO):")
        while temp:
            print(f"- {temp.data}")
            temp = temp.next