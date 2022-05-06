import bpy

def draw( self, context ):
    self.layout.label( text="TEST" )

bpy.context.window_manager.popup_menu( draw, title="TestPopup", icon="INFO")