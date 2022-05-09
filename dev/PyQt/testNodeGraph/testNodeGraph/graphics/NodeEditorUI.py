from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from common.NodeTypeManager import *
import graphics.stylesheet as StyleSheet

import functools



# Background Graphics Settings
g_GridStep = 50


# Port Graphics Settings
class PortFlow(IntEnum):
    In = 0
    Out = 1

g_PortDepth = 2
g_PortRadius = 7.5
g_PortFrameWidth = 1.75

g_PortColor = [QColor(150, 200, 100), QColor(80,90,75)] 
g_PortFrameColor = QColor(32,32,32)





# Edge Graphics Settings
class EdgeState(IntEnum):
    Default = 0
    Picked = 1

g_EdgeDepth = -1000
g_EdgeColor = [QColor(164, 128, 100), QColor(255,127,39)]
g_EdgeCollisionWidth = 10


# Node Graphics Settings

g_NodeDepth = 1
g_TitlebarHeight = 25
g_AttribAreaHeight = 25
g_LabelMargin = 13
g_HeightMargin = 5
g_WidthMargin = 5
g_NodeFrameColor = [QColor(32,32,32), QColor(255,127,39)]
g_NodeFrameWidth = 1.25
g_LabelColor = QColor(255,255,255)
g_NodeShadowColor = QColor(32, 32, 32)
g_BoxRoundRadius = 5




# Edge
class Edge(QGraphicsPathItem):

    def __init__( self, name, srcpoint, dstpoint ):

        super(Edge, self).__init__()

        self.__m_ObjectType = type(self).__name__
        self.__m_Name = name
        self.refSourcePort = None
        self.refDestPort = None
        self.sourcePoint = srcpoint # source point
        self.destPoint = dstpoint   # destination point
        
        self.setZValue(g_EdgeDepth)
        self.setFlags(QGraphicsItem.ItemIsSelectable)

        self.UpdatePath()
        

    def ConnectPort( self, sourceport, destport ):
        self.ConnectSourcePort( sourceport )
        self.ConnectDestPort( destport )

    def ConnectSourcePort( self, sourceport ):
        self.refSourcePort = sourceport
        self.SetSourcePosition(self.refSourcePort.scenePos())

    def ConnectDestPort( self, destport ):
        self.refDestPort = destport
        self.SetDestPosition(self.refDestPort.scenePos())


    def DisconnectPort( self ):
        self.refSourcePort = None
        self.refDestPort = None

    def DisconnectSourcePort(self):
        self.refSourcePort = None

    def DisconnectDestPort(self):
        self.refDestPort = None


    def SetSourcePosition(self, sourcepoint):
        #print("Edge::SetSourcePosition")
        self.sourcePoint = sourcepoint

    def SetDestPosition(self, destpoint):
        #print("Edge::SetDestPosition")
        self.destPoint = destpoint


    def UpdatePath(self):

        #print("Edge::UpdatePath")
        
        path = QPainterPath()
        dx = self.destPoint.x() - self.sourcePoint.x()
        ctrl1 = QPointF(self.sourcePoint.x() + dx * 0.5, self.sourcePoint.y())# + dy * 0.1)
        ctrl2 = QPointF(self.destPoint.x() - dx * 0.5, self.destPoint.y())# + dy * 0.9)
   
        path.moveTo(self.sourcePoint)
        path.cubicTo(ctrl1, ctrl2, self.destPoint)

        self.setPath(path)

    def ObjectType( self ):
        return self.__m_ObjectType


    def Name( self ):
        return self.__m_Name


    def Info( self ):
        print( "//------------- Edge " + self.__m_Name + " -------------//" )
        if( self.refSourcePort ):    print( "   Source Port: " + self.refSourcePort.Name() )
        if( self.refDestPort ):      print( "   Destination Port: " + self.refDestPort.Name() )


    ####################### QGraphicsItem func override ################################

    def shape( self ):
        
        stroker = QPainterPathStroker( )
        stroker.setWidth( g_EdgeCollisionWidth )
        return stroker.createStroke( self.path() )


    def paint(self, painter, option, widget):

        #print("Edge::paint")

        painter.setClipRect( option.exposedRect )
        painter.setPen(QPen(g_EdgeColor[int(self.isSelected())], 2.0))
        painter.drawPath(self.path())



# Temporary Edge
class TemporaryEdge(QGraphicsPathItem):

    def __init__(self, srcpoint, dstpoint):

        super(TemporaryEdge, self).__init__()

        self.setZValue(g_EdgeDepth)

        self.sourcePoint = srcpoint # source point
        self.destPoint = dstpoint   # destination point

        self.UpdatePath()


    def SetSourcePosition(self, sourcepoint):
        #print("TemporaryEdge::SetSourcePosition")
        self.sourcePoint = sourcepoint

    def SetDestPosition(self, destpoint):
        #print("TemporaryEdge::SetDestPosition")
        self.destPoint = destpoint


    def UpdatePath(self):

        #print("TemporaryEdge::UpdatePath")
        
        path = QPainterPath()
        dx = self.destPoint.x() - self.sourcePoint.x()
        ctrl1 = QPointF(self.sourcePoint.x() + dx * 0.5, self.sourcePoint.y())# + dy * 0.1)
        ctrl2 = QPointF(self.destPoint.x() - dx * 0.5, self.destPoint.y())# + dy * 0.9)
   
        path.moveTo(self.sourcePoint)
        path.cubicTo(ctrl1, ctrl2, self.destPoint)

        self.setPath(path)




    ####################### QGraphicsItem func override ################################

    #def shape( self ):
        
    #    stroker = QPainterPathStroker( )
    #    stroker.setWidth( g_EdgeCollisionWidth )
    #    return stroker.createStroke( self.path() )


    def paint(self, painter, option, widget):

        #print("Edge::paint")

        painter.setClipRect(option.exposedRect)
        painter.setPen( QPen(g_EdgeColor[int(self.isSelected())], 2.0, Qt.DotLine))
        painter.drawPath(self.path())



