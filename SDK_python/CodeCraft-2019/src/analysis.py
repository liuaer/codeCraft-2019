#-*- coding: UTF-8 -*-
import csv
from util import load_data
import  random



def getCarCSV():
    roadDataFrame = load_data('../config/car.txt')
    out = open('car.csv', 'a')
    csv_write = csv.writer(out, dialect='excel')

    for indexs in roadDataFrame.index:
        line = (roadDataFrame.loc[indexs].values[0:])
        csv_write.writerow(line)

