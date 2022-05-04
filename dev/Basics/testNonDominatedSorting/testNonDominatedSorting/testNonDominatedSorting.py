# https://ac.els-cdn.com/S089812210800552X/1-s2.0-S089812210800552X-main.pdf?_tid=8ea3c4a2-c003-46c9-9b4e-3d24e00ee298&acdnat=1535595316_4897ec82def277d1084a46d5435ed629
# http://vision.ucsd.edu/~sagarwal/nsga2.pdf
# http://read.pudn.com/downloads192/sourcecode/math/901231/NSGA-II/non_domination_sort_mod.m__.htm


from collections import defaultdict
import numpy



# check if p dominates q
def dominates( p, q ):
    for i in range(len(p)):
        if( p[i] > q[i] ):
            return False

    return True


# fast non-dominated sorting
def fast_nondominated_sort( P ):

    F = defaultdict( list )# Fronts
    D = defaultdict( list )# Individuals that P[i] dominates.
    n = defaultdict( int )# Num of individuals that dominates P[i].
    
    for ai in P:
        i = id(ai)
        n[i] = 0# number of solutions which dominate the ai.
        D[i] = []# set of solutions which ai dominates.
        
        for aj in P:
            if( dominates(ai,aj) ): # ajが劣解の場合はSpに追加する
                D[i].append(aj)
            elif( dominates(aj,ai) ):# aiが劣解の場合はランクを上げる
                n[i] = n[i] + 1

        if( n[i]==0 ):
            F[1].append(ai)

    r=1
    while( r in F ):
        H = []
        for ai in F[r]:
            i = id(ai)
            for aj in D[i]:# aiが支配する劣解のリストを取得したい.
                j = id(aj)
                n[j] = n[j] - 1
                if( n[j]==0 ):
                    H.append(aj)
        r = r + 1
        if( H ): F[r] = H
    
    return F




def fast_nondominated_sort_index_ver( P ):

    F = defaultdict( list )# Fronts
    D = [[]] * len(P)# Individuals that P[i] dominates.
    n = [0] * len(P)# Num of individuals that dominates P[i].
    
    for i in range( len(P) ):
        n[i] = 0# number of solutions which dominate the ai.
        D[i] = []# set of solutions which ai dominates.
        
        ai = P[i]         

        for j in range( len(P) ):
            aj = P[j]
            if( dominates(ai,aj) ): # ajが劣解の場合はSpに追加する
                D[i].append(j)
            elif( dominates(aj,ai) ):# aiが劣解の場合はランクを上げる
                n[i] = n[i] + 1

        if( n[i]==0 ):
            F[0].append(i) #F[1].append(ai)

    r=0
    while( r in F ):
        H = []
        for i in F[r]:# Get individual i from Front r.
            for j in D[i]:# P[i]が支配する劣解のリストを取得したい.
                n[j] = n[j] - 1
                if( n[j]==0 ):
                    H.append(j)
        r = r + 1
        if( H ): F[r] = H
    

    return F




# TODO: implement sort function.
def sort( f, m ):
    f.sort( solutions, key=lambda x:x[m] ) 


def argmaxmin( f, m ):
    arr = numpy.array(f)
    return arr.argmax(axis=m), arr.argmin(axis=m)



def crowding_distance( F ):

    N = len(F)
    M = F.shape[1]
    Fdist = numpy.zeros( N, dtype='float32' )
    
    # Initialize distance with zero
    for i in range(N):
        Fdist[i] = 0
    
    # Accumulate crowding distance.
    for m in range(M):
        # Sort F using objective m
        indices_sorted = F[:,m].argsort()# Fm = numpy.sort( F, axis=m )

        # Get fitness range of m's objective.
        fmax_m = F[ indices_sorted[N-1] ][m]
        fmin_m = F[ indices_sorted[0] ][m]
        f_range_m = max( fmax_m - fmin_m, 1.0e-5 )
        
        # Reorder F and Fdist according to objective m's fitness.
        F = F[ indices_sorted ]
        Fdist = Fdist[ indices_sorted ]
        
        # Set extreme solution's distance to infinity.(to guarantee that they will be selected in the next generation)
        Fdist[0] = Fdist[N-1] = numpy.inf
        # Calculate other solutions' distance
        for i in range(1, N-1):
            Fdist[i] = Fdist[i] + ( F[i+1][m] - F[i-1][m] ) / f_range_m

    sorted_idx = Fdist.argsort()
    F_ = F[sorted_idx[::-1]]
    Fdist_ = Fdist[sorted_idx[::-1]]

    print( 'F:', F_ )
    print( 'Fdist_:', Fdist_ )

    return F_



