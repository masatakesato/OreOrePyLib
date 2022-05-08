from SinglyLinkedList import SinglyLinkedList
from DoublyLinkedList import DoublyLinkedList



if __name__ == '__main__':

    s = SinglyLinkedList()
    s.append(31)
    s.append(2)
    s.append(3)
    s.append(4)
 
    s.show()
    s.remove(31)
    s.remove(3)
    s.remove(2)
    s.show()

    d = DoublyLinkedList()
 
    d.append(5)
    d.append(6)
    d.append(50)
    d.append(30)
 
    d.show()
 
    d.remove(50)
    d.remove(5)
 
    d.show()