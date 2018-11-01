# %load data_preprocess.py
import json
import os, sys
import re

# read all file names in a folder
def read_file(path):
    file_name=[]
    dirs=os.listdir(path)
    for file in dirs:
        if file=='.DS_Store'or file=='.ipynb_checkpoints'or file=='Untitled.ipynb':
            continue
        file_name.append(file)
    return file_name

# read all content in all files of a folder
def read_folder(path):
    name=read_file(path)
    list=[]
    dict={}
    for i in name:
        path1=path+'/'+i
        names=read_file(path1)
        #list.append(names)
        dict2={}
        for j in names:
            path2=path1+'/'+j
            json_data=open(path2).read()
            data = json.loads(json_data)
            dict2[j]=data
        dict[i]=dict2
    return dict

# mid_sentence
# generate two dict which contain ids with its mention
path='/projects/blstm/Jiaxin_Liu/data/mention_id/mid_sentence'
id_mentions=read_folder(path)
#print(id_mentions)
#print(id_mentions)
products=[i for i in id_mentions.keys()]
neg_id_mention={}
pos_id_mention={}
id_mention={}
for i in products:
    label=[j for j in id_mentions[i].keys()]  # ['neg.json','pos.json']
    # neg
    neg_pair_id=id_mentions[i][label[0]] # ['id':'mention',....]
    se=[i for i in neg_pair_id.values()]
    for k in neg_pair_id.keys():
        neg_id_mention[k]=neg_pair_id[k]
    pos_pair_id=id_mentions[i][label[1]] # ['id':'mention',....]
    for k in pos_pair_id.keys():
        pos_id_mention[k]=pos_pair_id[k]
#i=[i for i in neg_id_mention.keys()]
#j=[i for i in pos_id_mention.keys()]
#print(len(i+j))



# pair_label
#path='/projects/blstm/Jiaxin_Liu/data/mention_id/pair_label'
#pair_label=read_folder(path)

# read all mention ids into a list
# there are two lists: pos_id(2128) and neg_id(5912)
path='/projects/blstm/Jiaxin_Liu/data/mention_id/pair_mid'
pair_mid=read_folder(path)
products=[i for i in pair_mid.keys()] # name of products
#print(products)
neg_id=[]
pos_id=[]
for i in products:
    label=[j for j in pair_mid[i].keys()]  # ['neg.json','pos.json']
    # neg
    neg_pair_id=pair_mid[i][label[0]] # ['id':'['id1',id2]',....]
    for k in neg_pair_id.values():
        for w in k:
            neg_id.append(w) # ['id1','id2']
    # pos
    pos_pair_id=pair_mid[i][label[1]]
    for k in pos_pair_id.values():
        for w in k:
            pos_id.append(w)
#print(len(pos_id))
#print(len(neg_id))
# [['a7d8e305d570d95f2e66cc869353dc9a.(15, 17).Canon', 'he larger lens of the g3 gives better picture quality in low light and the <e1> 4 times </e11> optical <e2> zoom </e22> gets you just that much close', '+(e1, e2)']]
# generate two list contain all info we need
# [['id','mention','relation'],['id','mention','relation']]
dataset=[]
for i in neg_id:
    pos=re.findall(r'[(](.*?)[)]', i) # position of two words
    pos=pos[0].split(',')
    mention=neg_id_mention[i]
    men_nopunc=re.findall(r'\w+\-?\w+\-?\w+|\'?\w+',mention) # a list contain all words in mentions(omit punctuations)
    p1=int(pos[0])
    p2=int(pos[1])
    if p1>p2:   # (14,3)
        relation='-(e2, e1)'
        men_nopunc[p2]='<e1>'+men_nopunc[p2]+'</e1>'
        men_nopunc[p1]='<e2>'+men_nopunc[p1]+'</e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
    elif int(p1)==int(p1):   # (14,14)
        relation='-(e2, e1)'
        men_nopunc[p2]='<e2><e1>'+men_nopunc[p2]+'</e1></e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
    else:
        relation='-(e1, e2)'  # (3,14)
        men_nopunc[p1]='<e1>'+men_nopunc[p1]+'</e1>'
        men_nopunc[p2]='<e2>'+men_nopunc[p2]+'</e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
    data=[i,sentence,relation]
    dataset.append(data)
for i in pos_id:
    pos=re.findall(r'[(](.*?)[)]', i) # position of two words
    pos=pos[0].split(',')
    mention=pos_id_mention[i]
    men_nopunc=re.findall(r'\w+\-?\w+\-?\w+|\'?\w+',mention) # a list contain all words in mentions(omit punctuations)
    p1=int(pos[0])
    p2=int(pos[1])
    #print(p1)
    #print(p2)
    if p1>p2:   # (14,3)
        relation='-(e2, e1)'
        men_nopunc[p2]='<e1>'+men_nopunc[p2]+'</e1>'
        men_nopunc[p1]='<e2>'+men_nopunc[p1]+'</e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
    elif p1==p2:   # (14,14)
        relation='-(e2, e1)'
        men_nopunc[p2]='<e2><e1>'+men_nopunc[p2]+'</e1></e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
    else:
        relation='-(e1, e2)'  # (3,14)
        men_nopunc[p1]='<e1>'+men_nopunc[p1]+'</e1>'
        men_nopunc[p2]='<e2>'+men_nopunc[p2]+'</e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
        #print(sentence)
    data=[i,sentence,relation]
    dataset.append(data)
#print(dataset)
