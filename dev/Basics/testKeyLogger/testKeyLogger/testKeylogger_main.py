from oreorepylib.logger.keylogger.keylogger import KeyLogger

  

def KeyDown( event ):
    print( "KeyDown" )
    return True


def KeyUp( event ):
    print( "KeyUp" )
    return True



def MouseLeftDown( event ):
    print( "MouseLeftDown" )
    return True


def MouseLeftUp( event ):
    print( "MouseLeftUp" )
    return True



def MouseRightDown( event ):
    print( "MouseRightDown" )
    return True


def MouseRightUp( event ):
    print( "MouseRightUp" )
    return True



def MouseMiddleDown( event ):
    print( "MouseMiddleDown" )
    return True


def MouseMiddleUp( event ):
    print( "MouseMiddleUp" )
    return True



def MouseWheel( event ):
    print( "MouseWheel", event.Wheel )
    return True




if __name__=="__main__":

    keylogger = KeyLogger()

    keylogger.BindKeyDown( KeyDown )
    keylogger.BindKeyUp( KeyUp )

    keylogger.BindMouseLeftDown( MouseLeftDown )
    keylogger.BindMouseLeftUp( MouseLeftUp )

    keylogger.BindMouseRightDown( MouseRightDown )
    keylogger.BindMouseRightUp( MouseRightUp )

    keylogger.BindMouseMiddleDown( MouseMiddleDown )
    keylogger.BindMouseMiddleUp( MouseMiddleUp )

    keylogger.BindMouseWheel( MouseWheel )

    keylogger.Start()
