###################################
##########  PROBLEM 5-4 ###########
###################################
# import time

def pp(matrix):
    for i in range(len(matrix)):
        print(matrix[i])

def recoverPath2D(moveArray, ghost1, ghost2):
    """
    Starting from last move, follow parent pointers back until we get a parent points to (0,0), which is the start point
    """
    moveSeq = []

    i = len(moveArray)-1
    j = len(moveArray[0])-1

    while (i + j) > 0:
        if i==0: # we can only move left
            moveSeq.append(ghost1[j])
            j-=1

        elif j==0: # we can only move up
            moveSeq.append(ghost2[i])
            i-=1

        else: # consider left, up, diagonal
            leftParent = moveArray[i][j-1]
            aboveParent = moveArray[i-1][j]
            diagonalParent = moveArray[i-1][j-1]

            if ghost1[j] == ghost2[i]: # go diagonal
                moveSeq.append(ghost2[i])
                i -= 1
                j -= 1
            elif leftParent < aboveParent: # go left
                moveSeq.append(ghost1[j])
                j-=1
            else: # go up
                moveSeq.append(ghost2[i])
                i-=1

    moveSeq.reverse()
    return moveSeq


def recoverPath3D(moveArray, ghost1, ghost2, ghost3):
    # t1 = time.time()
    moveSeq = []

    k = len(moveArray)-1
    i = len(moveArray[0])-1
    j = len(moveArray[0][0])-1

    while (i+j+k) > 0:
        if i==0 and j==0: # we can only move in k direction
            moveSeq.append(ghost3[k])
            k-=1

        elif j==0 and k==0: # we can only move in i direction
            moveSeq.append(ghost2[i])
            i-=1

        elif i==0 and k==0: # we can only move in j direction
            moveSeq.append(ghost1[j])
            j-=1

        elif i==0: # we can only move in j or k directions
            parent_j = moveArray[k][i][j-1]
            parent_k = moveArray[k-1][i][j]
            parent_jk = moveArray[k-1][i][j-1]
            if ghost1[j] == ghost3[k] and parent_jk == min(parent_j, parent_k, parent_jk): 
                # move diagonally if it is best 
                moveSeq.append(ghost3[k])
                j,k = j-1,k-1
            else: # move in j or k direction
                if parent_j < parent_k: # move in j
                    moveSeq.append(ghost1[j])
                    j-=1
                else:
                    moveSeq.append(ghost3[k]) # move in k
                    k-=1

        elif j==0: # we can only move in i or k directions
            parent_i = moveArray[k][i-1][j]
            parent_k = moveArray[k-1][i][j]
            parent_ik = moveArray[k-1][i-1][j]
            if ghost2[i] == ghost3[k] and parent_ik == min(parent_i, parent_k, parent_ik): 
                # move diagonally
                moveSeq.append(ghost3[k])
                i,k=i-1,k-1
            else: # move in i or k direction
                if parent_i < parent_k: # move in i
                    moveSeq.append(ghost2[i])
                    i-=1
                else: # move in k
                    moveSeq.append(ghost3[k])
                    k-=1

        elif k==0: # we can only move in i or j directions
            parent_i = moveArray[k][i-1][j]
            parent_j = moveArray[k][i][j-1]
            parent_ij = moveArray[k][i-1][j-1]

            if ghost1[j] == ghost2[i] and parent_ij == min(parent_i, parent_j, parent_ij): 
            # move diagonally
                moveSeq.append(ghost2[i])
                i,j = i-1, j-1
            else: # move in i or j direction
                if parent_i < parent_j: # move in i
                    moveSeq.append(ghost2[i])
                    i-=1
                else: # move in j
                    moveSeq.append(ghost1[j])
                    j-=1

        else: # we can go in any of 7 directions
            parent_j = moveArray[k][i][j-1]
            parent_i = moveArray[k][i-1][j]
            parent_k = moveArray[k-1][i][j]
            parent_ij = moveArray[k][i-1][j-1]
            parent_ik = moveArray[k-1][i-1][j]
            parent_jk = moveArray[k-1][i][j-1]
            parent_ijk = moveArray[k-1][i-1][j-1]

            if ghost1[j] == ghost2[i] and ghost1[j] == ghost3[k] and parent_ijk==min(parent_i, parent_j, parent_k, parent_ik, parent_ij, parent_jk, parent_ijk): # ijk possible
                moveSeq.append(ghost2[i])
                i,j,k = i-1, j-1, k-1
            elif ghost1[j] == ghost2[i] and parent_ij == min(parent_i, parent_j, parent_k, parent_ij): # use ij
                moveSeq.append(ghost2[i])
                i,j = i-1, j-1
            elif ghost1[j] == ghost3[k] and parent_jk == min(parent_i, parent_j, parent_k, parent_jk): # use jk
                moveSeq.append(ghost1[j])
                j,k = j-1, k-1
            elif ghost2[i] == ghost3[k] and parent_ik == min(parent_i, parent_j, parent_k, parent_ik): # use ik
                moveSeq.append(ghost2[i])
                i,k = i-1,k-1
            else: # use whichever of i, j, k is shortest
                if parent_i == min(parent_j, parent_i, parent_k): # use parent_i
                    moveSeq.append(ghost2[i])
                    i-=1
                elif parent_j == min(parent_i, parent_j, parent_k): # use parent_j
                    moveSeq.append(ghost1[j])
                    j-=1
                else:
                    moveSeq.append(ghost3[k])
                    k-=1
    moveSeq.reverse()
    # t2 = time.time()
    # print("Recover time:", t2-t1)
    return moveSeq

