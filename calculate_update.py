# %load calculate.py
# %load read_calculate.py
#!/usr/bin/env python
import math
import sys

# Read PDB File
class Atom:
    def __init__(self, line):
        self.serial = int(line[6:11])
        self.name = line[11:16].strip()
        self.altLoc = line[16:17].strip()
        self.resName = line[17:20]
        self.chainID = line[21:22]
        self.resSeq = int(line[22:26])
        self.iCode = line[26:27].strip()
        self.x = float(line[30:38])
        self.y = float(line[38:46])
        self.z = float(line[46:54])
        self.occupancy = line[54:60].strip()
        self.tempFactor = line[60:66].strip()
        self.element = line[76:78].strip()
        self.charge = line[78:80].strip()
        if self.occupancy: self.occupancy = float(self.occupancy)
        if self.tempFactor: self.tempFactor = float(self.tempFactor)

    def __getitem__(self, key):
        return self.__dict__[key]

class PDB:
    def __init__(self, file):
        self.file = 'ligandrm.pdb'
        self.atoms = []
        self.parse()

    def parse(self):
        MODEL = None
        f = open(self.file, 'r')
        for line in f.readlines():
            if line.startswith('MODEL'): MODEL = int(line.split()[1])
            if line.startswith('ATOM'):
                atom = Atom(line)
                atom.MODEL = MODEL
                self.atoms.append(atom)
        f.close()

    def get_atoms(self, to_dict=True):
        """Return a list of all atoms.

        If to_dict is True, each atom is represented as a dictionary.
        Otherwise, a list of Atom objects is returned."""
        if to_dict: return [x.__dict__ for x in self.atoms]
        else: return self.atoms

    def get_model(self, model_num, to_dict=True):
        """Return all atoms where MODEL == model_num"""
        model_atoms = [x for x in self.atoms if x.MODEL == model_num]
        if to_dict:
            return [atom.__dict__ for atom in model_atoms]
        else:
            return model_atoms

# read structure file(.rtf) get info of bond
def loadDatadet(infile):
    f=open(infile,'r')
    sourceInLine=f.readlines()
    dataset=[]
    for line in sourceInLine:
        temp1=line.strip('\n')
        print(temp1)
        temp2=temp1.split()[1:3]
        dataset.append(temp2)
    return dataset
#print(structure)

# read structure file(.rtf) get info of id
def loadDatadet_id(infile):
    f=open(infile,'r')
    sourceInLine=f.readlines()
    ids={}
    for line in sourceInLine:
        temp1=line.strip('\n')
        print(temp1.split()[0]+' '+temp1.split()[1]+' '+temp1.split()[2])
        temp2=temp1.split()[1:3]
        ids[temp2[0]]=temp2[1]
    return ids
#print(structure)


# Calculate Steps Here!!!
# Bond
def dist (A, B):
    xdif = (float(A[0]) - float(B[0]))**2
    #print(xdif)
    ydif = (float(A[1]) - float(B[1]))**2
    #print(ydif)
    zdif = (float(A[2]) - float(B[2]))**2
    #print(zdif)
    return math.sqrt(xdif + ydif + zdif)

# Angle
def ang(A, B, C):
    xba = A[0] - B[0]
    yba = A[1] - B[1]
    zba = A[2] - B[2]
    xbc = C[0] - B[0]
    ybc = C[1] - B[1]
    zbc = C[2] - B[2]
    dot = (xba*xbc) + (yba*ybc) + (zba*zbc)
    d_ab = dist(A, B)
    d_bc = dist(B, C)
    return (math.acos(dot/(d_ab*d_bc))) * 180 / math.pi