class Port(QGraphicsItem):

    def __init__(self, parent, name, portType):

        super(Port, self).__init__(parent)

        # attributes
        self.__m_Name = name
        self.__m_Flow = portType
        self.radius = g_PortRadius
        self.diam = self.radius * 2
        self.bb = QRectF( -self.diam, -self.diam, self.diam*2, self.diam*2 )

        self.path = QPainterPath()
        self.path.addEllipse( self.bb )

        self.__m_Pen = QPen(g_PortFrameColor, g_PortFrameWidth)


        # connected edges
        self.__m_ConnectedEdges = {}
        
        # temporary variables for connected edge.  (mouse drag operation)
        self.__m_TempEdge = None
        self.__m_CurrEndType = "none"


    def ConnectEdge( self, edge ):
        self.__m_ConnectedEdges[ edge.Name() ] = edge


    def DisconnectEdge( self, edge ):
        name = edge.Name()
        if name in self.__m_ConnectedEdges:
            self.__m_ConnectedEdges[ name ] = None
            del self.__m_ConnectedEdges[ name ]


    def UpdateEdgePath( self ):

        if( self.__m_Flow==PortFlow.In ):
            for edge in self.__m_ConnectedEdges.values():
                edge.SetDestPosition( self.scenePos() )
                edge.UpdatePath()
        else:
            for edge in self.__m_ConnectedEdges.values():
                edge.SetSourcePosition( self.scenePos() )
                edge.UpdatePath()


    def ConnectedEdges( self ):
        return self.__m_ConnectedEdges


    def Name( self ):
        return self.parentItem().Name() + '.' + self.__m_Name


    def ParentName( self ):
        return self.parentItem().Name()


    def LocalName( self ):
        return self.__m_Name



    def Info( self ):

        print( "  - " + self.__m_Name + " [" + str(self.__m_Flow) +  "] Connections:" )
        
        if( len(self.__m_ConnectedEdges) <= 0 ):
            print( "     None" )
        else:
            for edge in self.__m_ConnectedEdges.values():
                print( "     " + edge.Name() )


    ########################### QGraphicsItem func override ################################

    def boundingRect(self):
        return self.bb#return QRectF( self.bb.x()-5, self.bb.y()-5, self.bb.width()+10, self.bb.height()+10 )


    def shape(self):
        #path = QPainterPath()
        #path.addEllipse( self.bb )
        #return path
        return self.path


    def paint(self, painter, option, widget):
        
        #print("Port::paint")

        painter.setClipRect(option.exposedRect)
        painter.setPen(self.__m_Pen)
        painter.setBrush(g_PortColor[self.__m_Flow])
        painter.drawRoundedRect( -self.radius, -self.radius, self.diam, self.diam, self.radius, self.radius )


    def mousePressEvent(self, event):

        #print("Port::mousePressEvent")

        if(self.__m_Flow == PortFlow.In):
            
            self.__m_CurrEndType = "from"
            pos = self.scenePos()
            self.__m_TempEdge = TemporaryEdge( pos, pos )
            self.scene().addItem(self.__m_TempEdge)

        elif(self.__m_Flow == PortFlow.Out):

            self.__m_CurrEndType = "to"
            pos = self.scenePos()
            self.__m_TempEdge = TemporaryEdge( pos, pos )
            self.scene().addItem(self.__m_TempEdge)

        else:
            super(Port, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):

        #print("Port::mouseMoveEvent")

        currPort = self.scene().itemAt(event.scenePos(),QTransform())          
        scenepos = event.scenePos()
        if(isinstance(currPort, Port)):
            if((currPort.__m_Flow == PortFlow.In and self.__m_CurrEndType == "to") or (currPort.__m_Flow == PortFlow.Out and self.__m_CurrEndType == "from")):
                #print("snap edge.")
                scenepos = currPort.scenePos()

        if(self.__m_CurrEndType == "to"):
            self.__m_TempEdge.SetDestPosition(scenepos)
            self.__m_TempEdge.UpdatePath()

        elif(self.__m_CurrEndType == "from"):
            self.__m_TempEdge.SetSourcePosition(scenepos)
            self.__m_TempEdge.UpdatePath()

        else:
            super(Port, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):

        #print("Port::mouseReleaseEvent")

        if(self.__m_TempEdge == None):
            return super(Port, self).mouseReleaseEvent(event)

        currPort = self.scene().itemAt(event.scenePos(),QTransform())  
        if(isinstance(currPort, Port)):

            if(self.__m_CurrEndType == "from" and currPort.__m_Flow == PortFlow.Out):# connect output port

                self.scene().removeItem( self.__m_TempEdge )
                self.scene().ExecCommand( [ 'Connect', currPort.Name(), self.Name() ] ) #self.scene().Connect( currPort, self )

            elif(self.__m_CurrEndType == "to" and currPort.__m_Flow == PortFlow.In):# connect input port

                self.scene().removeItem( self.__m_TempEdge )
                self.scene().ExecCommand( [ 'Connect', self.Name(), currPort.Name() ] ) #self.scene().Connect( self, currPort )

            else:
                print("invalid port connection. removing edge.")
                self.scene().removeItem(self.__m_TempEdge)

        else:
            print("port is not specified. removing edge")
            self.scene().removeItem( self.__m_TempEdge )
            super(Port, self).mouseReleaseEvent(event)

        
        self.__m_CurrEndType = "none"
        self.__m_TempEdge = None
        



