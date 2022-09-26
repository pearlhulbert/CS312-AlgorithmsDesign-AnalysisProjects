# Creating the Node class
class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None


# Create a circular doubly linked list class to initialize head and tail references
class CircleDoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def getHead(self):
        return self.head

    # Function to create Circular Doubly Linked List
    def insertTail(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
            self.head.prev = self.tail
            return
        last_node = self.head
        while last_node.next is not self.head:
            last_node = last_node.next
        last_node.next = new_node
        new_node.prev = last_node
        self.tail = new_node
        self.tail.next = self.head
        self.head.prev = self.tail

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next
            if node == self.tail.next:
                break

    def getSize(self):
        size = 0
        for _ in self:
            size += 1
        return size

    def makeList(self):
        cdllToList = []
        for el in self:
            cdllToList.append(el.value)
        return cdllToList