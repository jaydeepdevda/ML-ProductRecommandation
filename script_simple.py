# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 21:58:04 2018

@author: Jaydeep
"""

from collections import Counter
import pickle
import json

# save object using pickle in file
PICKLE_FOLDER = ''
ITEM_DICT_OBJ = PICKLE_FOLDER + 'obj_item_dict.pkl'
PAIR_DICT_OBJ = PICKLE_FOLDER + 'obj_pair_dict.pkl'
LIST_PAIR_OBJ = PICKLE_FOLDER + 'obj_list_pair.pkl'

listPairKeys = []
# init empty dictionary to store pair occurencess
pairDict = {}
itemDict = {}


# this function is check that saved object is available or not
def checkDataAvailable():
    try:
        with open(ITEM_DICT_OBJ, 'rb') as f:
            global itemDict
            itemDict = pickle.load(f)
        with open(PAIR_DICT_OBJ, 'rb') as f:
            global pairDict
            pairDict = pickle.load(f)
        with open(LIST_PAIR_OBJ, 'rb') as f:
            global listPairKeys 
            listPairKeys = pickle.load(f)
        return True
    except Exception:
        return False
    # checkDataAvailable function ends here

def processData():
    
    MIN_THRESHOLD = 1
    # read json file from os
    
    DATA_FILE_NAME = 'data_order.json'
    
    fileObj = open(DATA_FILE_NAME,"r")
    jsonObj = json.load(fileObj)
    fileObj.close()
    # order more than 2 items it is 29
    #orderLength = 0
    idList = []
    transactionList = []
    for i in jsonObj:
        if len(i['ItemList'])>=2:
            transactionList.append([j['item Id'] for j in i['ItemList']])
            for j in i['ItemList']:
                idList.append(j['item Id'])
                itemDict[j['item Id']]=j['item Name']
    
    #print('Data Loaded.')
    # transaction length as row length
    rowLen = len(transactionList)
    
    # all items in 1D array
    singleList = idList
    
    # count frequency
    counter = Counter(singleList)
    # remove min thresold
    occurDict = {x : counter[x] for x in counter if counter[x] >= MIN_THRESHOLD }
    
    keys = list(occurDict.keys())
    keyLen = len(keys)
    
    # merge two character for each
    for i in range(keyLen):
        for j in range(keyLen-i-1):
            # make a pair of each purchases
            listPairKeys.append([keys[i],keys[j+1+i]])
    #print(listPairKeys)
    #print('Pair Items')
    
    # assign all pair occurences is zero (0)
    for i in range(len(listPairKeys)):
        pairDict[i] = 0
    
    index  = -1
    # start count for all pairs occurences in dataset
    for pair in listPairKeys:
        index = index + 1
        #aKey = listPairKeys[0] # testing purpose
        char1 = pair[0]
        char2 = pair[1]
    
        # scan all rows as transaction
        for i in range(rowLen):
            # initially this flags are false
            #this is for each char in pair found or not in a transaction        
            tmpFlag1 = False
            tmpFlag2 = False
        
            # check 1st item is available in transaction
            if char1 in transactionList[i]:
                tmpFlag1 = True
            # check 2nd item is available in transaction
            if char2 in transactionList[i]:
                tmpFlag2 = True
            # if both char found then leave for loop
            if tmpFlag1 == True and tmpFlag2 == True:
                # increament count
                pairDict[index] = pairDict[index]+1
    
    # now remove less then thresold value pair from the diction
    # make a copy of dictionary 
    for aKey in list(pairDict):
        # remove pair if it bought toghether with less then min thresold value
        if(pairDict[aKey]<MIN_THRESHOLD):
            # delete from dictionary
            del pairDict[aKey]
    # save pairDict object --> Filtered value
    # save listPairKeys --> Original value
    with open(ITEM_DICT_OBJ, 'wb') as f:
        pickle.dump(itemDict, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(PAIR_DICT_OBJ , 'wb') as f:
        pickle.dump(pairDict, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(LIST_PAIR_OBJ , 'wb') as f:
        pickle.dump(listPairKeys, f)
    # object saved
    userInterection()
    # processData ends here
    

def userInterection():
    # if user is puchasing this item
    print('Select Menu Item from Following list:')
    tmpList1 = list(itemDict.items())
    for i in range(int(len(tmpList1 )/2)):
        print('{0:<30}'.format(str(tmpList1[2*i])), end='')
        print('{0:<30}'.format(str(tmpList1[2*i+1])))
    
    try:
        purchaseItem = int(input('Input Item Id:'))
    except Exception:
        print('Please Enter integer (Number) only from above menu')
    # init recommandation list
    recommandList = []
    
    #print(pairDict)
    
    # find out frequently bought together items in a trained model
    for aKey in pairDict.keys():
        #print(listPairKeys[aKey])
        if purchaseItem in listPairKeys[aKey]:
            # id found then add in recommandation list
            recommandList.extend(listPairKeys[aKey])
    #print('Recommandation')
    try:
        while(True):
            # remove self item
            recommandList.remove(purchaseItem)
    except Exception:
        #do nothing
        tIgnore = False
    #print('Removed Main')
    # print recommandation item list
    print('\n############## Recommandation ############')
    if len(recommandList)==0:
        print('No Items found for Recommandation')
    else :
        print('People who bought',itemDict[purchaseItem],'is also bought this item(s) together:')
        countRecomm = Counter(recommandList)
        for itemId,occur in countRecomm.items() :
            print(itemDict[itemId],occur)

# main program start from here    
if __name__ == '__main__':
    if checkDataAvailable() == True:
        # no need to process data trained model is already available
        userInterection()
    else:
        # no trained model found process data first and then call GUI
        processData()