class Node(QGraphicsItem):

    def __init__(self, name, nodedesc ):

        super(Node, self).__init__()
        
        self.__m_ObjectType = nodedesc.ObjectType()
        self.__m_Name = name
        self.__Width = 100 + g_WidthMargin * 2
        self.__Height = g_TitlebarHeight + max( len( nodedesc.InputAttribDescs() ), len( nodedesc.OutputAttribDescs() ) ) * g_AttribAreaHeight + g_HeightMargin
        
        self.__m_BoundingRect = QRectF(-g_PortRadius, -g_PortRadius, self.__Width+g_PortRadius*2, self.__Height+g_PortRadius*2)
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( QRectF(0, 0, self.__Width, self.__Height) ) 
        self.__m_Pen = QPen( g_NodeFrameColor[0], 1.25 )


        self.gradient = QLinearGradient(0, 0, 0,g_TitlebarHeight)
        self.gradient.setColorAt(0, QColor(128,128,128))
        self.gradient.setColorAt(0.49999, QColor(60,60,60))
        self.gradient.setColorAt(0.5, QColor(32,32,32))
        self.gradient.setColorAt(0.99999, QColor(48,48,48))
        self.gradient.setColorAt(1.0, QColor(64,64,64))



        self.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemIsSelectable )


        # Node's Label
        label = QGraphicsSimpleTextItem( nodedesc.ObjectType(), self )#QGraphicsTextItem( nodedesc.ObjectType(), self)
        bR = label.sceneBoundingRect()
        label.setPos( (self.__Width - bR.width()) / 2, g_TitlebarHeight / 2 - bR.height() / 2)
        label.setBrush( g_LabelColor )#label.setDefaultTextColor( g_LabelColor )
        #label.setTextInteractionFlags(Qt.TextEditorInteraction)

        # Port UI
        self.__m_InputPorts = []
        self.__m_OutputPorts = []

        self.__m_InputDict = {}
        self.__m_OutputDict = {}


        # Create Input Port GraphicsItems
        descs = nodedesc.InputAttribDescs()
        for idx in range(len(descs)):
            self.__CreatePortAndLabelGraphicsItem( descs[idx].Name(), descs[idx].DataFlow(), idx )

        # Create Output Port GraphicsItems
        descs = nodedesc.OutputAttribDescs()
        for idx in range(len(descs)):
            self.__CreatePortAndLabelGraphicsItem( descs[idx].Name(), descs[idx].DataFlow(), idx )

        
        # DropShadow Effect......Heavy!!! causes access violation!!
        #effect = QGraphicsDropShadowEffect()
        #effect.setBlurRadius(1)
        #effect.setOffset(1,1)
        #effect.setColor( g_NodeShadowColor )
        #self.setGraphicsEffect(effect)


    def ObjectType( self ):
        return self.__m_ObjectType


    def InputPorts( self ):
        return self.__m_InputPorts


    def OutputPorts( self ):
        return self.__m_OutputPorts


    def InputPort( self, name ):
        if( name in self.__m_InputDict ):
            return self.__m_InputPorts[ self.__m_InputDict[name] ]
        return None


    def OutputPort( self, name ):
        if( name in self.__m_OutputDict ):
            return self.__m_OutputPorts[ self.__m_OutputDict[name] ]
        return None


    def __CreatePortAndLabelGraphicsItem( self, portName, dataFlow, idx ):

        # calc base y position
        posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)

        # create port object
        if( dataFlow==DataFlow.Input ):
            port = Port( self, portName, PortFlow.In )
            port.setPos( 0, posy )
            self.__m_InputDict[ portName ] = len( self.__m_InputPorts )
            self.__m_InputPorts.append( port )


        elif( dataFlow==DataFlow.Output ):
            port = Port( self, portName, PortFlow.Out )
            port.setPos( self.__Width, posy )
            self.__m_OutputDict[ portName ] = len( self.__m_OutputPorts )
            self.__m_OutputPorts.append( port )
  

        # create label graphics object
        label = QGraphicsSimpleTextItem( portName, self )
        label.setBrush( g_LabelColor )
        br = label.sceneBoundingRect()

        if( dataFlow==DataFlow.Input ):
            label.setPos( g_LabelMargin, posy - br.height()*0.5 )

        elif( dataFlow==DataFlow.Output ):
            label.setPos( self.__Width - g_LabelMargin - br.width(), posy - br.height()*0.5 )


    def SetName( self, name ):
        self.__m_Name = name


    def Name( self ):
        return self.__m_Name


    def Info( self ):
        print( "//------------- Node: " + self.__m_Name+ " -------------//" )
        
        for port in self.__m_InputPorts:
            port.Info()

        for port in self.__m_OutputPorts:
            port.Info()     



    ######################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        if( change == QGraphicsItem.ItemPositionHasChanged ):

            for edge in self.__m_InputPorts:
                edge.UpdateEdgePath()

            for edge in self.__m_OutputPorts:
                edge.UpdateEdgePath()

        elif( change == QGraphicsItem.ItemSelectedChange ):

            if( value == True ):
                self.setZValue( self.zValue() + 0.1 )
                self.__m_Pen.setColor(g_NodeFrameColor[1])
            else:
                self.setZValue( self.zValue() - 0.1 )
                self.__m_Pen.setColor(g_NodeFrameColor[0])


        return super(Node, self).itemChange( change, value )


    def boundingRect(self):
        return self.__m_BoundingRect#QRectF(-10, -10, self.__Width+20, self.__Height+20)


    def shape( self ):
        #path = QPainterPath()
        #path.addRect( self.__m_Shape )
        #return path
        return self.__m_Shape


    def paint(self, painter, option, widget):

        #print("Node::paint")

        painter.setClipRect(option.exposedRect)
        painter.setBrush(self.gradient)
        painter.setPen(self.__m_Pen)
        painter.drawRoundedRect(0, 0, self.__Width, self.__Height, g_BoxRoundRadius, g_BoxRoundRadius)










