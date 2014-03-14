#! /usr/bin/env python
from sys import argv
import os
import json
import logging





class Parser(object):
    """parse data mining homework - movie data"""
    def __init__(self, filePath):
        self.filePath = filePath
        self.dataRow = []
        self.productIDPattern = "product/productId: "
        self.userIDPattern = "review/userId: "
        self.scorePattern = "review/score: "
        self.cachePath = "./cache/"
        self.datarowPath  = self.cachePath+"datarow"+".json"

        try:
            self.logger = logger
        except:
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(Parser)

    def load(self, cache=None):
        self.logger.info("loading data")
        if  DEBUG and os.path.exists(self.datarowPath):
            self.logger.info("find cachem, load cache")
            with open(self.datarowPath, 'r') as dataRowFd:
                self.dataRow = json.load(dataRowFd, "ASCII")
            return

        self.logger.info("No cache, parsing data from file.")
        with open(self.filePath, 'r') as fileFd:
            isEnd = False;
            while not isEnd:
                productID = ''
                userID = ''
                score = 0
                while True:
                    line = fileFd.readline()
                    if line == '':
                        isEnd = True
                        break
                    line = line.strip("\n")
                    if line.find(self.productIDPattern) != -1:
                        productID = line[len(self.productIDPattern):]
                    elif line.find(self.userIDPattern) != -1:
                        userID = line[len(self.userIDPattern):]
                    elif line.find(self.scorePattern) != -1:
                        score = float(line[len(self.scorePattern):])

                    if len(line.strip()) < 1:
                        break

                self.dataRow.append([productID, userID, score])
            if  cache:
                self.cache()

    def cache(self):
        if  not os.path.exists(self.cachePath):
            os.mkdir(self.cachePath)
        with open(self.datarowPath, 'w') as dataRowFd:
            dataRowFd.write(json.dumps(self.dataRow, indent=4))

    def getStaticByOneColumn(self, column, scoreColumn):
        """Use identified column as key to order data"""
        resultDict = {}
        for row in self.dataRow:
            key, val = row[column], row[scoreColumn]
            if  key not in resultDict:
                resultDict[key] = []
            resultDict[key].append(val)
        return resultDict
            
def mean(list):
    count = 0;
    total = 0;
    for item in list:
        total += item
        count += 1
    return total/count

def variance(list):
    count = 0;
    total = 0;
    for item in list:
        total += item**2
        count += 1
    return total/count

if __name__ == '__main__':
    DEBUG = True
    try:
        filePath = argv[1]
    except:
        filePath = "/home/lucas/Downloads/movies.minor"

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    parser = Parser(filePath)
    parser.load(cache=DEBUG)
    movieList = parser.getStaticByOneColumn(0,2)
    for key, val in movieList.iteritems():
        movieList[key] = [mean(val), variance(val)]
        print "{0}:\n\t mean={1} variance={2}".format(key, movieList[key][0], movieList[key][1])
        
    userList = parser.getStaticByOneColumn(1,2)
    for key, val in movieList.iteritems():
        userList[key] = [mean(val), variance(val)]
        print "{0}:\n\t mean={1} variance={2}".format(key, userList[key][0], userList[key][1])
        
