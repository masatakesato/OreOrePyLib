import sip
import traceback
import functools
from enum import IntEnum

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import *



g_DataChangedSymbol = { False: '', True: '*' }


class MouseMode(IntEnum):

    DoNothing = -1

    # QGraphicsScene's item operation
    DrawEdge = 0
    MoveNode = 1
    MoveGroup = 2
    MoveGroupIO = 3
    MoveSymbolicLink = 4
    RemoveSymbolicLink = 5

    # QGraphicsView's operation    
    RubberBandSelection = 6
    MoveViewport = 7

    # Other operations
    ContextMenu = 8



#http://www.qtcentre.org/threads/35221-Child-GraphicsItems-Not-Getting-itemChange()
#itemChangeは親アイテムに対して相対変化起こった場合だけ動く。Group→SymbolicLink→Portの場合、グループをマウス移動させてもSymbolicLinkのitemChangeは呼ばれない

# Commands
g_RemoveNodeCommand = 'RemoveNodeByID'
g_ConnectCommand = 'ConnectByID'
g_DisconnectCommand = 'DisconnectByID'
g_SelectCommand = 'SelectByID'
g_DeleteCommand = 'DeleteByID'
g_GroupCommand = 'GroupByID'
g_UngroupCommand = 'UngroupByID'
g_EditGroupCommand = 'EditGroupByID'
g_SetTranslationCommand = 'TranslateByID'

g_CreateSymbolicLinkCommand = 'CreateSymbolicLinkByID'
#g_RemoveSymbolicLinkCommand = 'RemoveSymbolicLinkByID'
g_SetSymbolicLinkSlotIndexCommand = 'SetSymbolicLinkSlotIndexByID'


# Label Graphics Settings
g_LabelFont = QFont('Times', 9.0)


# Background Graphics Settings
g_GridStep = 50


# Port Graphics Settings
g_PortDepth = 2
g_PortRadius = 7.5
g_PortFrameWidth = 1.75

g_PortColor = [ QColor(150, 200, 100), QColor(80,90,75) ] 
g_PortFrameColor = QColor(32,32,32)


# http://stackoverflow.com/questions/34429632/resize-a-qgraphicsitem-with-the-mouse QGraphicsItemの大きさをマウスで調整


# Commonn Settings
g_TitlebarHeight = 25
g_AttribAreaHeight = 25
g_LabelMargin = 10
g_LabelColor = QColor(255,255,255)
g_WidthMargin = 5
g_HeightMargin = 5
g_BoxRoundRadius = 5


# Edge Graphics Settings
g_EdgeWidth = 2.0
g_EdgeDepth = -1000
g_EdgeColor = [ QColor(164, 128, 100), QColor(255,127,39) ]
g_EdgeCollisionWidth = 10


# Node Graphics Settings
g_NodeDepth = 1
g_NodeMinWidth = 100 + g_WidthMargin * 2
g_NodeMinHeight = g_TitlebarHeight + g_HeightMargin
g_NodeFrameColor = [ QColor(32,32,32), QColor(255,127,39) ]
g_NodeFrameWidth = 1.25
g_NodeShadowColor = QColor(32, 32, 32)


# Group Graphics Settings
g_GroupMinWidth = 120 + g_WidthMargin * 2
g_GroupMinHeight = g_TitlebarHeight + g_HeightMargin
g_GroupFrameWidth = 1.5


# SymbolicLink Graphics Settings
g_ArrowHeight = 20.0
g_ArrowWidth = 80.0
g_ArrowLength = 10.0
g_ArrowColor = QColor(120,100,64)
g_ArrowFrameColor = [ QColor(32,32,32), QColor(255,127,39) ]
g_ArrowFrameWidth = 1.25


# GroupIO Graphics Settings
g_SlotHeight = g_ArrowHeight + 10.0
g_GroupIOWidth = 150.0
g_GroupIOFrameWidth = 1.25


# PushButton Graphics Settings
g_ButtonSize = 16
g_ButtonRoundRadius = 3
g_ButtonFrameColor = [ QColor(48,48,48), QColor(32,32,32) ]
g_ButtonFrameWidth = 1.0