# dihedral_angle
def dihe(A, B, C, D):
    xba = A[0] - B[0]
    yba = A[1] - B[1]
    zba = A[2] - B[2]
    xbc = C[0] - B[0]
    ybc = C[1] - B[1]
    zbc = C[2] - B[2]
    xcb = B[0] - C[0]
    ycb = B[1] - C[1]
    zcb = B[2] - B[2]
    xcd = D[0] - C[0]
    ycd = D[1] - C[1]
    zcd = D[2] - C[2]

    # Cross vectors
    Cbabc_x = (yba * zbc) - (zba * ybc)
    Cbabc_y = (zba * xbc) - (xba * zbc)
    Cbabc_z = (xba * ybc) - (yba * xbc)

    Ccbcd_x = (ycb * zcd) - (zcb * ycd)
    Ccbcd_y = (zcb * xcd) - (xcb * zcd)
    Ccbcd_z = (xcb * ycd) - (ycb * xcd)

    dot = (Cbabc_x * Ccbcd_x) + (Cbabc_y * Ccbcd_y) + (Cbabc_z * Ccbcd_z)
    Den = math.sqrt(Cbabc_x**2 + Cbabc_y**2 + Cbabc_z**2) * math.sqrt(Ccbcd_x**2     + Ccbcd_y**2 + Ccbcd_z**2 )

    i = yba * zcd - zba * ycd
    j = zba * xcd - xba * zcd
    k = xba * ycd - yba * xcd
    f = i * xbc + j * ybc + k * zbc

    if f >= 0:
        return (math.acos(dot / Den)) * 180 / math.pi
    else:
        return -1 * ((math.acos(dot / Den)) * 180 / math.pi)

# Calculate Energy
def loadDatadet_4_3(infile):
    f=open(infile,'r')
    sourceInLine=f.readlines()
    dataset=[]
    Bond={}
    Angle={}
    Dihedral={}
    id_name=[]
    for line in sourceInLine:
        temp1=line.strip('\n')
        first=temp1.split()[0]
        if first=='BONDS':
            sign=1
            continue
        elif first=='ANGLES':
            sign=2
            continue
        elif first=='DIHEDRALS':
            sign=3
            continue
        if sign==1: # bond
            temp2=temp1.split()[0:4]
            Bond[temp2[0]+temp2[1]]=temp2[2:4]
            id_name.append(temp2[0]+temp2[1])
        elif sign==2:
            temp2=temp1.split()[0:5]
            Angle[temp2[0]+temp2[1]+temp2[2]]=temp2[3:5]
            id_name.append(temp2[0]+temp2[1]+temp2[2])
        elif sign==3:
            temp2=temp1.split()[0:7]
            #print(temp2)
            if temp2[0]+temp2[1]+temp2[2]+temp2[3] in Dihedral.keys():
                values=[i for i in Dihedral[temp2[0]+temp2[1]+temp2[2]+temp2[3]]]
                for i in range(4,7):
                    temp2[i]=float(temp2[i])+values[i-4]
                tmp=[float(i) for i in temp2[4:7]]
                Dihedral[temp2[0]+temp2[1]+temp2[2]+temp2[3]]=tmp
            else:
                tmp=[float(i) for i in temp2[4:7]]
                Dihedral[temp2[0]+temp2[1]+temp2[2]+temp2[3]]=tmp
            id_name.append(temp2[0]+temp2[1]+temp2[2]+temp2[3])
    return Bond,Angle,Dihedral,id_name

def loadDatadet_nonbond(infile):
    f=open(infile,'r')
    sourceInLine=f.readlines()
    nonbond={}
    for line in sourceInLine:
        temp1=line.strip('\n')
        first=temp1.split()
        #print(first)
        try:
            num=float(first[5])
            nonbond[first[0]]=[[float(first[2]),float(first[3])],[float(first[5]),float(first[6])]] # {id:[eps,Rmin/2]}
        except:
            nonbond[first[0]]=[[float(first[2]),float(first[3])]]
    return nonbond

