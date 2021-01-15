from keras.models import Model, load_model
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

mPath = "Model/"
smodel_path = mPath + 'file_classification.h5'
sweight_path = mPath + 'classification_weights'
imodel_path = mPath + 'image_classification.h5'
iweight_path = mPath + 'image_weights'

Summarizer = pipeline("summarization")
Tokenizer = XLNetTokenizer.from_pretrained('xlnet-large-cased')

class NullModel :
    def __init__(self) :
        pass
    def predict(self,*args,**kwargs) :
        raise Exception

def getModel(model_path,weight_path) :
    try :
        print('[+] Loading Model')
        model = load_model(model_path)
        print('[+] Loading Weights')
        model.load_weights(weight_path)

        return model
    except OSError :
        print("[!] Model Not Loaded")
        return NullModel

sModel = getModel(smodel_path,sweight_path)
iModel = getModel(imodel_path,iweight_path)

n_topics = 10

classes = ['Algebra',
 'Calculus',
 'City',
 'Curves',
 'Education',
 'Flower',
 'Geometry',
 'Light',
 'Science',
 'Trigonometry']

def getCategory(sentence) :
    summary = Summarizer(sentence)[0]['summary_text']
    tokenized = Tokenizer.encode(summary)
    xData = tokenized[:20]

    preds = model.predict([xData])
    preds = np.argmax(preds,axis=1)

    classification = preds[0]
    
    return classes[classification]

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