path='rmsd.dat'  # path

# load data as a list
count=0
dat=[]
with open(path) as f:
    for line in f:
        data=line.split()
        dat.append(float(data[1]))
        #dat.append(str(data[0])+' '+str(data[1])+' '+str(data[2])+' '+str(data[3]))
#print(min(dat))  # min 1.2034075260162354 max3.4252567291259766

# histogram
num_bin=20
n, bins, patches = plt.hist(dat, num_bin, facecolor='green',alpha=0.75) # n: number of value in a range
plt.title('Histogram of rmsd value distribution')
plt.xlabel('rmsd value')
plt.ylabel('number')
plt.axis([1, 3.5, 0, 600])
plt.show()

# average
count=0
sum=0
average=[]
for i in dat:
    if count%10==0:
        sum=sum+i
        ave=sum/10
        average.append(ave)
        sum=0
        count=count+1
    else:
        count=count+1
        sum=sum+i
#print(max(average))
#print(len(average))

# histogram
num_bin=20
n, bins, patches = plt.hist(average, num_bin, facecolor='orange',alpha=0.75) # n: number of value in a range
plt.title('Histogram of rmsd average distribution')
plt.xlabel('the average of rmsd value')
plt.ylabel('number')
plt.axis([1, 3.5, 1, 90])
plt.show()
