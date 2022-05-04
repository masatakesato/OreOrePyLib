from CommandManager import ICommand, CommandManager


# Undo/Redo implementation using Command pattern

#http://gernotklingler.com/blog/implementing-undoredo-with-the-command-pattern/


 

# ----- the MODEL -----
class Tv:

    def __init__( self ):

        self.mOn = None
        self.mChannel = None
 

    def switchOn( self ):
        self.mOn = True


    def switchOff( self ):
        self.mOn = False

  
    def switchChannel( self, channel ):
        self.mChannel = channel

  
    def isOn( self ):
        return self.mOn
  
  
    def getChannel( self ):
        return self.mChannel
 
 
# ----- concrete ICommand commands -----
class TvOnCommand(ICommand):

    def __init__( self, tv ):
        super(TvOnCommand, self).__init__()

        self.mTv = tv
 

    def execute( self ):
        self.mTv.switchOn()


    def undo( self ):
        self.mTv.switchOff()


    def redo( self ):
        self.self.mTv.switchOn()



 
class TvOffCommand(ICommand):

    def __init__( self, tv ):
      super( TvOffCommand, self ).__init__()

      self.mTvOnCommand = TvOnCommand(tv)# reuse complementary command


    def execute( self ):
        self.mTvOnCommand.undo()


    def undo( self ):
        self.mTvOnCommand.execute()


    def redo( self ):
        self.mTvOnCommand.undo()


 
 
class TvSwitchChannelCommand(ICommand):

    def __init__( self, tv, channel ):
        super( TvSwitchChannelCommand, self ).__init__()

        self.mTv = tv
        self.mOldChannel = None
        self.mNewChannel = channel

 
    def execute( self ):
        self.mOldChannel = self.mTv.getChannel()
        self.mTv.switchChannel( self.mNewChannel ) 

 
    def undo( self ):
        self.mTv.switchChannel( self.mOldChannel )

 
    def redo( self ):
        self.mTv.switchChannel( self.mNewChannel )

 
 

if __name__ == '__main__':

    tv = Tv()
    commandManager = CommandManager()
 
    # create command for switching to channel 1
    c1 = TvSwitchChannelCommand(tv, 1)
    commandManager.executeCmd(c1)
    print( "switched to channel: " + str(tv.getChannel()) )
  
    # create command for switching to channel 2
    c2 = TvSwitchChannelCommand(tv, 2)
    commandManager.executeCmd(c2)
    print( "switched to channel: " + str(tv.getChannel()) )
  
    # create command for switching to channel 3
    c3 = TvSwitchChannelCommand(tv, 3)
    commandManager.executeCmd(c3)
    print( "switched to channel: " + str(tv.getChannel()) )
  
    print( "undoing..." )
    commandManager.undo()
    print( "current channel: " + str(tv.getChannel()) )
  
    print( "undoing..." )
    commandManager.undo()
    print( "current channel: " + str(tv.getChannel()) )
  
    print( "redoing..." )
    commandManager.redo()
    print( "current channel: " + str(tv.getChannel()) )
  
    print( "redoing..." )
    commandManager.redo()
    print( "current channel: " + str(tv.getChannel()) )
 
