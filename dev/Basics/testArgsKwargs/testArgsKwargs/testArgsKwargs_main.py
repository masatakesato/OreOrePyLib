#class A():

#    def __init__( self ):
#        self.func_dic = { 'func1': self.func1, 'func2': self.func2, 'func3': self.func3 }

#    def CallbackFunc( self, func_name, *args, **kwargs ):
#        self.func_dic[ func_name ](*args, **kwargs)

#    def func1( self, a ):
#        print( 'func1' )
#        print( a )


#    def func2( self, a, *, b=3, nn=5 ):
#        print( 'func2' )
#        print( a, b, nn )


#    def func3( self, a, b, c ):
#        print( 'func3' )
#        print( a, b, c )



#a = A()
#a.CallbackFunc('func1', 2 )
#a.CallbackFunc('func2', 2, nn=4, b=0.333 )






class SelectionList:

    def __init__( self ):
        self.__m_Selection_list = []
        self.__m_Changed = False


    def Exec( self, *args, **kwargs ):

        obj_ids = [ arg for arg in args if type(arg)==str ]
 
        if( 'add' in kwargs ):# add
            if( kwargs['add']==True ):
                self.__Add( obj_ids )

        elif( 'delete' in kwargs ):# delete
            if( kwargs['delete']==True ):
                self.__Delete( obj_ids )

        elif( 'clear' in kwargs ):# clear
            if( kwargs['clear']==True ):
                self.__Clear( obj_ids )

        else:# no option specified
            self.__Add( obj_ids )


    def Iter( self ):
        return iter(self.__m_Selection_list)


    def Print( self ):
        print( 'SelectionList:', self.__m_Selection_list )
        print( 'Changed:', self.__m_Changed )


    def __Add( self, object_ids ):
        len_before = len( self.__m_Selection_list )
        self.__m_Selection_list = list( dict.fromkeys( self.__m_Selection_list + object_ids ) )
        len_after = len( self.__m_Selection_list )
        self.__m_Changed = len_before != len_after


    def __Delete( self, object_ids ):
        len_before = len( self.__m_Selection_list )
        self.__m_Selection_list = [ obj_id for obj_id in self.__m_Selection_list if not obj_id in object_ids ]
        len_after = len( self.__m_Selection_list )
        self.__m_Changed = len_before != len_after


    def __Clear( self, object_ids ):
        if( not self.__m_Selection_list ):
            self.__m_Changed = False
        else:
            self.__m_Selection_list.clear()
            self.__m_Selection_list = object_ids
            self.__m_Changed = True





if __name__=="__main__":

    #def select( *args, **kwargs ):
    #    print( args )
    #    print( kwargs )


    selected_objects = SelectionList()




    selected_objects.Exec( 'sphere1', 'sphere2', 'cube1', add=True )
    selected_objects.Print()

    selected_objects.Exec( 'cube2', 'cube3', 'cube4' )
    selected_objects.Print()

    selected_objects.Exec( 'cube1' )
    selected_objects.Print()

    selected_objects.Exec( 'cube1', 'sphere1', delete=True )
    selected_objects.Print()


    selected_objects.Exec( 'plane000', 'plane001', clear=True )
    selected_objects.Print()



    for id_ in selected_objects.Iter():
        print(id_)


    selected_objects.Print()


    selected_objects.Exec( 'cube1', clear=True )
    selected_objects.Print()

    selected_objects.Exec( 'cube1', clear=True )
    selected_objects.Print()