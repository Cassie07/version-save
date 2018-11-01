# %load data_helpers.py
import numpy as np
import pandas as pd
import nltk
import re
import json
import os, sys


# ===========================================================================================
# Modify start here
# Load our dataset
# generate a list of dataset in the same format as the paper did
# r[['id','mention','relation'],['id','mention','relation'],...]
# ============================================================================================

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
id_mention={} # a dictionary contain all id:mention
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
        # define relation
        relation='-(e2, e1)'
        # add position info to target word
        men_nopunc[p2]='<e1>'+men_nopunc[p2]+'</e1>'
        men_nopunc[p1]='<e2>'+men_nopunc[p1]+'</e2>'
        # combine all words in the list
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
        relation='+(e2, e1)'
        men_nopunc[p2]='<e1>'+men_nopunc[p2]+'</e1>'
        men_nopunc[p1]='<e2>'+men_nopunc[p1]+'</e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
    elif p1==p2:   # (14,14)
        relation='+(e2, e1)'
        men_nopunc[p2]='<e2><e1>'+men_nopunc[p2]+'</e1></e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
    else:
        relation='+(e1, e2)'  # (3,14)
        men_nopunc[p1]='<e1>'+men_nopunc[p1]+'</e1>'
        men_nopunc[p2]='<e2>'+men_nopunc[p2]+'</e2>'
        seperator = ' '
        sentence=seperator.join(men_nopunc)
        #print(sentence)
	sentence = sentence.replace("<e1>", "<e1> ").replace("</e1>", " </e11>") # replace the front by the back
	sentence = sentence.replace("<e2>", "<e2> ").replace("</e2>", " </e22>")
	sentence = clean_str(sentence) # delete
    data=[i,sentence,relation]
    dataset.append(data)
#print(dataset)


# ===========================================================================================
# clean_str: extract words we want or delete punctuation we don't want
# Regular expressionn
# re.sub('[A-Za-z0-9]') means only save letters and numbers. Without [] means save every thing
# re.sub(',',' , ',string) means change a,b to a , b
# ============================================================================================
def clean_str(string):
	"""
	Tokenization/string cleaning for all datasets except for SST.
	Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
	"""
	string = re.sub(r"[^A-Za-z0-9()<>/,!?\'\`]", " ", string)
	string = re.sub(r"\'s", " \'s", string)
	string = re.sub(r"\'ve", " \'ve", string)
	string = re.sub(r"n\'t", " n\'t", string)
	string = re.sub(r"\'re", " \'re", string)
	string = re.sub(r"\'d", " \'d", string)
	string = re.sub(r"\'ll", " \'ll", string)
	string = re.sub(r",", " , ", string)
	string = re.sub(r"!", " ! ", string)
	string = re.sub(r"\(", " \( ", string)
	string = re.sub(r"\)", " \) ", string)
	string = re.sub(r"\?", " \? ", string)
	string = re.sub(r"\s{2,}", " ", string)
	return string.strip().lower()


def load_data_and_labels(path):
	#data = []
	# read by line and add all elements into a list
	#lines = [line.strip() for line in open(path)]
	#for idx in range(0, len(lines), 4): # start: 0. end: lines.length. selected_interval:4(0,4,8,12,...)
	#	id = lines[idx].split("\t")[0]
	#relation = lines[idx + 1] # extract relation(string)
		#print(relation)
	#	sentence = lines[idx].split("\t")[1]#[1:-1]# delete "(index=0) and "(index=the last word in sentence) in sentence
	#	print(sentence)
	#	sentence = sentence.replace("<e1>", "<e1> ").replace("</e1>", " </e11>") # replace the front by the back
	#	sentence = sentence.replace("<e2>", "<e2> ").replace("</e2>", " </e22>")
	#	sentence = clean_str(sentence) # delete
		# data.append([id, sentence, e1, e2, relation])
	#	data.append([id, sentence, relation])
	#print(data)

	# df = pd.DataFrame(data=data, columns=["id", "sentence", "e1_pos", "e2_pos", "relation"])
    # a structure like dictionary
	df = pd.DataFrame(data=dataset, columns=["id", "sentence", "relation"])
	labelsMapping = {'+(e2, e1)': 1,'+(e1, e2)':1,'-(e2, e1)':0,'-(e1, e2)':0}
    # transfer string label to int lable
	df['label'] = [labelsMapping[r] for r in df['relation']]

	x_text = df['sentence'].tolist()

	# pos1, pos2 = get_relative_position(df)

	# Label Data
	y = df['label']
	labels_flat = y.values.ravel() #a contiguous flattened array.
	# count the total numbers of labels
	labels_count = np.unique(labels_flat).shape[0]

	# convert class labels from scalars to one-hot vectors
	# 0  => [1 0 0 0 0 ... 0 0 0 0 0]
	# 1  => [0 1 0 0 0 ... 0 0 0 0 0]
	# ...
	# 18 => [0 0 0 0 0 ... 0 0 0 0 1]
	def dense_to_one_hot(labels_dense, num_classes):
		num_labels = labels_dense.shape[0]
		index_offset = np.arange(num_labels) * num_classes
		labels_one_hot = np.zeros((num_labels, num_classes))
		labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
		return labels_one_hot

	labels = dense_to_one_hot(labels_flat, labels_count)
	labels = labels.astype(np.uint8)

	# return x_text, pos1, pos2, labels
	return x_text, labels


def get_relative_position(df, max_sentence_length=100):
	# Position data
	pos1 = []
	pos2 = []
	for df_idx in range(len(df)):
		sentence = df.iloc[df_idx]['sentence']
		tokens = nltk.word_tokenize(sentence)
		e1 = df.iloc[df_idx]['e1_pos']
		e2 = df.iloc[df_idx]['e2_pos']

		d1 = ""
		d2 = ""
		for word_idx in range(len(tokens)):
			d1 += str((max_sentence_length - 1) + word_idx - e1) + " "
			d2 += str((max_sentence_length - 1) + word_idx - e2) + " "
		for _ in range(max_sentence_length - len(tokens)):
			d1 += "999 "
			d2 += "999 "
		pos1.append(d1)
		pos2.append(d2)

	return pos1, pos2


def batch_iter(data, batch_size, num_epochs, shuffle=True):
	"""
	Generates a batch iterator for a dataset.
	"""
	data = np.array(data)
	data_size = len(data)
	num_batches_per_epoch = int((len(data) - 1) / batch_size) + 1
	for epoch in range(num_epochs):
		# Shuffle the data at each epoch
		# if shuffle:
		# 	shuffle_indices = np.random.permutation(np.arange(data_size))
		# 	shuffled_data = data[shuffle_indices]
		# else:
		# 	shuffled_data = data
		for batch_num in range(num_batches_per_epoch):
			start_index = batch_num * batch_size
			end_index = min((batch_num + 1) * batch_size, data_size)
			# yield shuffled_data[start_index:end_index]
			yield data[start_index:end_index]

a=load_data_and_labels('/projects/blstm/data/all.txt')