def double_kill(ghost1, ghost2):
    """
    Compute the shortest move sequence which will make both ghosts disappear.

    Parameters
    ----------
    ghost1: []
        ordered list of moves which will make ghost1 disappear
    ghost2: []
        ordered list of moves which will make ghost2 disappear

    Returns
    -------
    seq : []
        move sequence of minimal length which will make both ghosts disappear
    """
    ghost1 = ['_'] + ghost1
    ghost2 = ['_'] + ghost2
    #initialize empty move array with |ghost1|+1 columns and |ghost2|+1 rows
    moveArray = [[0 for i in range(len(ghost1))] for j in range(len(ghost2))]

    # fill in the moveArray row by row
    for i in range(len(ghost2)): # for a given row
        for j in range(len(ghost1)): # for each element in that row
            
            #case 0: i=0 and j=0 means that we're in the starting slot
            if (i==0 and j==0):
                continue
            #case 1: i=0 means that there are no slots above
            elif i==0:
                # (Num. moves of left slot +1, letter of this col., index of left slot)
                moveArray[i][j] = moveArray[i][j-1]+1

            #case 2: j=0 means that there are no slots to the left
            elif j==0:
                # (Num. moves of above slot +1, letter of this row, indes of above slot)
                moveArray[i][j] = moveArray[i-1][j]+1

            else: # consider item to left, item above, and diagonal item (if letter are the same)
                # consider left, up, diagonal
                left = moveArray[i][j-1]
                up = moveArray[i-1][j]
                
                if ghost1[j] == ghost2[i]:
                    diagonal = moveArray[i-1][j-1]
                    # if we want the left parent
                    if (left < up) and (left < diagonal):
                        moveArray[i][j] = left+1

                    # if we want the above parent
                    elif up < diagonal:
                        moveArray[i][j] = up+1

                    else: #use diagonal
                        moveArray[i][j] = diagonal+1

                else: # do not consider diagonal
                    if left < up:
                        moveArray[i][j] = left+1
                    else:
                        moveArray[i][j] = up+1
    return recoverPath2D(moveArray, ghost1, ghost2)

# #
# PART B: Fill in the code for part b
#

