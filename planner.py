import argparse
from pulp import *
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--mdp', help='mdp', type=str, default='dumy_feature')
parser.add_argument('--algorithm', help='algo', type=str, default='hpi')
parser.add_argument('--policy', help='policy', type=str, default='')
args = parser.parse_args()
mdp_path=args.mdp
algo=args.algorithm
policy=args.policy

def HPI_episodic(mdp):
    end_state=mdp["end_state"]
    arr=np.zeros(mdp["num_states"])
    I=np.eye(mdp["num_states"])
    for i in range(mdp["num_states"]):
            
        target_first_value = i
        l=[lst for lst in mdp["transitions"] if lst[0] == target_first_value]
        if len(l)==0:
            continue
        arr[i]=l[0][1] 
    k=10
    while k>0:
        T=np.zeros((mdp["num_states"],mdp["num_states"]))
        R=np.zeros(mdp["num_states"])
        for i in range(mdp["num_states"]):
            if str(i) in end_state:
                T[i:]=0
                R[i]=0
                continue
            z=0
            for j in range(mdp["num_states"]):
               l=[lst for lst in mdp["transitions"] if lst[0] == i and lst[1] == arr[i] and lst[2]== j] 
               #print(l)
               if bool(l):
                T[i][j]=l[0][4]
                z=z+l[0][4]*l[0][3]
            R[i]=z
        V_1=np.linalg.inv(I-mdp["discount"]*T)
        V=np.dot(V_1,R)
        a=I-mdp["discount"]*T
        #V=np.linalg.solve(a,R)
        #print(V)
        #print(arr)
        my_dict = {i: None for i in range(mdp["num_states"])}
        e=0.000001
        for i in range(mdp["num_states"]):
            v_temp=V[i]
            for j in range(mdp["num_actions"]):
                b=0
                l=[lst for lst in mdp["transitions"] if lst[0] == i and lst[1] == j] 
                for x in l:
                    s=x[2]
                    b=b+ x[4]*(x[3]+mdp["discount"]*V[s])
                    #print(i,b,V[i])
                if b-V[i]>e:
                    my_dict[i]=1
                if b>v_temp:
                    arr[i]=j
                    v_temp=b
        #k=k-1
        #print(my_dict)
        if all(value is None for value in my_dict.values()):
            break
    return V,arr
    
def HPI(mdp):

    arr=np.zeros(mdp["num_states"])
    I=np.eye(mdp["num_states"])
    for i in range(mdp["num_states"]):
            
        target_first_value = i
        l=[lst for lst in mdp["transitions"] if lst[0] == target_first_value]
        arr[i]=l[0][1] 
    k=10
    while k>0:
        T=np.zeros((mdp["num_states"],mdp["num_states"]))
        R=np.zeros(mdp["num_states"])
        for i in range(mdp["num_states"]):
            z=0
            for j in range(mdp["num_states"]):
               l=[lst for lst in mdp["transitions"] if lst[0] == i and lst[1] == arr[i] and lst[2]== j] 
               #print(l)
               if bool(l):
                T[i][j]=l[0][4]
                z=z+l[0][4]*l[0][3]
            R[i]=z
        V_1=np.linalg.inv(I-mdp["discount"]*T)
        V=np.dot(V_1,R)
        a=I-mdp["discount"]*T
        #V=np.linalg.solve(a,R)
        #print(V)
        #print(arr)
        my_dict = {i: None for i in range(mdp["num_states"])}
        e=0.000001
        for i in range(mdp["num_states"]):
            v_temp=V[i]
            for j in range(mdp["num_actions"]):
                b=0
                l=[lst for lst in mdp["transitions"] if lst[0] == i and lst[1] == j] 
                for x in l:
                    s=x[2]
                    b=b+ x[4]*(x[3]+mdp["discount"]*V[s])
                    #print(i,b,V[i])
                if b-V[i]>e:
                    my_dict[i]=1
                if b>v_temp:
                    arr[i]=j
                    v_temp=b
        #k=k-1
        #print(my_dict)
        if all(value is None for value in my_dict.values()):
            break
    return V,arr
                

    

