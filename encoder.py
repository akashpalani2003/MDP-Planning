import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument('--gridworld', help='mdp', type=str, default='dumy_feature')
args = parser.parse_args()
grid_path=args.gridworld

def main():
    
    file=open(grid_path, "r")
    #line_count = sum(1 for _ in enumerate(file))
    read=file.readlines()
    line_count=0
    for line in read:
        x = line.strip().split()  
        #print(x)
        l=len(x)
        line_count=line_count+1
    map=np.zeros((line_count,l))
    file=open(grid_path, "r")
    read=file.readlines()
    i=0
    num_states=0
    num_actions=4
    discount=0.95
    mdp_type='episodic'

    for line in read:
        line = line.strip().split()
        #print(line)
        for j in range(l):
            if line[j]=='W':
                map[i][j]=0
            elif line[j]=='_':
                map[i][j]=1
                num_states+=1
            elif line[j]=='s':
                map[i][j]=2
                num_states+=1
                start=l*i+j
            elif line[j]=='k':
                map[i][j]=3
                num_states+=1
                key=(i,j)
            elif line[j]=='d':
                map[i][j]=4
                num_states+=1
                door=(i,j)
            elif line[j]=='g':
                map[i][j]=5
                end_state=(i,j)
                num_states+=1
        i=i+1
    
    
    dict={"states":[],"actions":[0,1,2,3],"start":start,"key":key,"door":door}
    for i in range(line_count):
        for j in range(l):
            if map[i][j]==1 or map[i][j]==2 or map[i][j]==3 or map[i][j]==4:
                dict["states"].append((i,j))
    W=0
    t=[]
    for x in dict["states"]:
        
        for y in range(4):# 0 is up, 1 is right, 2 is down, 3 is left
            

            if y==0:
                for z in range(4):
                    if z==0:
                        if (map[x[0]-1][x[1]]!=W):
                            if(map[x[0]-2][x[1]]!=W):
                                if(map[x[0]-3][x[1]]!=W):
                                    t.append(((x,y),z,((x[0]-1,x[1]),y),0,0.5))
                                    t.append(((x,y),z,((x[0]-2,x[1]),y),0,0.3))
                                    t.append(((x,y),z,((x[0]-3,x[1]),y),0,0.2))
                                else:
                                    t.append(((x,y),z,((x[0]-1,x[1]),y),0,0.5))
                                    t.append(((x,y),z,((x[0]-2,x[1]),y),0,0.5))
                            else:
                                t.append(((x,y),z,((x[0]-1,x[1]),y),0,1))
                    elif z==1:
                        t.append(((x,y),z,((x[0],x[1]),y+3),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y+2),0,0.1))
                    elif z==2:
                        t.append(((x,y),z,((x[0],x[1]),y+1),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y+2),0,0.1))
                    else:
                        t.append(((x,y),z,((x[0],x[1]),y+2),0,0.8))
                        t.append(((x,y),z,((x[0],x[1]),y+1),0,0.1))
                        t.append(((x,y),z,((x[0],x[1]),y+3),0,0.1))
            elif y==1:#right
                for z in range(4):
                    if z==0:
                        

                        if (map[x[0]][x[1]+1]!=W):
                            if(map[x[0]][x[1]+2]!=W):
                                
                                if(map[x[0]][x[1]+3]!=W):
                                    t.append(((x,y),z,((x[0],x[1]+1),y),0,0.5))
                                    t.append(((x,y),z,((x[0],x[1]+2),y),0,0.3))
                                    t.append(((x,y),z,((x[0],x[1]+3),y),0,0.2))
                                else:
                                    t.append(((x,y),z,((x[0],x[1]+1),y),0,0.5))
                                    t.append(((x,y),z,((x[0],x[1]+2),y),0,0.5))
                            else:
                                t.append(((x,y),z,((x[0],x[1]+1),y),0,1))
                    elif z==1:
                        t.append(((x,y),z,((x[0],x[1]),y-1),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y+2),0,0.1))
                    elif z==2:
                        t.append(((x,y),z,((x[0],x[1]),y+1),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y+2),0,0.1))
                    else:
                        t.append(((x,y),z,((x[0],x[1]),y+2),0,0.8))
                        t.append(((x,y),z,((x[0],x[1]),y+1),0,0.1))
                        t.append(((x,y),z,((x[0],x[1]),y-1),0,0.1))

            elif y==2:#down
                for z in range(4):
                    if z==0:
                        if (map[x[0]+1][x[1]]!=W):
                            if(map[x[0]+2][x[1]]!=W):
                                if(map[x[0]+3][x[1]]!=W):
                                    t.append(((x,y),z,((x[0]+1,x[1]),y),0,0.5))
                                    t.append(((x,y),z,((x[0]+2,x[1]),y),0,0.3))
                                    t.append(((x,y),z,((x[0]+3,x[1]),y),0,0.2))
                                else:
                                    t.append(((x,y),z,((x[0]+1,x[1]),y),0,0.5))
                                    t.append(((x,y),z,((x[0]+2,x[1]),y),0,0.5))
                            else:
                                t.append(((x,y),z,((x[0]+1,x[1]),y),0,1))
                    elif z==1:
                        t.append(((x,y),z,((x[0],x[1]),y-1),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y-2),0,0.1))
                    elif z==2:
                        t.append(((x,y),z,((x[0],x[1]),y+1),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y-2),0,0.1))
                    else:
                        t.append(((x,y),z,((x[0],x[1]),y-2),0,0.8))
                        t.append(((x,y),z,((x[0],x[1]),y-1),0,0.1))
                        t.append(((x,y),z,((x[0],x[1]),y+1),0,0.1))

            elif y==3:#left
                for z in range(4):
                    if z==0:
                        if (map[x[0]][x[1]-1]!=W):
                            if(map[x[0]][x[1]-2]!=W):
                                if(map[x[0]][x[1]-3]!=W):
                                    t.append(((x,y),z,((x[0],x[1]-1),y),0,0.5))
                                    t.append(((x,y),z,((x[0],x[1]-2),y),0,0.3))
                                    t.append(((x,y),z,((x[0],x[1]-3),y),0,0.2))
                                else:
                                    t.append(((x,y),z,((x[0],x[1]-1),y),0,0.5))
                                    t.append(((x,y),z,((x[0],x[1]-2),y),0,0.5))
                            else:
                                t.append(((x,y),z,((x[0],x[1]-1),y),0,1))
                    elif z==1:
                        t.append(((x,y),z,((x[0],x[1]),y-1),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y-2),0,0.1))
                    elif z==2:
                        t.append(((x,y),z,((x[0],x[1]),y-3),0,0.9))
                        t.append(((x,y),z,((x[0],x[1]),y-2),0,0.1))
                    else:
                        t.append(((x,y),z,((x[0],x[1]),y-2),0,0.8))
                        t.append(((x,y),z,((x[0],x[1]),y-3),0,0.1))
                        t.append(((x,y),z,((x[0],x[1]),y-1),0,0.1))


    if any(3 in row for row in map):
        target_value = key

        for i in range(len(t)):
            if t[i][2][0] == key:  
       
                t[i] = (((t[i][0][0][0], t[i][0][0][1]),t[i][0][1]), t[i][1], ((t[i][2][0][0], t[i][2][0][1]),t[i][2][1]), 1000, t[i][4])
    else:
        target_value = key

        for i in range(len(t)):
            if t[i][2][0] == door:  
       
                t[i] = (((t[i][0][0][0], t[i][0][0][1]),t[i][0][1]), t[i][1], ((t[i][2][0][0], t[i][2][0][1]),t[i][2][1]), 1000, t[i][4])
    with open("output.txt", "w") as file:
        print("numStates", num_states, file=file)
        print("numActions 4", file=file)
        print("end", end_state, file=file)
        for i in range(len(t)):
            print("transition", end=' ', file=file)
            for j in range(5):
                print(t[j],end=' ',file=file)
            print("\n",file=file)
        print("mdptype episodic", file=file)
        print("discount", 0.95, file=file)
  
    #print("numStates",num_states)
    #print("numActions 4")
    #print("end",end_state)
    #for i in range(len(t)):
        #print("transition",t[i])
    #print("mdptype episodic")
    #print("discount", 0.95)









if __name__ == '__main__':
    main()