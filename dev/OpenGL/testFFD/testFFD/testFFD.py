# TODO: Thin-Plate Spline Image Warpingの実装
# TODO: Moving Least Squareの実装




import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
#import scipy.misc as scm



gridsize = 20
cpsize = 4

# control points
P = np.zeros( (cpsize, cpsize, 2), dtype=np.float )



# set control point coordinates [0, 1]
for i in range(cpsize):
    x = i / (cpsize-1)
    for j in range(cpsize):
        y = j / (cpsize-1)
        P[i, j] = [x,y]
        


# bezier_patches(?)
X = np.zeros( (gridsize * gridsize, 2) )

# polygon vertices
V = np.zeros((gridsize * gridsize, 3))

# tex coords
T = np.zeros( (gridsize * gridsize, 2) ) 

# vertex indices
IDX = np.zeros( (gridsize-1, gridsize*2) )



class vec2:
    x=0.0
    y=0.0

    def __init__(self, x, y):
        self.x=x
        self.y=y


windowsize = vec2( 800, 800 )


start = vec2( -3, -4 )
delta = vec2( 0, 0 )

pick_radius = 5 / windowsize.x
cp_idx = vec2(-1,-1)




def factorial(k):
    sum = 1
    for i in range(1, k+1):
        sum *= i
    return sum


def binomialCoeff( n, k ):
    return factorial(n) / ( factorial(k) * factorial(n-k) )



def bernstein( n, i, t ):
    return binomialCoeff(n, i) * t**i * (1 - t)**(n-i)#return scm.comb(n, i) * t**i * (1 - t)**(n-i)



def bezier_patches( m, n, u, v, q ):
    return np.dot( [ bernstein(n, j, v) for j in range(n + 1) ], np.tensordot( [ bernstein(m, i, u) for i in range(m + 1) ], q, axes=1 ) )








def load_texture():
    img = Image.open( 'image.png' )
    w, h = img.size
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())



def reshape( w, h ):
    windowsize.x = w
    windowsize.y = h
    glViewport( 0, 0, windowsize.x, windowsize.y )
#    glMatrixMode(GL_PROJECTION)
#    glLoadIdentity()



def mouse( button, state, x, y ):

    cp_idx.x=-1
    cp_idx.y=-1

    if( state==GLUT_DOWN ):
        if( button==GLUT_LEFT_BUTTON ):
            pos = np.array( [ 2*(x/windowsize.x-0.25), 2*(1.0-y/windowsize.y-0.25)] )

            dist_2 = np.sum((P - pos)**2, axis=2)
            #print( dist_2 )

            #print( P )
            #print( pos )
            closest = np.unravel_index( np.argmin(dist_2), dist_2.shape )
            #print( np.unravel_index( np.argmin(dist_2), dist_2.shape ) )

            if( dist_2[ closest ] < pick_radius ):
                cp_idx.x = closest[0]
                cp_idx.y = closest[1]
                start.x = x
                start.y = y
                glutPostRedisplay()



def motion( x, y ):
    if( cp_idx.x < 0 or cp_idx.y<0 ):
        return
    delta.x = x - start.x
    delta.y = y - start.y
    #print( 'motion:', x-start.x, y-start.y )
    start.x = x
    start.y = y
    #print( 'motion:', x, y, start.x, start.y )

    P[ cp_idx.x, cp_idx.y, 0 ] += delta.x / windowsize.x * 2
    P[ cp_idx.x, cp_idx.y, 1 ] -= delta.y / windowsize.y * 2

    glutPostRedisplay()


def display():

    for i in range(gridsize):
        for j in range(gridsize):
            u = i / (gridsize-1)#10.0
            v = j / (gridsize-1)#10.0
            X[i * gridsize + j] = bezier_patches( cpsize-1, cpsize-1, u, v, P ) # FFD

            T[i * gridsize + j] = [i / (gridsize-1), 1.0 - j / (gridsize-1)]
            #T[i * gridsize + j] = [i / 10.0, 1.0 - j / 10.0]


    for i in range(gridsize):
        for j in range(gridsize):
            V[i*gridsize+j] = [ (X[i*gridsize+j, 0]-0.5)*1.5, (X[i*gridsize+j, 1]-0.5)*1.5, 0 ]


    for i in range(gridsize-1):#range(10):
        for j in range(gridsize):
            IDX[i, j * 2] = i * gridsize + j
            IDX[i, j * 2 + 1] = (i + 1) * gridsize + j


    #glPolygonMode( GL_FRONT_AND_BACK, GL_LINE ) 

    glClear(GL_COLOR_BUFFER_BIT)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    glEnable(GL_TEXTURE_2D)

    glVertexPointerf(V)
    glTexCoordPointerf(T)

    for idx in IDX:
        glDrawElementsui(GL_TRIANGLE_STRIP, idx)

    glDisable(GL_TEXTURE_2D)

    glDisable(GL_BLEND)


    # Draw control points
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for p in P.reshape((-1, 2)):
        glVertex2f(p[0] - 0.5, p[1] - 0.5)

    glEnd()

    glFlush()



def main():

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize( windowsize.x, windowsize.y )
    glutCreateWindow(b"FFDSample1")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glClearColor(0.2, 0.2, 0.2, 1.0)

    load_texture()
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glutMainLoop()

if __name__ == '__main__':
    main()