def main():
    mdp={"num_states":0, "num_actions":0,"end_state":[], "transitions": [], "type": "", "discount":0}
    file=open(mdp_path, "r")
    read=file.readlines()
    for line in read:
        x = line.strip().split()  
        
        if x[0]=="numStates":
            mdp["num_states"]=int(x[1])
        elif x[0]=="numActions":
            mdp["num_actions"]=int(x[1])
        elif x[0]=="end":
            mdp["end_state"]=x[1:]
        elif x[0]=="transition":
            s=int(x[1])
            a=int(x[2])
            s_dash=int(x[3])
            r=float(x[4])
            p=float(x[5])
            mdp["transitions"].append((s,a,s_dash,r,p))
        elif x[0]=="mdptype":
            mdp["type"]=x[1]
        elif x[0]=="discount":
            mdp["discount"]=float(x[1])
        
    if (policy != ''):
        
        pol=[]
        file=open(policy, "r")
        read=file.readlines()
        for line in read:
            x = line.strip().split()  
            pol.append(int(x[0]))
        I=np.eye(mdp["num_states"])
        T=np.zeros((mdp["num_states"],mdp["num_states"]))
        R=np.zeros(mdp["num_states"])
        for i in range(mdp["num_states"]):
            z=0
            for j in range(mdp["num_states"]):
               l=[lst for lst in mdp["transitions"] if lst[0] == i and lst[1] == pol[i] and lst[2]== j] 
               #print(l)
               if bool(l):
                T[i][j]=l[0][4]
                z=z+l[0][4]*l[0][3]
            R[i]=z
        V_1=np.linalg.inv(I-mdp["discount"]*T)
        V=np.dot(V_1,R)

        h=0
        
        for var in range(mdp["num_states"]):
            print(V[var],pol[var])  
            h=h+1 
            if h>=len(pol):
                break
        '''lp=LpProblem("MDP",LpMaximize)
        var_keys=np.arange(mdp["num_states"])
        x=LpVariable.dicts('Value_Functions',var_keys)       
        for i in range(mdp["num_states"]):
            c=pol[i]
            b=0
            target_first_value = i
            target_second_value = c
            l=[lst for lst in mdp["transitions"] if lst[0] == target_first_value and lst[1] == target_second_value]
            for j in l:
                if j[0]==i and j[1]==c:
                    b=b+j[4]*(j[3]+mdp["discount"]*x[j[2]])
            lp += x[i]==b
        status = lp.solve(PULP_CBC_CMD(msg=0))
        

        h=0
        
        for var in lp.variables():
            print(value(var),pol[h])  
            h=h+1 
            if h>=len(pol):
                break'''
    elif algo=='hpi':
        if int(mdp["end_state"][0])<0:

            a,b=HPI(mdp)
            for i in range(mdp["num_states"]):
                print(a[i],b[i])
            with open("output1.txt", "w") as file:
                for i in range(mdp["num_states"]):
                    print(a[i],b[i],file=file)   
        else:
            a,b=HPI_episodic(mdp)
            for i in range(mdp["num_states"]):
                print(a[i],b[i])
            with open("output1.txt", "w") as file:
                for i in range(mdp["num_states"]):
                    print(a[i],b[i],file=file)

   
    elif algo=='lp':

        
        lp=LpProblem("MDP",LpMinimize)
        var_keys=np.arange(mdp["num_states"])
        x=LpVariable.dicts('Value_Functions',var_keys,lowBound=None)
        a=0
        for i in range(mdp["num_states"]):
            a=a+x[i]
        #a=(-1)*a
        lp += a
        
        #print(mdp["end_state"])
        for i in range(mdp["num_states"]):
            if str(i) in mdp["end_state"]:
                lp+=(x[i]==0)
                continue
            for c in range(mdp["num_actions"]):
                b=0
                target_first_value = i
                target_second_value = c
                l=[lst for lst in mdp["transitions"] if lst[0] == target_first_value and lst[1] == target_second_value]
                if len(l)!=0:
                    
                    for j in l:
                        if j[0]==i and j[1]==c:
                            b=b+j[4]*(j[3]+mdp["discount"]*x[j[2]])
                    lp +=(x[i]>=b)

            
        #a=(-1)*a
        #lp += a
        #print("Parsed transitions:", mdp["transitions"][:10])  # Print first 10 transitions
        #print("Total transitions:", len(mdp["transitions"]))    
            #if i >= 5:  # Stop after printing 5 constraints
                #break
            #print(constraint)
        status = lp.solve(PULP_CBC_CMD(msg=0))
        #status = lp.solve(GLPK(msg=0))
        #print(lp.variables)
     
        values=[]
        for var in lp.variables():
            values.append(value(var))
        V_need = np.zeros(mdp["num_states"])
        for i in range(mdp["num_states"]):
            V_need[i]=value(x[i])
        #print(V_optimal)  
        #print(values[:5])
        actions=[]
        e=0.00001
        for i in range(mdp["num_states"]):
            if str(i) in mdp["end_state"]:
                actions.append(0)
            min=sys.float_info.max
            c_real=10000000
            for c in range(mdp["num_actions"]):
                #print("C is", c)
                b=0
                target_first_value = i
                target_second_value = c
                l=[lst for lst in mdp["transitions"] if lst[0] == target_first_value and lst[1] == target_second_value]
                for j in l:
                    b=b+j[4]*(j[3]+mdp["discount"]*V_need[j[2]])
                #print("A",abs(values[i]-b))
                d=abs(V_need[i]-b)
                if d<=min:
                    min=d
                    c_real=c
            actions.append(c_real)
        h=0
        #print(value(lp.variables))
        for i in range(mdp["num_states"]):
            print(V_need[i],actions[h])  
            h=h+1    
        #print("Constructed actions:", actions)
        #print("Length of actions:", len(actions))
        #actions = list(set(a for _, a, _, _, _ in mdp["transitions"]))
        #print("Extracted actions before deduplication:", actions)
        #print(mdp)
    
        #for i, (name, constraint) in enumerate(lp.constraints.items()):
            #if i >= 2000:  # Stop after printing 30 constraints
                #break
            #print(f"Constraint {i+1}: {constraint}")


if __name__ == '__main__':
    main()