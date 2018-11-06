import dataset_function
import json
import os, sys
import re
import tensorflow as tf

tf.flags.DEFINE_string("train_dir", "/projects/blstm/new_dataset/train_dataset", "Path of json file:{'pair':['mention_ids']}")
tf.flags.DEFINE_string("test_dir", "/projects/blstm/new_dataset/test_dataset", "Path of json file: {'id':'mention'}")
tf.flags.DEFINE_string("dir", "/projects/blstm/new_dataset", "Path of json file:{'pair':['mention_ids']}")
FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()): # sorted here is to sort the elements by their first letter
	print("{} = {}".format(attr.upper(), value))
print("")

def load_pair_name(dir):
    list=dataset_function.read_file(dir) #['test','train]
    print(list)
    train_dataset_pair=[]
    test_dataset_pair=[]
    for i in list:
        if i=='train_dataset':
            path=dir+'/'+i
            label=dataset_function.read_file(path) #['neg','pos',...]
            for j in label:
                path2=path+'/'+j
                product=dataset_function.read_file(path2) #['p1','p2',...]
                for k in product:  # read content in each product file(its pair)
                    text_file = open(path2+'/'+k, "r")
                    lines = text_file.readlines()
                    for l in lines:
                        train_dataset_pair.append(l.split('\n')[0])
            print(len(train_dataset_pair))
        else:
            path=dir+'/'+i
            label=dataset_function.read_file(path) #['neg','pos',...]
            for j in label:
                path2=path+'/'+j
                product=dataset_function.read_file(path2) #['p1','p2',...]
                for k in product:
                    text_file = open(path2+'/'+k, "r")
                    lines = text_file.readlines()
                    for l in lines:
                        test_dataset_pair.append(l.split('\n')[0])
            print(len(test_dataset_pair))
    return train_dataset_pair,test_dataset_pair

a=load_pair_name(FLAGS.dir)
