# http://ls.pwd.io/2014/08/singly-and-doubly-linked-lists-in-python/

class Node(object):
 
    def __init__(self, data, next):
        self.data = data
        self.next = next
 
 
class SinglyLinkedList(object):
 
    head = None
    tail = None
 
    def show(self):
        print( 'Showing list data:' )
        current_node = self.head
        while current_node is not None:
            print( current_node.data, '->', end=' ' )
            current_node = current_node.next
        print( '' )
 
    def append(self, data):
        node = Node(data, None)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
        self.tail = node
 
    def remove(self, node_value):
        current_node = self.head
        previous_node = None
        while current_node is not None:
            if current_node.data == node_value:
                # if this is the first node (head)
                if previous_node is not None:
                    previous_node.next = current_node.next
                else:
                    self.head = current_node.next
 
            # needed for the next iteration
            previous_node = current_node
            current_node = current_node.next
 
