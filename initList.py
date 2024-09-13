def genVal(base,len):
    # start with len 0's
    init = []
    for i in range(len):
        init.append(0)
    temp = [init]
    # increment_base that list base**len -1 times
    for i in range((base**(len))-1):
        temp.append(increment(temp[-1],base))
    return temp

def increment(list,base):
    temp = list.copy()
    if list[0] < base-1:
        temp[0] += 1
    else:
        temp[0] = 0    # carry
        temp[1:] = increment(temp[1:],base)
    return temp


# generalization of above to a list of bases
#   e.g.   genVal(2,3) == genValBL([2,2,2])
def genValBL(baseList):
    init = []
    iter = 1
    for i in range(len(baseList)):
        init.append(0)
        iter = iter*baseList[i]
    temp = [init]
    for i in range(iter-1):
        temp.append(incrementBL(temp[-1],baseList))
    return temp

def incrementBL(list,baseList):
    temp = list.copy()
    if list[0] < baseList[0]-1:
        temp[0] += 1
    else:
        temp[0] = 0    # carry
        temp[1:] = incrementBL(temp[1:],baseList[1:])
    return temp



def initTransReln(qNumber,k):
    temp = []
    for q in range(qNumber):
        qTrans = []
        for a in range(k):
            qTrans.append([])
        temp.append(qTrans)
    return temp
    # to see if [q1,a,q2] is a transition according to T
    #   check   q2 in  T[q1][a]