class Group(QGraphicsItem):

    def __init__(self, name, itemlist):

        super(Group, self).__init__()
        
        self.__m_Name= name
        self.__Width = 100 + g_WidthMargin * 2
        self.__Height = g_TitlebarHeight + 5 * g_AttribAreaHeight + g_HeightMargin
        
        self.__m_InitialPos = QPoint()
        self.__m_BoundingRect = QRectF(-g_PortRadius, -g_PortRadius, self.__Width+g_PortRadius*2, self.__Height+g_PortRadius*2)
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( QRectF(0, 0, self.__Width, self.__Height) ) 
        self.__m_Pen = QPen( g_NodeFrameColor[0], 1.25 )

        self.gradient = QLinearGradient(0, 0, 0,g_TitlebarHeight)
        self.gradient.setColorAt(0, QColor(128,128,128))
        self.gradient.setColorAt(0.49999, QColor(60,60,60))
        self.gradient.setColorAt(0.5, QColor(32,32,32))
        self.gradient.setColorAt(0.99999, QColor(48,48,48))
        self.gradient.setColorAt(1.0, QColor(64,64,64))

        self.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemIsSelectable )

        # Node's Label
        label = QGraphicsSimpleTextItem( 'Group: ' + name, self )
        bR = label.sceneBoundingRect()
        label.setPos( (self.__Width - bR.width()) / 2, g_TitlebarHeight / 2 - bR.height() / 2)
        label.setBrush( g_LabelColor )#label.setDefaultTextColor( g_LabelColor )
        #label.setTextInteractionFlags(Qt.TextEditorInteraction)

        # Inputs/Outpus
        self.__m_InputPorts = []
        self.__m_OutputPorts = []

        self.__m_InputDict = {}
        self.__m_OutputDict = {}


        self.__m_GroupInputDescs = []
        self.__m_GroupOutputDescs = []

        # Group Objects
        self.__m_Children = {}
        self.__m_InternalEdges = {}


        # Gather children
        for item in itemlist:
            if( isinstance( item, Edge)==False ): # ignore edges
                self.__m_InitialPos += item.scenePos()
                self.__m_Children[ id(item) ] = item
                item.setVisible(False)

        self.__m_InitialPos /= len(self.__m_Children)
        self.setPos( self.__m_InitialPos )



    def Children( self ):
        return self.__m_Children


    def CreateSymbolicLink( self ):

        in_idx = 0
        out_idx = 0

        # Detect internal connection
        for child in self.__m_Children.values():

            for port in child.InputPorts():

                bHasGroupInput = False
                reconnectionList = []

                for edge in port.ConnectedEdges().values(): # 入力コネクション群を調べる
                    
                    source_parent = edge.refSourcePort.parentItem()

                    if( id(source_parent) in self.__m_Children ): # グループ内部で閉じている接続を見つけた
                        self.__m_InternalEdges[ id(edge) ] = edge
                        edge.setVisible(False)

                    else:                                   # グループ外との接続コネクションを見つけた
                        bHasGroupInput = True
                        reconnectionList.append( edge )
 
                if( bHasGroupInput==True ):
                    symbolicLinkName = port.Name().replace('.', '_')
                    self.__CreatePortAndLabelGraphicsItem( symbolicLinkName, DataFlow.Input, in_idx )
                    in_idx += 1
                        
                    for edge in reconnectionList:
                        source_name = edge.refSourcePort.Name()
                        dest_name = self.Name() + '.' + symbolicLinkName
                        self.scene().Disconnect_Exec( edge.Name() )# reconnect ui only
                        self.scene().Connect_Exec( edge.Name(), source_name, dest_name )# reconnect ui only

            for port in child.OutputPorts():

                bHasGroupOutput = False
                reconnectionList = []

                for edge in port.ConnectedEdges().values(): # 出力コネクション群を調べる

                    dest_parent = edge.refDestPort.parentItem()

                    if( id(dest_parent) in self.__m_Children ): # グループ内部で閉じている接続を見つけた
                        pass
                    else:                                   # グループ外との接続コネクションを見つけた
                        bHasGroupOutput = True
                        reconnectionList.append( edge )

                if( bHasGroupOutput==True ):
                    symbolicLinkName = port.Name().replace('.', '_')
                    self.__CreatePortAndLabelGraphicsItem( symbolicLinkName, DataFlow.Output, out_idx )
                    out_idx += 1

                    for edge in reconnectionList:
                        source_name = self.Name() + '.' + symbolicLinkName
                        dest_name = edge.refDestPort.Name()
                        self.scene().Disconnect_Exec( edge.Name() )# reconnect ui only
                        self.scene().Connect_Exec( edge.Name(), source_name, dest_name )# reconnect ui only


    def Ungroup( self ):
        
        for port in self.__m_InputPorts:
            for edge in list(port.ConnectedEdges().values())[:]:
                if( not id(edge) in self.__m_InternalEdges ):
                    conn_name = edge.Name()
                    source_name = edge.refSourcePort.Name()

                    dest_names = port.Name().split('.')# '.'で分割して後ろ側の部分文字列を取得する
                    dest_name = dest_names[ len(dest_names)-1 ].replace('_', '.', 1)# child_port_nameの一番左端の'_'だけ'.'に置き換える
                    self.scene().Disconnect_Exec( edge.Name() )
                    self.scene().Connect_Exec( edge.Name(), source_name, dest_name )

        for port in self.__m_OutputPorts:
            for edge in list(port.ConnectedEdges().values())[:]:
                if( not id(edge) in self.__m_InternalEdges ):
                    conn_name = edge.Name()
                    dest_name = edge.refDestPort.Name()

                    source_names = port.Name().split('.')# '.'で分割して後ろ側の部分文字列を取得する
                    source_name = source_names[ len(source_names)-1 ].replace('_', '.', 1)# child_port_nameの一番左端の'_'だけ'.'に置き換える
                    self.scene().Disconnect_Exec( edge.Name() )
                    self.scene().Connect_Exec( edge.Name(), source_name, dest_name )


        vec = self.scenePos() - self.__m_InitialPos

        for k in self.__m_Children.keys():
            self.__m_Children[k].setVisible(True)
            self.__m_Children[k].setPos( self.__m_Children[k].scenePos() + vec )
            self.__m_Children[k] = None
            
        self.__m_Children.clear()


        for k in self.__m_InternalEdges.keys():
            edge = self.__m_InternalEdges[k]
            edge.setVisible(True)
            edge.UpdatePath()
           
            self.__m_InternalEdges[k] = None

        self.__m_InternalEdges.clear()


    def ObjectType( self ):
        return 'Group'


    def InputPorts( self ):
        return self.__m_InputPorts


    def OutputPorts( self ):
        return self.__m_OutputPorts


    def InputPort( self, name ):
        if( name in self.__m_InputDict ):
            return self.__m_InputPorts[ self.__m_InputDict[name] ]
        return None


    def OutputPort( self, name ):
        if( name in self.__m_OutputDict ):
            return self.__m_OutputPorts[ self.__m_OutputDict[name] ]
        return None



    def __CreatePortAndLabelGraphicsItem( self, portName, dataFlow, idx ):

        # calc base y position
        posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)

        # create port object
        if( dataFlow==DataFlow.Input ):
            port = Port( self, portName, PortFlow.In )
            port.setPos( 0, posy )
            self.__m_InputDict[ portName ] = len( self.__m_InputPorts )
            self.__m_InputPorts.append( port )


        elif( dataFlow==DataFlow.Output ):
            port = Port( self, portName, PortFlow.Out )
            port.setPos( self.__Width, posy )
            self.__m_OutputDict[ portName ] = len( self.__m_OutputPorts )
            self.__m_OutputPorts.append( port )
  

        # create label graphics object
        label = QGraphicsSimpleTextItem( portName, self )
        label.setBrush( g_LabelColor )
        br = label.sceneBoundingRect()

        if( dataFlow==DataFlow.Input ):
            label.setPos( g_LabelMargin, posy - br.height()*0.5 )

        elif( dataFlow==DataFlow.Output ):
            label.setPos( self.__Width - g_LabelMargin - br.width(), posy - br.height()*0.5 )


    def SetName( self, name ):
        self.__m_Name = name


    def Name( self ):
        return self.__m_Name


    def Info( self ):
        print( "//------------- Group: " + self.__m_Name+ " -------------//" )

        for child in self.__m_Children.values():
            child.Info()



    ######################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        if( change == QGraphicsItem.ItemPositionHasChanged ):

            for edge in self.__m_InputPorts:
                edge.UpdateEdgePath()

            for edge in self.__m_OutputPorts:
                edge.UpdateEdgePath()

        elif( change == QGraphicsItem.ItemSelectedChange ):

            if( value == True ):
                self.setZValue( self.zValue() + 0.1 )
                self.__m_Pen.setColor(g_NodeFrameColor[1])
            else:
                self.setZValue( self.zValue() - 0.1 )
                self.__m_Pen.setColor(g_NodeFrameColor[0])


        return super(Group, self).itemChange( change, value )


    def boundingRect(self):
        return self.__m_BoundingRect#QRectF(-10, -10, self.__Width+20, self.__Height+20)


    def shape( self ):
        #path = QPainterPath()
        #path.addRect( self.__m_Shape )
        #return path
        return self.__m_Shape


    def paint(self, painter, option, widget):

        #print("Node::paint")

        painter.setClipRect(option.exposedRect)
        painter.setBrush(self.gradient)
        painter.setPen(self.__m_Pen)
        painter.drawRoundedRect(0, 0, self.__Width, self.__Height, g_BoxRoundRadius, g_BoxRoundRadius)















