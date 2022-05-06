import threading


import bpy

def DoPopup():
    def draw( self, context ):
        self.layout.label( text="TEST" )

    bpy.context.window_manager.popup_menu( draw, title="TestPopup", icon="INFO")


thread1 = threading.Thread( target= DoPopup)

thread1.start()
thread1.join()