path='rmsd_all.dat'
dat=[]
count=0
with open(path) as f:
    for line in f:
        data=line.split()
        data[0]=count
        count=count+1
        dat.append(str(data[0])+' '+str(data[1]))
        #dat.append(str(data[0])+' '+str(data[1])+' '+str(data[2])+' '+str(data[3]))
print(dat)

f = open('rmsd_all.txt','w') 
for i in dat:
    print(i)
    f.write(i+'\n')
f.close()
