class NFA:
    def __init__(self):
        self.init = "q0"
        self.final = set()
        self.trans = {}  # dict with key = prestate (number)
                         #           val = dict with key = act 
                         #                  val = set of poststates (numbers)

    def accept(self,strList):
        if len(strList) == 0:
            if self.init in self.final:
                ans = "accepted"
            else:
                ans = "rejected"
        else:
            stateList = [self.init]
            ans = "rejected"
            for state in self.steps(strList, stateList):
                if state in self.final:
                    ans = "accepted"
                    break
        return ans

    def steps(self, strList, stateList):
        if len(strList) == 1:
            temp = self.step(strList[0],stateList)
        elif len(strList) > 1:
            symbol = strList[0]
            tail = strList[1:]
            temp = self.steps(tail, self.step(symbol,stateList))
        return(temp)

    def step(self, symbol, stateList):
        temp = []
        for state in stateList:
            if state in self.trans:
                if symbol in self.trans[state]:
                    for next in self.trans[state][symbol]:
                        temp.append(next)
        return(temp)
        
    def add_trans(self, pre, label, post):
        if pre in self.trans:
            if label in self.trans[pre]:
                self.trans[pre][label].add(post)
            else:
                self.trans[pre][label] = {post}
        else:
            self.trans[pre] = {label: {post}}

    def add_final(self, state):
        self.final.add(state)

    def trace(self,strList):  # depth-first, contra breadth-first accept above
        return self.dfsRun([(strList,self.init,[])])
                
    def dfsRun(self,frontier):
        if frontier == []:
            return "rejected" 
        else:
            strList = frontier[-1][0]
            state = frontier[-1][1]
            run = frontier.copy()[-1][2]
            frontier.pop()
            if len(strList) == 0 and state in self.final:
                return run
            elif len(strList)>0:
                symbol = strList[0]
                tail = strList[1:]
                for next in self.step(symbol,[state]):
                    r = run.copy()
                    r.append((symbol,next))
                    frontier.append((tail,next,r))
            return self.dfsRun(frontier)


    def make_sfa(self,label):
        temp = sfa()
        temp.labels = { label } 
        invStateD = { self.init : 0 }
        istate = 1
        for i in self.trans:
            if not(i in invStateD):
                invStateD[i] = { istate }
                istate += istate        
            temp.trans[invStateD[i]] = {}
            poststates = set()
            for act in self.trans[i]:
                temp.actD[s2s({act})] ={ act }
                for post in self.trans[i][act]:
                    if not(post in invStateD):
                        invStateD[post] = istate
                        istate += istate        
                    poststates.add(invStateD[post])
                #print("poststates", poststates)
                #print(temp.trans)
                temp.trans[invStateD[i]] = dicMerge(temp.trans[invStateD[i]],
                                                    { s2s({act}): poststates })
                #print(temp.trans)
        #print("invStateD", invStateD)
        for i in invStateD:
            temp.stateD[invStateD[i]] = { label : i }
#            temp.stateD[invStateD[i]] = i
            if i in self.final:
                temp.final.add(invStateD[i])
        #print("temp.stateD", temp.stateD)
        return temp

def dicMerge(dic1,dic2):
    temp = dic1.copy()
    for key in dic2:
        if key in dic1:
            temp[key] = temp[key].union(dic2[key])
        else:
            temp[key] = dic2[key]
    return temp
    

def uld(a):   # encode interval a in action (public) but not in state (private)
    temp = NFA()
    temp.init = "u"      # + "(" + str(a) + ")"
    temp.final = {"d"}   # + "(" +str(a) + ")"}
    la = "l"             # +"("+str(a)+")"
    temp.trans = { temp.init: {a: {la}},
                   la: {-a: temp.final}  }
    return temp

    
# sfa = set/structured finite automata (for S-words)
#  nfa with trans given for states and acts described by dictionaries 
#    stateD decoding/structuring state as a dictionary [record]
#    actD decoding str(act) [better: s2s(act)] to expose the set behind act
#  plus
#    labels used by stateD to describe states
#      make disjoint from other sfa to keep information private
#  and method accS for accept given a list of sets (internally representing
#                                   a set qua symbol as the string from s2s)
#
class sfa(NFA):

#  init = 0
#  stateD = {}
#  actD = {}
#  labels = { "need to fix for use in stateD" }                 

    def __init__(self):
        super().__init__()
        self.init = 0
        self.final = set()
        self.stateD = { 0:{} }
        self.actD = {}
        self.labels = { "need to fix for use in stateD" } 
                    

    def accS(self,listSet):
        return self.accept(sfaInput(listSet))

def sfaInput(listSet):
    print()
    temp = []
    for i in listSet:
        temp.append(s2s(i))
    return temp
    
# variant of str(set0) s.t. s2s({-1,-3,-2}) == s2s({-2,-3,-1})
def s2s(set0):
    temp = []
    for i in set0:
        temp.append(i)
    temp.sort()
    return str(temp)


