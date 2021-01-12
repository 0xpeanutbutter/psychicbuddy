import pandas as pd
import numpy as np

import random
# import torch
import nltk
import sys
import os
import io

nltk.download('punkt')

from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5Tokenizer,
    get_linear_schedule_with_warmup , 
    pipeline ,
    XLNetTokenizer,
)

Summarizer = pipeline("summarization")
Tokenizer = XLNetTokenizer.from_pretrained('xlnet-large-cased')

n_topics = 10

def getRandom(x) :
    return random.random()

def getFileNames(pathname) :
    classes = os.listdir(pathname)
    classes.sort()
    files = []
    fileNames = {}
    for i in classes :
        tFiles = os.listdir(pathname+i)
        tFiles.sort()
        tFiles = [pathname + i + '/' + j for j in tFiles]
        for k in tFiles :
            fileNames[k] = i
        files += tFiles 
    files.sort(key=getRandom)
    return classes , files , fileNames

def readDataFromFolder(pathname) :
    classes , files , fileNames = getFileNames(pathname)
    X = []
    Y = []
    for i in files :
        f = open(i)
        data = f.read()
        if len(data.split()) > 142 :
            data = Summarizer(data)[0]['summary_text']
        if data not in ['' , ' '] :
            # print(i)
            X.append(data)
            Y.append([classes.index(fileNames[i])])
    return classes , X , Y

def getOneHot(x,num_classes=n_topics) :
    encoded = np.zeros(num_classes)
    encoded[x] = 1

    return encoded