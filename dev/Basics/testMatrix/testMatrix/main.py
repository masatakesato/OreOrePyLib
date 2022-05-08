from oreorepylib.math.util import *


if __name__=='__main__':

    #m = Matrix(2, 3)
    #m[0][0] = 99.9
    #m.Print()


    #m_identity = IdentityMat3()
    #m_identity.Print()

    #m_99 = 99.9 * m_identity
    #m_99.Print()

    #m7 = m_identity * m_99
    ##m7.Print()


    #mat1 = Matrix(2, 2)
    #mat1.Init( [ [1, -3], [2, -4] ] )

    #mat2 = Matrix(2, 2)
    #mat2.Init( [ [5, 6], [7, 3] ] )


    #(3.0*mat1 - 2.0*mat2).Print()


    #mat = Matrix( 3, 3 )
    #mat.Init( [ [1, 2, 5], [1, -1, 1,], [0, 1, 2] ] )
    #mat.Print()

    #mat_inv = inverse_3x3( mat )
    #mat * mat_inv.Print()


    # init pos
    pos = Vec3( 3.36, -5.55, 1.0 )
    pos2 = Vec2( 3.36, -5.55 )
    
    # init translate matrix
    mat_trans = TranslateMat3( 10, 10 )

    pos.Print()
    mat_trans.Print()

    # translate pos
    p = mat_trans * pos
    p.Print()

    (mat_trans * pos2).Print()


    # inverse translate matrix and restore initial pos
    mat_trans_inv = InverseMat3( mat_trans )
    (mat_trans_inv * p).Print()

    mat2 = mat_trans_inv
    mat2 *= mat_trans
    mat2.Print()


    mat_trans *= pos
    mat_trans.Print()