def sup(sfa1,sfa2,voc1,voc2): 
    temp = sfa()
    temp.stateD = { 0: {1:sfa1.init, 2:sfa2.init} }
    newp = {(sfa1.init,sfa2.init)}
    done = set()
    while not(newp==set()):
        nextp = set()
        for q in newp:
            morecu = rulecu(sfa1,sfa2,voc1,voc2,q,temp)
            mored1 = ruled1(sfa1,voc2,q,temp)
            mored2 = ruled2(sfa2,voc1,q,temp)        
            morep = morecu.union(mored1.union(mored2))
            nextp = nextp.union(morep)
        done = done.union(newp)
        newp = nextp.difference(done)
    for i in temp.stateD:
        if temp.stateD[i][1] in sfa1.final and temp.stateD[i][2] in sfa2.final:
            temp.final.add(i)
#  unwind temp.stateD using sfa1, sfa2
    temp.stateD = unwindSD(temp.stateD,sfa1.stateD,sfa2.stateD)
    temp.labels = sfa1.labels.union(sfa2.labels)
    return temp

def unwindSD(sD,sD1,sD2):
    temp = {}
    for i in sD:
# flatten:        
        temp[i] = dicUnion(sD1[sD[i][1]],sD2[sD[i][2]])
    return temp

def dicUnion(dic1,dic2):
    temp = dic1.copy()
    for key in dic2:
        if key in temp:
            if not(dic2[key] == temp[key]):
                print("Clashing keys/labels (dicUnion)")
        temp[key] = dic2[key]
    return temp
        
def rulecu(sfa1,sfa2,voc1,voc2,q,temp): # cu add to p [side-effects on temp]
    morep = set()
    moretrans = {}
    if (q[0] in sfa1.trans  and  q[1] in sfa2.trans):
        for a1 in sfa1.trans[q[0]]:
            for a2 in sfa2.trans[q[1]]:
                s1 = sfa1.actD[a1]
                s2 = sfa2.actD[a2]
                s = s1.union(s2)
                if contain(s1,voc2,s2) and contain(s2,voc1,s1):
                    for r1 in sfa1.trans[q[0]][a1]:
                        for r2 in sfa2.trans[q[1]][a2]:
                            r = (r1,r2)
                            morep.add(r)
                            temp.actD[s2s(s)] = s
                            add2stateD(temp,r)
                            qcode = decodeState(temp,q)
                            di = {s2s(s): {decodeState(temp,r)}} 
                            if qcode in temp.trans:
                                temp.trans[qcode] = dicMerge(temp.trans[qcode],
                                                             di)
                            else:
                                temp.trans[qcode] = di
    return morep

def ruled1(sfa1,voc2,q,temp): # d1 add to p [side-effects on temp]
    morep = set()
    moretrans = {}
    if q[0] in sfa1.trans:
        for a1 in sfa1.trans[q[0]]:
            s = sfa1.actD[a1]
            if contain(s,voc2,set()):
                for r1 in sfa1.trans[q[0]][a1]:
                    r = (r1,q[1])
                    morep.add(r)
                    temp.actD[s2s(s)] = s
                    add2stateD(temp,r)
                    qcode = decodeState(temp,q)
                    di = {s2s(s): {decodeState(temp,r)}} 
                    if qcode in temp.trans:
                         temp.trans[qcode] = dicMerge(temp.trans[qcode],
                                                      di)
                    else:
                         temp.trans[qcode] = di
    return morep

def ruled2(sfa2,voc1,q,temp): # d2 add to p [side-effects on temp]
    morep = set()
    moretrans = {}
    if q[1] in sfa2.trans:
        for a2 in sfa2.trans[q[1]]:
            s = sfa2.actD[a2]
            if contain(s,voc1,set()):
                for r2 in sfa2.trans[q[1]][a2]:
                    r = (q[0],r2)
                    morep.add(r)
                    temp.actD[s2s(s)] = s
                    add2stateD(temp,r)
                    qcode = decodeState(temp,q)
                    di = {s2s(s): {decodeState(temp,r)}} 
                    if qcode in temp.trans:
                         temp.trans[qcode] = dicMerge(temp.trans[qcode],
                                                      di)
                    else:
                         temp.trans[qcode] = di
    return morep

def add2stateD(sfa,r):
    old = False
    for i in sfa.stateD:
        if sfa.stateD[i]=={1:r[0], 2:r[1]}:
            old = True
    if old == False:
        sfa.stateD[len(sfa.stateD)] = {1:r[0], 2:r[1]}

def decodeState(sfa,r):
    found = -1
    for i in sfa.stateD:
        if sfa.stateD[i]=={1:r[0], 2:r[1]}:
            found = i
    return found

def contain(set1,set2,set3):
    return set1.intersection(set2).issubset(set3)

def voc(n):
    return {n,-n}

def vocA(n):
    temp = voc(n)
    if n == 1:
        return temp
    elif 1<n:
        return temp.union(vocA(n-1))

def supULD(n):
    temp = uld(n).make_sfa(n)
    if n == 1:
        return temp
    elif 1<n:
        return sup(temp,supULD(n-1),voc(n),vocA(n-1))
    
def itemize(dic):
    for i in dic:
        print(i," ", dic[i], " end of item")



def demo():
    
    f3 = supULD(2)
    print(" ULD for 3 intervals via f3 = supULD(3)")
    print("f3.stateD[f3.init]=", f3.stateD[f3.init])
    tStr = sfaInput([{1,2,3},{-1,-2,-3}])
    print(" tStr = ",tStr)
    print("f3.accept(tStr) =", f3.accept(tStr))
    print("f3.accS([{1,2,3},{-1,-2,-3}]) =", f3.accS([{1,2,3},{-1,-2,-3}]))
    print(f3.stateD)

demo()