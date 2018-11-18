path='rmsd.dat'
dat=[]
count=0
with open(path) as f:
    for line in f:
        data=line.split()
        data[0]=count
        count=count+1
        dat.append(str(data[0])+' '+str(data[1]))
print(dat)

f = open('rmsd_new.txt','w') 
for i in dat:
    print(i)
    f.write(i+'\n')
f.close()
