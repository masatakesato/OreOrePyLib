mylist  = [ 'a','b','c','d','e' ]
myorder = [  3,  2,  0,  1,  4  ]

print( "original list..." )
print( mylist, "\n" )

print( "specified order..." )
print( myorder, "\n\n" )


print( "reordered list..." )
resultlist = [ x for _,x in sorted(zip(myorder, mylist)) ]
print( resultlist, "\n" )

