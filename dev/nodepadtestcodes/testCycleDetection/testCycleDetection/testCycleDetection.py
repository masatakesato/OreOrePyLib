#import sys
#from datetime import datetime



#def test_graph(n):
#    """Return an acyclic graph containing 2**n simple paths."""
#    g = dict()
#    for i in range(n):
#        g[3 * i] = (3 * i + 1, 3 * i + 2)
#        g[3 * i + 1] = g[3 * i + 2] = (3 * (i + 1),)
#    return g




#def cyclic(g):
#    """Return True if the directed graph g has a cycle.
#    g must be represented as a dictionary mapping vertices to
#    iterables of neighbouring vertices. For example:

#    >>> cyclic({1: (2,), 2: (3,), 3: (1,)})
#    True
#    >>> cyclic({1: (2,), 2: (3,), 3: (4,)})
#    False

#    """
#    path = set()
#    visited = set()

#    def visit(vertex):
#        if vertex in visited:
#            return False
#        visited.add(vertex)
#        path.add(vertex)
#        for neighbour in g.get(vertex, ()):
#            if neighbour in path or visit(neighbour):
#                return True
#        path.remove(vertex)
#        return False

#    return any(visit(v) for v in g)



##sys.setrecursionlimit(100000000)

#print( 'Recursion depth =', sys.getrecursionlimit() )

##for i in range(2000, 2001):
##    print(i, timeit.timeit(lambda:cyclic(test_graph(i)), number=1))


#for i in range(0, 10):

#    #test_graph(600000)# 600,000ノードで実験

#    t1 = datetime.now()

#    #for i in range(10, 20):
#    g = test_graph(1600)
#    cyclic(g)

#    t2 = datetime.now()

#    diff = t2 - t1

#    print ( "elapsed_time: " + str(diff.microseconds * 0.001) + "[ms]" )




#https://gist.github.com/mikofski/6262755

"""
`Topological sort by Kahn (1962) on Wikipedia
<http://en.wikipedia.org/wiki/Topological_sorting>`_
L ← Empty list that will contain the sorted elements
S ← Set of all nodes with no incoming edges
while S is non-empty do
    remove a node n from S
    insert n into L
    for each node m with an edge e from n to m do
        remove edge e from the graph
        if m has no other incoming edges then
            insert m into S
if graph has edges then
    return error (graph has at least one cycle)
else 
    return L (a topologically sorted order)
"""

class CircularDependencyError(Exception):
    def __init__(self, keys):
        self.args = keys
        self.message = self.__str__
    def __str__(self):
        return 'Not a DAG. These keys are cyclic:\n\t%s' % str(self.args)


def topological_sort(DAG):
    """
    Kahn ('62) topological sort.

    :param DAG: directed acyclic graph
    :type DAG: dict
    """
    L = []
    S = [k for k, v in DAG.items() if not v]
    while S:
        n = S.pop(0)
        L.append(n)
        for m in (k for k, v in DAG.items() if n in v):
            # idx = DAG[m].index(n); DAG[m].pop(idx)  # Python < 2.7 alternative
            DAG[m] = list(set(DAG[m]).difference([n]))
            if not DAG[m]:
                S.append(m)
    if any([bool(v) for v in DAG.values()]):
        raise CircularDependencyError([k for k, v in DAG.items() if v])
    return L


if __name__ == "__main__":
    # test DAG
    DAG = {'7': [], '5': [], '3': [], '11': ['7', '5'], '8': ['7', '3'],
           '2': ['11'], '9': ['11', '8'], '10': ['11', '3']}
    print( topological_sort(DAG.copy()) )
    
    # test 10->9->8 circular dependency
    notDAG = {'7': [], '5': [], '3': [], '11': ['7', '5'], '8': ['7', '3', '10'],
              '2': ['11'], '9': ['11', '8'], '10': ['11', '3', '9']}
    print( topological_sort(notDAG.copy()) )
