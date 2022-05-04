# Undo/Redo implementation using Command pattern

#http://gernotklingler.com/blog/implementing-undoredo-with-the-command-pattern/

#----- the Command Interface -----
class ICommand:

    def __init__( self ):
        pass


    def execute( self ):
        pass


    def undo( self ):
        pass


    def redo( self ):
        pass

  
 
# ----- Undo/Redo Controller -----
 
class CommandManager:

    def __init__( self ):

        self.mUndoStack = []
        self.mRedoStack = []

 
    def executeCmd( self, command ):

        self.mRedoStack.clear()

        command.execute()
        self.mUndoStack.append( command )
 

    def undo( self ):

        if( len(self.mUndoStack) <= 0 ):
            return

        command = self.mUndoStack.pop() # remove top entry from undo stack
        command.undo()                  # undo most recently executed command
        self.mRedoStack.append( command ) # add undone command to undo stack

  
    def redo( self ):

        if( len(self.mRedoStack) <= 0 ):
            return
    
        command = self.mRedoStack.pop() # remove top entry from redo stack
        command.redo()                  # redo most recently executed command
        self.mUndoStack.append( command ) # add undone command to redo stack