def crowding_distance_index_ver( F ):

    N = len(F)
    M = F.shape[1]
    Fdist = numpy.zeros( N, dtype='float32' )# TODO: Must be reordered along with F. Should be attached to F. 2018.08.31
    
    # Initialize distance with zero
    for i in range(N):
        Fdist[i] = 0
    
    # Accumulate crowding distance.
    for m in range(M):
        # Sort F using objective m
        indices_sorted = F[:,m].argsort()#Fm = numpy.sort( F, axis=m )

        # Get fitness range of m's objective.
        fmax_m = F[ indices_sorted[N-1] ][m]
        fmin_m = F[ indices_sorted[0] ][m]
        f_range_m = max( fmax_m - fmin_m, 1.0e-5 )
        
        # Set extreme solution's distance to infinity.(to guarantee that they will be selected in the next generation)
        Fdist[ indices_sorted[0] ] = Fdist[ indices_sorted[N-1] ] = numpy.inf

        # Calculate other solutions' distance
        for i in range(1, N-1):
            il = indices_sorted[i-1]
            ir = indices_sorted[i+1]
            ic = indices_sorted[i]
            Fdist[ic] = Fdist[ic] + ( F[ir][m] - F[il][m] ) / f_range_m

    sorted_idx = Fdist.argsort()
    F_ = F[ sorted_idx[::-1] ]
    Fdist_ = Fdist[ sorted_idx[::-1] ]
    
    print( 'F_:', F_ )
    print( 'Fdist_:', Fdist_ )

    return F_








if __name__=='__main__':

    #=================== Fast Non-dominated Sorting test ======================#    
    #print( dominates( [-3.0, 0.0], [3.0,3.0] ) )
    
    #solutions_ = numpy.array( [ [0.0, 0.0], [7.0,7.0], [3.0,5.0], [3.0,3.0], [5.0,3.0], [1.0, 7.0], [7.0, 1.0] ] )
    #solutions = [ [0.0, 0.0], [7.0,7.0], [3.0,5.0], [3.0,3.0], [5.0,3.0], [1.0, 7.0], [7.0, 1.0], ]

    #print( solutions )

    #fronts = fast_nondominated_sort( solutions )
    #print( fronts )

    #fronts = fast_nondominated_sort_index_ver( solutions )
    #print( fronts )


    #for i, f in fronts.items():
    #    front = numpy.array( f )
    #    print( 'Front %d:\n' % i, front, '\n' )

    #    crowding_distance( front )
    

    #=================== Crowding Distance Calculation test ======================#    
    print( 'crowding_distance()...' )
    front = numpy.array( [ [0.0, 0.0], [7.0,4.0], [3.0,5.0], [3.0,3.0], [5.0,3.0], [1.0, 1.0], [4.0, 7.0], ] )
    sorted_front = crowding_distance( front )

    print( 'crowding_distance_index_ver()...' )
    front = numpy.array( [ [0.0, 0.0], [7.0,4.0], [3.0,5.0], [3.0,3.0], [5.0,3.0], [1.0, 1.0], [4.0, 7.0], ] )
    sorted_front = crowding_distance_index_ver( front )#
        
    #print( front )
    #print( sorted_front )

    # TODO: 解候補に含まれる全フロントのCroiwing Distanceを計算する
    # TODO: 全フロントの解候補をCrodwing Distanceでソートする( 降順ソート.疎な解から優先的に選択する )
    # TODO: ソート結果の上位から次の世代に残す個体を選別する