if __name__ == '__main__':
    infile='par_all36_cgenff.txt'
    Bond,Angle,Dihedral,id_name=loadDatadet_4_3(infile)
    #print(Bond['CG331CG321'])
    print('===============================================================')
    print('====================    {ATOM : ID}    ========================')
    print('===============================================================')
    ids='id.txt'
    ids=loadDatadet_id(ids)
    print('===============================================================')
    print('=====================    STRUCTURE    =========================')
    print('===============================================================')
    structure='bond.txt'
    structure=loadDatadet(structure)
    pdb = PDB(sys.argv[0])
    atoms = pdb.get_atoms(to_dict=False) # if to_dict == True, atoms is the List of Atom dictionaries.
    pdb={}
    print('===============================================================')
    print('=======================    PDB    =============================')
    print('===============================================================')
    for atom in atoms:
        pdb[atom.name]=[atom.x,atom.y,atom.z]
        print(atom.serial, atom.name, atom.x, atom.y, atom.z, atom.element)
    #print(pdb)


    # serial atom indices for bond, angle, and dihedral
    # read 4 atom and calculate its bond, angle and dihedral
    print('===============================================================')
    print('=======================    BOND    ============================')
    print('===============================================================')
    sum=0
    for i in structure:
            atm1=i[0]
            atm2=i[1]
            atm1_v=pdb[atm1]
            atm2_v=pdb[atm2]
            #print(atm1_v)
            #print(atm2_v)
            bond=dist(atm1_v,atm2_v)
            print('the bond of '+atm1+' and '+atm2+' is : '+str(bond))
            id1=ids[atm1]
            id2=ids[atm2]
            id=id1+id2
            if id not in id_name:
                id=id2+id1
            kb=float(Bond[id][0])
            b0=float(Bond[id][1])
            Vbond=kb*(math.pow((bond-b0),2))
            sum=sum+Vbond
            print('(Vbond)the bond energy of '+atm1+' and '+atm2+' is : '+str(Vbond))
            print('\t')
    print('the sum of bond energy is: '+str(sum))
    print('===============================================================')
    print('=======================    ANGLE    ===========================')
    print('===============================================================')
    angle_structure=[]
    sum=0
    for i in range (len(structure)):
        for j in range(i+1,len(structure)):
            if structure[i][1]==structure[j][0]: # 1-2 2-3
                atm1=structure[i][0]
                atm2=structure[i][1]
                atm3=structure[j][1]
                atm1_v=pdb[atm1]
                atm2_v=pdb[atm2]
                atm3_v=pdb[atm3]
                angle=ang(atm1_v,atm2_v,atm3_v)
                print('the angle of '+atm1+' ,'+atm2+' and '+atm3+' is : '+str(angle))
                id1=ids[atm1]
                id2=ids[atm2]
                id3=ids[atm3]
                id=id1+id2+id3
                if id not in id_name:
                    id=id3+id2+id1
                ktheta=float(Angle[id][0])
                theta0=float(Angle[id][1])
                rad=math.pow((math.pi/180),2)
                Vangle=(ktheta*(math.pow((angle-theta0),2)))*rad
                sum=sum+Vangle
                print('(Vangle)the angle energy of '+atm1+' ,'+atm2+' and '+atm3+' is : '+str(Vangle))
                print('\t')
                angle_structure.append([atm1,atm2,atm3])
            elif structure[i][0]==structure[j][0]: # 1-2 1-3
                atm1=structure[j][1] #3
                atm2=structure[i][0] #1
                atm3=structure[i][1] #2
                atm1_v=pdb[atm1]
                atm2_v=pdb[atm2]
                atm3_v=pdb[atm3]
                angle=ang(atm1_v,atm2_v,atm3_v)
                print('the angle of '+atm1+' ,'+atm2+' and '+atm3+' is : '+str(angle))
                id1=ids[atm1]
                id2=ids[atm2]
                id3=ids[atm3]
                id=id1+id2+id3
                if id not in id_name:
                    id=id3+id2+id1
                ktheta=float(Angle[id][0])
                theta0=float(Angle[id][1])
                rad=math.pow((math.pi/180),2)
                Vangle=(ktheta*(math.pow((angle-theta0),2)))*rad
                sum=sum+Vangle
                print('(Vangle)the angle energy of '+atm1+' ,'+atm2+' and '+atm3+' is : '+str(Vangle))
                print('\t')
                angle_structure.append([atm1,atm2,atm3])
            else:
                continue
    #print(angle_structure)

    print('The number of angle is: '+str(len(angle_structure)))
    print('The sum of angle is '+str(sum))
    print('===================================================================')
    print('========================    DIHEDRAL    ===========================')
    print('===================================================================')
    #print(angle_structure)
    dihedral_structure=[]
    sum=0
    for i in range(len(angle_structure)):
        for j in range(i+1,len(angle_structure)): # c1 c2 c3 - h1 c1 c2
            if angle_structure[i][0]==angle_structure[j][1] and angle_structure[i][1]==angle_structure[j][2]:
                atm1=angle_structure[j][0] #h1
                atm2=angle_structure[i][0] #c1
                atm3=angle_structure[i][1] #c2
                atm4=angle_structure[i][2] #c3
                atm1_v=pdb[atm1]
                atm2_v=pdb[atm2]
                atm3_v=pdb[atm3]
                atm4_v=pdb[atm4]
                dihedral=dihe(atm1_v,atm2_v,atm3_v,atm4_v)
                print('the dihedral of '+atm1+' ,'+atm2+' ,'+atm3+' and '+atm4+' is : '+str(dihedral))
                dihedral_structure.append([atm1,atm2,atm3,atm4])
                id1=ids[atm1]
                id2=ids[atm2]
                id3=ids[atm3]
                id4=ids[atm4]
                id=id1+id2+id3+id4
                if id not in id_name:
                    id=id4+id3+id2+id1
                kx=float(Dihedral[id][0])
                n=float(Dihedral[id][1])
                e=float(Dihedral[id][2])
                Vdihedral=kx*(1+math.cos((n*dihedral-e)*(math.pi/180)))
                sum=sum+Vdihedral
                print('(Vdihedral)the dihedral energy of '+atm1+' ,'+atm2+' ,'+atm3+' and '+atm4+' is : '+str(Vdihedral))
                print('\t')
            # h1 c1 c2 - c1 c2 h4
            elif angle_structure[i][1]==angle_structure[j][0] and angle_structure[i][2]==angle_structure[j][1]:
                atm1=angle_structure[i][0] #h1
                atm2=angle_structure[j][0] #c1
                atm3=angle_structure[j][1] #c2
                atm4=angle_structure[j][2] #h4
                atm1_v=pdb[atm1]
                atm2_v=pdb[atm2]
                atm3_v=pdb[atm3]
                atm4_v=pdb[atm4]
                dihedral=dihe(atm1_v,atm2_v,atm3_v,atm4_v)
                print('the dihedral of '+atm1+' ,'+atm2+' ,'+atm3+' and '+atm4+' is : '+str(dihedral))
                dihedral_structure.append([atm1,atm2,atm3,atm4])
                id1=ids[atm1]
                id2=ids[atm2]
                id3=ids[atm3]
                id4=ids[atm4]
                id=id1+id2+id3+id4
                if id not in id_name:
                    id=id4+id3+id2+id1
                kx=float(Dihedral[id][0])
                n=float(Dihedral[id][1])
                e=float(Dihedral[id][2])
                Vdihedral=kx*(1+math.cos((n*dihedral-e)*(math.pi/180)))
                sum=sum+Vdihedral
                print('(Vdihedral)the dihedral energy of '+atm1+' ,'+atm2+' ,'+atm3+' and '+atm4+' is : '+str(Vdihedral))
                print('\t')
            else:
                continue
    #print(dihedral_structure)           
    print('The number of dihedral is: '+str(len(dihedral_structure)))
    print('The sum of Vdihedral is: '+str(sum))
    print('=======================================================================')
    print('======================    Nonbonded Energy    =========================')
    print('=======================================================================')
    # Nonbonded energy
    infile='nonbonded.txt'
    nonbond_dict=loadDatadet_nonbond(infile)
    nonbond=[]
    atom=[atom.name for atom in atoms]
    bonds=[]
    #print(structure)
    #print(angle_structure)
    ### all atoms
    for i in range(len(atom)):
        for j in range(i+1,len(atom)):
            bonds.append([atom[i],atom[j]])
    #print(len(bonds))
    nonbonds=[]
    #print(structure)
    for i in structure:
        for j in bonds:
            if j[0] in i and j[1] in i:
                bonds.remove(j)
            else:
                continue
    for i in angle_structure:
        for j in bonds:
            if j[0] in i and j[1] in i:
                bonds.remove(j)
            else:
                continue
    
    qs={'C1':-0.270,'C2':-0.180,'C3':-0.181,'C4':0.051,'H1':0.090,'H2':0.090,'H3':0.090,'H4':0.090,'H5':0.090,'H6':0.090,'H7':0.090,'H8':0.090,'H9':0.090,'O':-0.650,'H10':0.420}
    sum_lj=0
    sum_c=0
    #print(dihedral_structure)
    indih=[]
    for i in dihedral_structure:
        indih.append([i[0],i[3]])
        try:
            bonds.remove([i[0],i[3]])
        except:
            bonds.remove([i[3],i[0]])
    # in dihedral read another two line
    for i in indih:
        atom1=i[0]
        atom2=i[1]
        co_atom1=pdb[atom1]
        co_atom2=pdb[atom2]
        rab=dist(co_atom1,co_atom2)
        id1=ids[atom1]
        id2=ids[atom2]
        try:
            Ra_2=nonbond_dict[id1][1]
            Ra_2=Ra_2[1]
        except:
            Ra_2=nonbond_dict[id1][0]
            Ra_2=Ra_2[1]
        try:
            Rb_2=nonbond_dict[id2][1]
            Rb_2=Rb_2[1]
        except:
            Rb_2=nonbond_dict[id2][0]
            Rb_2=Rb_2[1]
        try:
            eps_a=nonbond_dict[id1][1]
            eps_a=eps_a[0]
        except:
            eps_a=nonbond_dict[id1][0]
            eps_a=eps_a[0]
        try:
            eps_b=nonbond_dict[id2][1]
            eps_b=eps_b[0]
        except:
            eps_b=nonbond_dict[id2][0]
            eps_b=eps_b[0]
        Rab_2=Ra_2+Rb_2
        eps_ab=math.sqrt(eps_a*eps_b)
        U_lj=eps_ab*(math.pow(Rab_2/rab,12)-2*math.pow(Rab_2/rab,6))
        U_coul=332*((qs[atom1]*qs[atom2])/rab)
        sum_lj=sum_lj+U_lj
        sum_c=sum_c+U_coul
        print('U_lj of '+ atom1+'and '+atom2+' is: '+str(U_lj))
        print('U_coul of '+id1+'and '+id2+' is: '+str(U_coul))
        print('\t')
    # not in dihedral just read the first two 
    for i in bonds:
        atom1=i[0]
        atom2=i[1]
        co_atom1=pdb[atom1]
        co_atom2=pdb[atom2]
        rab=dist(co_atom1,co_atom2)
        id1=ids[atom1]
        id2=ids[atom2]
        Ra_2=nonbond_dict[id1][0]
        Ra_2=Ra_2[1]
        Rb_2=nonbond_dict[id2][0]
        Rb_2=Rb_2[1]
        Rab_2=Ra_2+Rb_2
        eps_a=nonbond_dict[id1][0]
        eps_a=eps_a[0]
        eps_b=nonbond_dict[id2][0]
        eps_b=eps_b[0]
        eps_ab=math.sqrt(eps_a*eps_b)
        U_lj=eps_ab*(math.pow(Rab_2/rab,12)-2*math.pow(Rab_2/rab,6))
        U_coul=332*((qs[atom1]*qs[atom2])/rab)
        sum_lj=sum_lj+U_lj
        sum_c=sum_c+U_coul
        print('U_lj of '+ atom1 +'and '+atom2+' is: '+str(U_lj))
        print('U_coul of '+atom1 +'and '+atom2+' is: '+str(U_coul))
        print('\t')

print('the sum of Lennard-Jones potential is: '+ str(sum_lj))
print('the sum of Coulombic interaction energy is: '+str(sum_c))

