'''
p3, mix gas
Yuan Ji
'''
import time
import os
import numpy as np
import random
import matplotlib.pyplot as plt
from copy import copy


#print(grid)
#plt.imshow(grid)
def successors(point,grid):
    existed=False
    dxlist=[-1,1,0,0]
    dylist=[0,0,-1,1]
    succ=[]
    xp=point[0]
    yp=point[1]
    for (dx,dy) in zip(dxlist,dylist):
        if (xp+dx)>-1 and (xp+dx)<len(grid) and yp+dy>-1 and yp+dy<len(grid[0]):
            if grid[xp+dx][yp+dy]==0:
                existed=True
                succ.append((xp+dx,yp+dy))
        
    return existed,succ

#1e8

def diffuse(interval,sample=24):
    #initialize
    grid=np.zeros((120,80),dtype=np.int)
    #suppose A=1 B=2, initialize
    for i in range(40):
        for j in range(80):
            grid[i][j]=1

    for i in range(80,120):
        for j in range(80):
            grid[i][j]=2
    time=interval*sample #whole time range
    grids=[]
    #temp=copy(grid)
    grids.append(copy(grid))
    
    for k in range(time):
        if (k+1)%interval==0:
            #print(k)
            temp=copy(grid)
            grids.append(temp)
        
        i=random.randint(0,119)
        j=random.randint(0,79)
        value=grid[i][j]
        
        if value!=0:
            existed,succ=successors((i,j),grid)
            if existed:
                suc=random.choice(succ)
                #print suc
                grid[suc[0]][suc[1]]=copy(value)
                grid[i][j]=0
        
    return grids
#part a and part b ##########################################################################
start=time.clock()
grids=diffuse(1500000)
end=time.clock()
print str(end-start), "seconds"

if not os.path.exists("p3ab/density_plot/densityalonglongside"):
        os.makedirs("p3ab/density_plot/densityalonglongside")
if not os.path.exists("p3ab/density-_plot/densityalongshortside"):
        os.makedirs("p3ab/density_plot/densityalongshortside")
if not os.path.exists("p3ab/grid_snapshots"):
        os.makedirs("p3ab/grid_snapshots")
#120-x, 80-y
for i,grid in enumerate(grids):

    #plot grid snapshot
    f1=plt.figure()
    plt.imshow(grid)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Gas snapshot"+str(i))
    plt.savefig("p3ab/grid_snapshots/snapshot"+str(i)+".pdf")
    
    plt.close(f1)
    
    
    #calculate linear density for A and B along x,y directions
    row_A=[]
    row_B=[]
    for j in range(120):
        row=[0,0] # of A and B
        for k in range(80):
            if grid[j][k]==1:
                row[0]+=1
            elif grid[j][k]==2:
                row[1]+=1
        row_A.append(row[0])
        row_B.append(row[1])
        
    f2=plt.figure()
    plt.plot(row_A,'.')
    plt.plot(row_B,'.')
    plt.legend(["A","B"],loc='upper right')
    plt.xlabel("y")
    plt.ylabel("density")
    plt.title("Density along y axis")
    plt.savefig("p3ab/density_plot/densityalonglongside/ydensity"+str(i)+".pdf")
    plt.close(f2)
    
    col_A=[]
    col_B=[]
    for j in range(80):
        #print j
        col=[0,0] # of A and B
        for k in range(120):
            if grid[k][j]==1:
                col[0]+=1
            elif grid[k][j]==2:
                col[1]+=1
        col_A.append(col[0])
        col_B.append(col[1])

    f3=plt.figure()
    plt.plot(col_A,'.')
    plt.plot(col_B,'.')
    plt.legend(["A","B"],loc='upper right')
    plt.xlabel("x")
    plt.ylabel("density")
    plt.title("Density along x axis")
    plt.savefig("p3ab/density_plot/densityalongshortside/xdensity"+str(i)+".pdf")
    plt.close(f3)

############part c##############################################################
repeats=100
collection=[]

start=time.clock()
for r in range(repeats):
    collection.append(diffuse(1500000))
    #collection.append(diffuse(100000))



if not os.path.exists("p3c/density_plot/densityalonglongside"):
        os.makedirs("p3c/density_plot/densityalonglongside")
if not os.path.exists("p3c/density_plot/densityalongshortside"):
        os.makedirs("p3c/density_plot/densityalongshortside")
if not os.path.exists("p3c/grid_snapshots"):
        os.makedirs("p3c/grid_snapshots")

row_A_aver2=[]
row_B_aver2=[]
col_A_aver2=[]
col_B_aver2=[]
for n,c in enumerate(collection):
    row_A_aver=[]
    row_B_aver=[]
    col_A_aver=[]
    col_B_aver=[]
    for i,grid in enumerate(c):# snapshots--time
        #calculate linear density for A and B along x,y directions
        row_A=[]
        row_B=[]
        for j in range(120):
            row=[0,0] # of A and B
            for k in range(80):
                if grid[j][k]==1:
                    row[0]+=1
                elif grid[j][k]==2:
                    row[1]+=1
            row_A.append(row[0])
            row_B.append(row[1])
        row_A_aver.append(row_A)
        row_B_aver.append(row_B)
        
        
        col_A=[]
        col_B=[]
        for j in range(80):
            #print j
            col=[0,0] # of A and B
            for k in range(120):
                if grid[k][j]==1:
                    col[0]+=1
                elif grid[k][j]==2:
                    col[1]+=1
            col_A.append(col[0])
            col_B.append(col[1])
        col_A_aver.append(col_A)
        col_B_aver.append(col_B)
    row_A_aver2.append(row_A_aver)
    row_B_aver2.append(row_B_aver)
    col_A_aver2.append(col_A_aver)
    col_B_aver2.append(col_B_aver)
row_A_average=np.mean(row_A_aver2,axis=0)
row_B_average=np.mean(row_B_aver2,axis=0)
col_A_average=np.mean(col_A_aver2,axis=0)
col_B_average=np.mean(col_B_aver2,axis=0)

end=time.clock()
print str(end-start), "seconds"
'''
plot and check result
'''
for i,(a,b) in enumerate(zip(row_A_average, row_B_average)):
    f2=plt.figure()
    if int(np.sum(a))!=3200 or int(np.sum(b))!=3200:
        print "wrong",np.sum(a),np.sum(b)
    #print "sanpshot",i,"A # sum",np.sum(a),"should be 3200"  #40*80
    #print "sanpshot",i,"B # sum",np.sum(b),"should be 3200"
    plt.plot(a,'.')
    plt.plot(b,'.')
    plt.legend(["A","B"],loc='upper right')
    plt.xlabel("y")
    plt.ylabel("density")
    plt.title("Density along y axis")
    plt.savefig("p3c/density_plot/densityalonglongside/ydensity"+str(i)+".pdf")
    plt.close(f2)
    
for i,(a,b) in enumerate(zip(col_A_average, col_B_average)):
    f3=plt.figure()
    if int(np.sum(a))!=3200 or int(np.sum(b))!=3200:
        print "wrong",np.sum(a),np.sum(b)
    #print "sanpshot",i,"A # sum",np.sum(a),"should be 3200"  #40*80
    #print "sanpshot",i,"B # sum",np.sum(b),"should be 3200"
    plt.plot(a,'.')
    plt.plot(b,'.')
    plt.legend(["A","B"],loc='upper right')
    plt.xlabel("x")
    plt.ylabel("density")
    plt.title("Density along x axis")
    plt.savefig("p3c/density_plot/densityalongshortside/xdensity"+str(i)+".pdf")
    plt.close(f3)