def triple_kill(ghost1, ghost2, ghost3):
    #t1 = time.time()
    """
    Compute the shortest move sequence which will make all three ghosts disappear.

    Parameters
    ----------
    ghost1: []
        ordered list of moves which will make ghost1 disappear
    ghost2: []
        ordered list of moves which will make ghost2 disappear
    ghost3: []
        ordered list of moves which will make ghost3 disappear

    Returns
    -------
    seq : []
        move sequence of minimal length which will make all three ghosts disappear
    """
    ghost1 = ['_']+ghost1
    ghost2 = ['_']+ghost2
    ghost3 = ['_']+ghost3

    # [ghost3][ghost2][ghost1] order of indexing
    moveArray = [[[0 for i in range(len(ghost1))] for j in range(len(ghost2))] for k in range(len(ghost3))]
    
    for k in range(len(ghost3)): # consider one ij plane at a time
        for i in range(len(ghost2)): # for a given row
            for j in range(len(ghost1)): # fill in the whole column of that row

                # ignore the origin 
                if i==0 and j==0 and k==0:
                    continue

                # parent must be from left
                elif k==0 and i==0:
                    moveArray[k][i][j] = moveArray[k][i][j-1]+1

                # parent must be above
                elif k==0 and j==0:
                    moveArray[k][i][j] = moveArray[k][i-1][j]+1

                # parent must be from behind (on k axis)
                elif i==0 and j==0:
                    moveArray[k][i][j] = moveArray[k-1][i][j]+1

                elif k==0: # we are in the front plane, so 
                    # consider: parent i, parent j, parent ij
                    if ghost1[j] == ghost2[i]:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k][i][j-1], moveArray[k][i-1][j-1])
                    else:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k][i][j-1])

                elif j==0: # we are in the left plane
                    # consider: parent i, parent k, parent ik
                    if ghost2[i] == ghost3[k]:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k-1][i][j], moveArray[k-1][i-1][j])
                    else:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k-1][i][j])

                elif i==0: # we are in the top plane
                    # consider: parent j, parent k, and parent jk
                    if ghost1[j] == ghost3[k]:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i][j-1], moveArray[k-1][i][j], moveArray[k-1][i][j-1])
                    else:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i][j-1], moveArray[k-1][i][j])

                else:
                    # all possible parents
                    parent_i = moveArray[k][i-1][j]
                    parent_j = moveArray[k][i][j-1]
                    parent_k = moveArray[k-1][i][j]

                    if ghost1[j] == ghost3[k] and ghost1[j] == ghost2[i]: # then ijk is possible
                        parent_ij = moveArray[k][i-1][j-1]
                        parent_jk = moveArray[k-1][i][j-1]
                        parent_ik = moveArray[k-1][i-1][j]
                        parent_ijk = moveArray[k-1][i-1][j-1]
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_ij, parent_jk, parent_ik, parent_ijk)
                    
                    elif ghost1[j] == ghost2[i]: #ij is possible
                        parent_ij = moveArray[k][i-1][j-1]
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_ij)

                    elif ghost2[i] == ghost3[k]: #ik is possible
                        parent_ik = moveArray[k-1][i-1][j]
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_ik)

                    elif ghost1[j] == ghost3[k]: #jk is possible
                        parent_jk = moveArray[k-1][i][j-1]
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_jk)

                    else: # just consider i, j, k
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k)      

    # t2 = time.time()
    # print("Build time:", t2-t1)
    path = recoverPath3D(moveArray, ghost1, ghost2, ghost3)
    return path

# moves1 = ['A', 'B', 'B', 'B', 'D', 'A', 'D', 'C', 'A', 'B', 'C', 'A', 'D', 'B', 'A', 'A', 'A', 'B']
# moves2 = ['C', 'B', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'B', 'A', 'A']
# moves2 = ['C', 'B', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'B', 'A', 'A']

# double_kill_sol = double_kill(moves1,moves2)
# triple_kill_sol = triple_kill(moves1,moves2,[])
# print double_kill_sol
# print triple_kill_sol