class NodeEditorUI(QGraphicsScene):

    def __init__(self, parent=None):

        super(NodeEditorUI, self).__init__(parent)
        
        self.setItemIndexMethod( QGraphicsScene.NoIndex )

        self.__m_pSceneManager = None
        self.__m_pNodeTypeManager = None

        # pointers
        self.__m_Nodes = {} # key: name, val: Node
        self.__m_Edges = {} # key: name, val: Edge

        self.selectionChanged.connect( self.SelectionChanged_Exec )



    def SelectionChanged_Exec( self ):

        print('selectionChanged...')

        item_name = '-clear'

        if( len( self.selectedItems() )>0 ):
            self.selectedItems()[0].Info()
            item_name = self.selectedItems()[0].Name()

        self.__m_pSceneManager.Select_Exec( ['Select', item_name ])

            #        # send node selection info only
            #item = self.selectedItems()[0]
            #if( isinstance( item, Node )==True ):
            #    self.__m_pSceneManager.Select_Exec( ['Select', item.Name() ])

        #for item in self.selectedItems():
        #    print( item.ObjectType() )


        


    #====================== Setup ==========================#

    def BindSceneManager( self, sceneManager ):
        self.__m_pSceneManager = sceneManager
        self.__m_pNodeTypeManager = self.__m_pSceneManager.NodeTypeManager()


    def UnbindSceneManager( self ):
        self.__m_pSceneManager = None
        self.__m_pNodeTypeManager = None



    #=============== Command functions ================#
    def ExecCommand( self, commandbuffer ):

        self.__m_pSceneManager.ExecCommand( commandbuffer )



    def CreateNode_Exec( self, node_name, nodetype, posx, posy ):

        self.CreateNode( node_name, nodetype, posx, posy )


    def RemoveNode_Exec( self, node_name ):
        
        self.RemoveNode( self.__m_Nodes[ node_name ] )


    def Connect_Exec( self, conn_name, source_name, dest_name ):
        
        src_nodename, src_portname = source_name.split('.')
        dst_nodename, dst_portname = dest_name.split('.')

        self.Connect( conn_name,
                     self.__m_Nodes[ src_nodename ].OutputPort( src_portname ),
                     self.__m_Nodes[ dst_nodename ].InputPort( dst_portname ) )


    def Disconnect_Exec( self, edge_name ):

        if( not(edge_name in self.__m_Edges) ):
            print( edge_name + ' does not exist on NodeEditorUI' )
            return False

        self.Disconnect( self.__m_Edges[ edge_name ] )
        return True


    def Rename_Exec( self, currname, newname ):

        if( not(currname in self.__m_Nodes) ):
            return False

        node = self.__m_Nodes[ currname ]
        node.SetName( newname )
        self.__m_Nodes[ node.Name() ] = self.__m_Nodes.pop( currname )

        return True


    def Group_Exec( self, group_name, obj_name_lsit ):
        
        selectedItems = []
        for name in obj_name_lsit:
            if( name in self.__m_Nodes ):
                selectedItems.append( self.__m_Nodes[ name ] )

        if( len(selectedItems) < 1 ):
            return False

        group = Group( group_name, selectedItems )
        self.__m_Nodes[ group.Name() ] = group
        self.addItem( group )

        group.CreateSymbolicLink()

        return True


    def Ungroup_Exec( self, group_name ):

        group = self.__m_Nodes[ group_name ]
        group.Ungroup()
        self.removeItem( group )
        del group

    
    def GatherRemoveCandidateConnections( self, node_name ):

        conn_list = []

        if( not(node_name in self.__m_Nodes) ):
            return None

        node = self.__m_Nodes[ node_name ]

        # gather edge name from input ports. pickup unselected edges only.
        for port in node.InputPorts():
            for edgekey in port.ConnectedEdges().keys():
                conn_list.append( edgekey )

        # gather edge name from output ports. pickup unselected edges only.
        for port in node.OutputPorts():
            for edgekey in port.ConnectedEdges().keys():
                conn_list.append( edgekey )

        return conn_list



    #================ Scene Edit Functions =================#

    def Connect( self, conn_name, source_port, dest_port ):

        # create edge object
        edge = Edge( conn_name, source_port.scenePos(), dest_port.scenePos() )
        self.__m_Edges[ conn_name ] = edge # key: name, val: Edge

        self.addItem( edge )

        # establish edge-to-port link
        edge.ConnectSourcePort(source_port)
        edge.ConnectDestPort(dest_port)
        edge.UpdatePath()

        # establish port-to-edge link
        source_port.ConnectEdge( edge )
        dest_port.ConnectEdge( edge )

        print( "Create Edge(" + edge.Name() + ")" )
        
        print( 'ConnectAttribute( ' + source_port.Name() + ', ' + dest_port.Name() + ' )' )


    #def Reconnect( self, conn_name, source_port, dest_port ):

    #    if( not conn_name in self.__m_Edges ):
    #        return

    #    edge = self.__m_Edges[ conn_name ]


    #    # remove edge reference from ports
    #    if( edge.refSourcePort ):
    #        edge.refSourcePort.DisconnectEdge(edge)

    #    if( edge.refDestPort ):
    #        edge.refDestPort.DisconnectEdge(edge)

    #    # remove port reference from edge
    #    edge.DisconnectPort()


    #    # establish edge-to-port link
    #    edge.ConnectSourcePort(source_port)
    #    edge.ConnectDestPort(dest_port)
    #    edge.UpdatePath()

    #    # establish port-to-edge link
    #    source_port.ConnectEdge( edge )
    #    dest_port.ConnectEdge( edge )




    def Disconnect( self, edge ):

        #print( "Disconnecting Edge(" + edge.Name() + ")" )

        # remove edge reference from ports
        if( edge.refSourcePort ):
            edge.refSourcePort.DisconnectEdge(edge)

        if( edge.refDestPort ):
            edge.refDestPort.DisconnectEdge(edge)

        # remove port reference from edge
        edge.DisconnectPort()

        # remove from GraphicssScene
        self.removeItem( edge )
        del self.__m_Edges[ edge.Name() ]



    def CreateNode( self, node_name, nodetype, posx, posy ):

        #print( "Creating Node: " + nodetype )

        if( self.__m_pNodeTypeManager == None ):
            return

        node = Node( node_name, self.__m_pNodeTypeManager.GetNodeDesc(nodetype) )
        node.setPos( posx, posy )
        self.__m_Nodes[ node_name ] = node
        
        self.addItem(node)


    def RemoveNode_Standalone( self, node ):
        
        #print( "Removing Node(" + node.Name() + ")" )
        
        # disconnect input edges. delete only if unselected.
        for port in node.InputPorts():
            for edge in list(port.ConnectedEdges().values()):
                if( not edge.isSelected() ):
                    self.ExecCommand( ['Disconnect', edge.Name() ] ) #self.Disconnect( edge )# disconnect
                    self.removeItem( edge )# remove from QGraphicsScene
            port.ConnectedEdges().clear()

        # disconnect output edges. delete only if unselected.
        for port in node.OutputPorts():
            for edge in list(port.ConnectedEdges().values()):
                if( not edge.isSelected() ):
                    self.ExecCommand( ['Disconnect', edge.Name() ] ) #self.Disconnect( edge )# disconnect
                    self.removeItem( edge )# remove from QGraphicsScene
            port.ConnectedEdges().clear()

        # remove node
        #self.removeItem( node )


        # remove from dictionary
        del self.__m_Nodes[ node.Name() ]



    def RemoveNode( self, node ):

        print( "NodeEditorUI::RemoveNode(" + node.Name() + ")" )

        # remove from GraphicssScene
        self.removeItem( node )
        del self.__m_Nodes[ node.Name() ]


    def RemoveSelectedObjects( self ):
        
        #selectedItems = self.selectedItems()# // get list of selected items
        #for item in reversed(selectedItems):
        #    if( isinstance(item,Edge) ):
        #        self.ExecCommand( [ 'Disconnect', item.Name() ] )

        #for item in reversed(selectedItems):
        #    if( isinstance(item,Node) ):
        #        self.ExecCommand( [ 'RemoveNode', item.Name() ] )

        #    ################ NodeGroup Experimental implementation ###################
        #    if( isinstance(item,Group) ):
        #        self.ExecCommand( [ 'RemoveGroup', item.Name() ] )

        
        self.ExecCommand( ['Delete'] + [ item.Name() for item in self.selectedItems() ] )


