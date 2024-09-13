import initList as iL

class actionSig():
    def __init__(self,k,m):
        # names as non-negative integers
        self.actionNames = range(k)
        self.fluentNames = range(m)
        temp = []
        # default propositional
        for i in range(m):
            temp.append(2)
        self.fluentVals = temp


    # to override propositional default
    def setFluentVals(self,list):
        self.fluentVals = list

    def mkTranSys(self):
        temp = tranSys(len(self.actionNames), len(self.fluentNames))
        temp.setFluentVals(self.fluentVals)
        temp.val = iL.genValBL(self.fluentVals)
        temp.states =  range(len(temp.val))
        temp.transReln = iL.initTransReln(len(temp.states),len(self.actionNames))
        return temp

    #\def ULD_automata(self):
        #uld = actionSig(2,2);
        #uld.setFluentVals(['u','l','d']);
        #uld_t = uld.mkTranSys();

        
class tranSys(actionSig):      # add states, valuations, transRelation
    def __init__(self,k,m):
        super(tranSys,self).__init__(k,m)
        self.val = iL.genValBL(self.fluentVals)
        self.states = range(len(self.val))
        self.transReln = iL.initTransReln(len(self.states),k)
        
    # add transitions
    def addTrans(self,preState,action,postState):
        if not(postState in self.transReln[preState][action]):
            self.transReln[preState][action].append(postState)

    # remove transitions
    def removeTrans(self,preState,action,postState):
        if postState in self.transReln[preState][action]:
            self.transReln[preState][action].remove(postState)

            
class descTranSys(tranSys):    # add actionLangDescriptions
    pass



def demo():
    a = actionSig(3,4)
    print("Did: a = actionSig(3,4) for 3 actions, 4 fluents")
    a.setFluentVals([5,2,3,3])
    print("Did: a.setFluentVals([5,2,3,3])")
    t = a.mkTranSys()
    print("Did: t = a.mkTranSys()")
    print(len(t.states),"states over",len(t.fluentNames),"fluents")
    print("fluent i at state q has value = t.val[q][i]")
    print("t.val =",t.val)
    print(len(t.actionNames),"actions in t.transReln =",t.transReln)
    print("[q1,a,q2] is a t-transition  iff  q2 in t.transReln[q1][a]")
    t.addTrans(2,1,7)    
    print("t.addTrans(2,1,7) for",t.transReln)
    t.removeTrans(2,1,7)    
    print("t.removeTrans(2,1,7) for",t.transReln)

    
demo() 