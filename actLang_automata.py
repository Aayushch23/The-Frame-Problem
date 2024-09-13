from automata.fa.dfa import DFA
import actLang as al
import initList as iL

def nestedList(List):
     init = {}
     for i in range(len(List)):
       init[i] = [0,0]
       init[i][0] = List[i]
       init[i][1] = [0,0,0]
     return init     
     
a = al.actionSig(3,4)
a.setFluentVals([5,2,3,3])
t = a.mkTranSys()
g = nestedList(t.val)
print(g)

d = []
state = set()
#print(g)
for j in g:
     a = []
     b = ''
     b = b + str(j) + str(g[j][1])
     a.append(g[j][1])
     state.add(b)
     d.append(b)

print(state)
dfa = DFA(
      states = g,
      input_symbols ={0,1},
      transitions ={ 
           g[0][1][0]: {0:g[0][1][0],1:g[1][1][0]},
           g[0][1][1]: {0:g[1][1][0],1:g[1][1][0]}
      },
      initial_state = g[0][1][0],
      final_states = len(range(g))
)
   
#dfa.show_diagram()   
    
#def addTrans(self,preState,action,postState):
      #dfa.transitions
  