#############################################################################################################
#################################### NodeGroup Experimental implementation ##################################
#############################################################################################################

    def Group( self ):

        selectedItems = [ item for item in self.selectedItems() if not isinstance(item, Edge) ]
        commandbuffer = ['Group'] + [ item.Name() for item in selectedItems ]

        self.ExecCommand( commandbuffer )


    def Ungroup( self ):

        selectedItems = [ item for item in self.selectedItems() if isinstance(item, Group) ] #self.selectedItems()# // get list of selected items
        
        for item in selectedItems[:]:
            self.ExecCommand( [ 'Ungroup', item.Name() ] )



#############################################################################################################
#############################################################################################################
#############################################################################################################





    ######################## QGraphicsScene func override #########################

    def keyPressEvent( self, event ):
        
        if( event.matches(QKeySequence.Delete) ):
            self.RemoveSelectedObjects()


#################################### NodeGroup Experimental implementation ##################################

        elif( (event.key()==Qt.Key_G) and (event.modifiers() & Qt.ControlModifier) ):
            self.Group()
            print('Grouping Operation')

        elif( (event.key()==Qt.Key_U) and (event.modifiers() & Qt.ControlModifier) ):
            self.Ungroup()
            print('Ungrouping Operation')

#############################################################################################################


        elif( event.matches( QKeySequence.Copy ) ):
            print('Ctrl-C')
            self.selectionList = self.selectedItems()

        elif( event.matches( QKeySequence.Cut ) ):
            print('Ctrl-X')

            self.selectionList = self.selectedItems()
            self.RemoveSelectedObjects()
    
        elif( event.matches( QKeySequence.Paste ) ):
            try:
                for item in self.selectionList:

                    if( isinstance(item,Node) ):

                        # TODO: ListConnections
                        self.ExecCommand( ['Duplicate', item.ObjectType(), item.scenePos().x()+50, item.scenePos().y()+50 ] )
                        # TODO: 引数で複製対象オブジェクト群の名前を送る -> sceneManager->Duplicate_Exec関数を実装する


                #for item in self.selectionList:
                #    if( isinstance(item,Node) ):
                #        self.ExecCommand( ['Connect', item.Name() ] )

                        print('Ctrl-V')
                self.selectionList.clear()
            except:
                pass




        return super(NodeEditorUI, self).keyPressEvent(event)


    #def keyReleaseEvent( self, event ):
        
    #    self.RemoveSelectedObjects(event)
    #    super(NodeEditorUI, self).keyReleaseEvent(event)


    def contextMenuEvent( self, event ):

        if( self.__m_pNodeTypeManager == None ):
            return

        pos = event.scenePos()

        menu = QMenu()

        # http://stackoverflow.com/questions/8824311/how-to-pass-arguments-to-callback-functions-in-pyqt

        for key in self.__m_pNodeTypeManager.GetNodeTypes():
            action = QAction( key, self )
            #action.triggered.connect( functools.partial(self.CreateNode, nodetype=key, pos=event.scenePos()) ) # OK
            #action.triggered.connect( lambda nodetype=key : self.CreateNode( nodetype, event.scenePos() ) ) # NG
            #menu.addAction( action )
            
            #menu.addAction( key, lambda nodetype=key : self.CreateNode( nodetype, event.scenePos() ) )# OK
            #menu.addAction( key, functools.partial(self.CreateNode, nodetype=key, pos=event.scenePos()) )

            action.triggered.connect( functools.partial(self.ExecCommand, commandbuffer=['CreateNode', key, pos.x(), pos.y()] ) )
            menu.addAction( action )

        #menu.addAction( 'TestNode2', lambda: self.CreateNode( val.Name(), event.scenePos() ) )
        #menu.addAction( 'TestNode', lambda: self.CreateNode( 'TestNode', event.scenePos() ) )
        # http://stackoverflow.com/questions/18428095/qt4-qmenu-addaction-connect-function-with-arguments
        # use "lambda:" for parametrized functions

        menu.exec(event.screenPos())

        

