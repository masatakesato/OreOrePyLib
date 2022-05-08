# http://ls.pwd.io/2014/08/singly-and-doubly-linked-lists-in-python/


class DLNode(object):
 
    prev = None
    next = None
 

    def insertBefore( self, node ):
        self.next = node
        self.prev = node.prev
        node.prev = self
        if(self.prev): self.prev.next=self


    def insertAfter( self, node ):
        self.next = node.next
        self.prev = node
        node.next = self
        if(self.next): self.next.prev=self


    def remove( self ):
        if(self.prev): self.prev.next = self.next
        if(self.next): self.next.prev = self.prev
        self.next = None
        self.prev = None


    def flip( self ):
        tmp = self.next
        self.next = self.prev
        self.prev = tmp


 
#class DoubleList(object):
 
#    head = None
#    tail = None
 
#    def append(self, data):
#        new_node = DLNode(data, None, None)
#        if self.head is None:
#            self.head = self.tail = new_node
#        else:
#            new_node.prev = self.tail
#            new_node.next = None
#            self.tail.next = new_node
#            self.tail = new_node
 
#    def remove(self, node_value):
#        current_node = self.head
 
#        while current_node is not None:
#            if current_node.data == node_value:
#                # if it's not the first element
#                if current_node.prev is not None:
#                    current_node.prev.next = current_node.next
#                    current_node.next.prev = current_node.prev
#                else:
#                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
#                    self.head = current_node.next
#                    current_node.next.prev = None
 
#            current_node = current_node.next
 
#    def show(self):
#        print( 'Show list data:' )
#        current_node = self.head
#        while current_node is not None:
#            print( current_node.prev.data, end=' <- ' ) if hasattr(current_node.prev, 'data') else None
#            print( current_node.data, end='' )
#            print( ' ->', current_node.next.data ) if hasattr(current_node.next, 'data') else None 
#            current_node = current_node.next
#        print('')

#        print( '*'*50 )
 