# https://wiki.qt.io/Smooth_Zoom_In_QGraphicsView/ja
class GraphicsView(QGraphicsView):

    def __init__(self):

        super(QGraphicsView, self).__init__()

        self.setWindowTitle("Test Node Graph")
        self.setStyleSheet( StyleSheet.NodeEditorStyleSheet )
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        #view->setOptimizationFlags(QGraphicsView::DontSavePainterState);
        self.setViewportUpdateMode( QGraphicsView.SmartViewportUpdate )
        self.setCacheMode( QGraphicsView.CacheBackground )
        
        self.setResizeAnchor( QGraphicsView.AnchorViewCenter )

        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )

        #self.__m_RubberBand = QRubberBand(self)
        

        self.zoomScale = 1.0
        # Background config
        self.gridStep = g_GridStep


    ######################## QGraphicsView func override #########################

    # zoom in/out using mouse wheel: http://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-out-under-mouse-position-using-mouse-wheel
    # deprecated (07.08.2016)

    # new reference implementation: http://blog.automaton2000.com/2014/04/mouse-centered-zooming-in-qgraphicsview.html
    def wheelEvent( self, event ):

        if( event.angleDelta().x() == 0 ):

            pos  = event.pos()
            posf = self.mapToScene(pos)

            by = 1.0
            angle = event.angleDelta().y()

            if( angle > 0 ):    by = 1 + ( angle / 360 * 0.2)
            elif( angle < 0 ):  by = 1 - (-angle / 360 * 0.2)
            else:               by = 1

            self.zoomScale *= by
            #self.scale(by, by)
            self.setTransform( QTransform().scale( self.zoomScale, self.zoomScale ) )


            w = self.viewport().width()
            h = self.viewport().height()

            wf = self.mapToScene( QPoint(w-1, 0) ).x() - self.mapToScene(QPoint(0,0)).x()
            hf = self.mapToScene( QPoint(0, h-1) ).y() - self.mapToScene(QPoint(0,0)).y()

            lf = posf.x() - pos.x() * wf / w
            tf = posf.y() - pos.y() * hf / h

            # try to set viewport properly
            self.setSceneRect( lf, tf, wf, hf )
            #self.ensureVisible( lf, tf, wf, hf, 0, 0 )

            newPos = self.mapToScene(pos)
           
            # readjust according to the still remaining offset/drift. I don't know how to do this any other way
            self.setSceneRect( QRectF( QPointF(lf, tf) - newPos + posf, QSizeF(wf, hf)) )
            #self.ensureVisible( QRectF( QPointF(lf, tf) - newPos + posf, QSizeF(wf, hf)), 0, 0 )
            
            event.accept()


    def mousePressEvent(self, event):

        self.prevPos = QPoint()
        self.drag = False

        if( event.modifiers() == Qt.AltModifier and event.button() == Qt.MiddleButton  ):

            self.setDragMode(QGraphicsView.NoDrag)
            self.drag = True
            self.prevPos = event.pos()
            self.setCursor(Qt.SizeAllCursor)

            #self.setDragMode( QGraphicsView.ScrollHandDrag )

        elif( event.button() == Qt.LeftButton ):

            self.setDragMode(QGraphicsView.RubberBandDrag)

        super(GraphicsView, self).mousePressEvent(event)
 

    def mouseMoveEvent(self, event):

        if( self.drag == True ):

            delta = (self.mapToScene(event.pos()) - self.mapToScene(self.prevPos)) * -1.0
            center = QPoint( self.viewport().width()/2 + delta.x(), self.viewport().height()/2 + delta.y() )
            newCenter = self.mapToScene(center)
            
            self.prevPos = event.pos()
            self.centerOn(newCenter)

            rect = self.sceneRect()
            self.setSceneRect( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height() )
            #self.ensureVisible( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height(), 0, 0 )

            event.accept()

            return

        super(GraphicsView, self).mouseMoveEvent(event)
 

    def mouseReleaseEvent(self, event):

        if( self.drag==True ):
            self.drag = False
            self.setCursor(Qt.ArrowCursor)

        super(GraphicsView, self).mouseReleaseEvent(event)


       
    def drawBackground( self, painter, rect ):
        #print( "GraphicsView::drawBackground" )

        # set background color
        #painter.fillRect( rect, QColor(42,42,42) ) # deprecated. defined using stylesheet (2016.07.16)

        # draw horizontal grid
        painter.setPen( QPen( QColor(64, 64, 64), 1.0/self.zoomScale ) )
        
        start = int(rect.top()) + self.gridStep / 2
        start -= start % self.gridStep

        if(start > rect.top()):
            start -= self.gridStep
        
        y = start - self.gridStep
        while( y < rect.bottom() ):
            y += self.gridStep
            painter.drawLine(rect.left(), y, rect.right(), y)

        # now draw vertical grid
        #start = rect.left() % self.gridStep
        start = int(rect.left()) + self.gridStep / 2
        start -= start % self.gridStep

        if(start > rect.left()):
            start -= self.gridStep
        
        x = start - self.gridStep
        while( x < rect.right() ):
            x += self.gridStep
            painter.drawLine(x, rect.top(), x, rect.bottom())




# http://www.qtcentre.org/threads/46648-Draw-Line-QGraphicsView
# http://www.walletfox.com/course/customqgraphicslineitem.php
# https://github.com/SonyWWS/ATF

#if __name__ == "__main__":

#    app = QApplication(sys.argv)

#    graphicsView = GraphicsView()
#    graphicsView.show()
#    sys.exit(app.exec_())
