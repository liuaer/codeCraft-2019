#-*- coding: UTF-8 -*-
import csv
import os
from util import load_data
from collections import defaultdict
from heapq import *
from util import load_data
import  random

class  Answer():

    def __init__(self,car_path, road_path, answer_path):

        self.G_car_path = car_path
        self.G_road_path = road_path
        self.G_answer_path =answer_path
        self.dijkstraAnswer={}

    def getAnswer(self):
        #         0     1     2     3        4           5                  6        7
        titls = ['id', 'from', 'to', 'speed', 'planTime', 'pathLength','roadpath','road*speed']
        CarsList = []
        carDataFrame = load_data(self.G_car_path)
        raodMap, roadDic, roadDataFrame = self.getRoadMap()
        for indexs in carDataFrame.index:
            line = (carDataFrame.loc[indexs].values[0:]).tolist()
            # print(line)
            # def  getBestPath(carFrom,carTo,carSpeed,roadMap,roadDic,roadDataFrame):
            roadList, bestPathLength = self.getBestPath(line[1], line[2], line[3], raodMap, roadDic, roadDataFrame)
            line.append(bestPathLength)
            line.append(roadList)
            CarsList.append(line)
        # 多键排序   速度降序   路程升序
        CarsList = sorted(CarsList, key=lambda car: (car[4], -car[3], car[5]))

        #相同StartTime分批调度
        import numpy as np
        SSDic={}
        for index, car in enumerate(CarsList):
            if car[4] in SSDic.keys():
                sumPathLenCount=SSDic[car[4]]
                sumPathLenCount.append(car[5])
            else:
                sumPathLenCount =[]
                sumPathLenCount.append(car[5])
                SSDic[car[4]]=sumPathLenCount

        file = open(self.G_answer_path, 'w')
        end = len(CarsList) - 1
        for index, car in enumerate(CarsList):
            # print(car)
            # s输出答案
            #根据开始时间的奇偶性随机增加
            import math
            carPlanTime = car[4]+(car[4]-1)*50

            sumPathLenCount = SSDic[car[4]]
            a = np.array(sumPathLenCount)
            P_10 = np.percentile(a,10)
            P_20 =np.percentile(a,20)
            P_30 =np.percentile(a,30)
            P_40 = np.percentile(a, 40)
            P_50 = np.percentile(a, 50)
            P_60 = np.percentile(a, 60)
            P_70 = np.percentile(a, 70)
            P_80 = np.percentile(a, 80)
            P_90 = np.percentile(a, 90)

            baseLine = int(50/9)
            if car[5]>P_10 and car[5]<P_20:
                carPlanTime +=baseLine
            elif car[5]>P_20 and car[5]<P_30:
                carPlanTime += baseLine*2
            elif car[5] > P_30 and car[5] < P_40:
                carPlanTime +=baseLine * 3
            elif car[5]>P_40 and car[5]<P_50:
                carPlanTime += baseLine*4
            elif car[5]>P_50 and car[5]<P_60:
                carPlanTime += baseLine*5
            elif car[5]>P_60 and car[5]<P_70:
                carPlanTime += baseLine*6
            elif car[5]>P_80 and car[5]<P_90:
                carPlanTime += baseLine*7
            elif car[5]>P_90:
                carPlanTime += baseLine*8

            answer = '(' + '{}'.format(car[0]) + ',' + ' ' + '{}'.format(carPlanTime)
            for road in car[6]:
                answer = answer + ',' + ' ' + '{}'.format(road)
            answer = answer + ')'
            if (end != index):
                answer = answer + '\n'
            file.writelines(answer)


    def dijkstra_raw(self,edges, from_node, to_node):
        g = defaultdict(list)
        for l, r, c in edges:
            g[l].append((c, r))
        q, seen = [(0, from_node, ())], set()
        while q:
            (cost, v1, path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == to_node:
                    return cost, path
                for c, v2 in g.get(v1, ()):
                    if v2 not in seen:
                        heappush(q, (cost + c, v2, path))
        return float("inf"), []

    def dijkstra(self,edges, from_node, to_node):
        len_shortest_path = -1
        ret_path = []
        length, path_queue = self.dijkstra_raw(edges, from_node, to_node)
        if len(path_queue) > 0:
            len_shortest_path = length
            left = path_queue[0]
            ret_path.append(left)
            right = path_queue[1]
            while len(right) > 0:
                left = right[0]
                ret_path.append(left)
                right = right[1]
            ret_path.reverse()

        return len_shortest_path, ret_path

    def getRoadMap(self):
        VDic = {}
        roadid = 0
        roadlength = 1
        roadspeed = 2
        roadchannel = 3
        roadfrom = 4
        roadto = 5
        roadisDuplex = 6
        roadDic = {}  # 边的集合
        Vertex = []  # 顶点集合
        roadMap = [[99999] * 65 for i in range(65)]
        roadDataFrame = load_data(self.G_road_path)
        for indexs in roadDataFrame.index:
            line = (roadDataFrame.loc[indexs].values[0:])
            fromInt = int(line[roadfrom])
            toInt = int(line[roadto])

            # 添加顶点
            if fromInt not in Vertex:
                Vertex.append(fromInt)
            if toInt not in Vertex:
                Vertex.append(toInt)

            # 添加道路
            road_v1 = "{}:{}".format(fromInt, toInt)
            road_v2 = "{}:{}".format(toInt, fromInt)
            if (road_v1 in roadDic.keys()) or (road_v2 in roadDic.keys()):
                pass
            else:
                roadDic[road_v1] = line[roadid]
                roadDic[road_v2] = line[roadid]
        '''
        raodMap 二维矩阵
        roadDic 道路字典
        '''
        return roadMap, roadDic, roadDataFrame

    # 返回最短路径，和权重之和
    def getBestPath(self,carFrom, carTo, carSpeed, roadMap, roadDic, roadDataFrame):
        roadid = 0
        roadlength = 1
        roadspeedIndex = 2
        roadchannel = 3
        roadfrom = 4
        roadto = 5
        roadisDuplex = 6

        #拼接字段
        FromRoadTo = '{}:{}:{}'.format(carFrom,carTo,carSpeed)
        #判断结果是否保存 roadList, bestPathLength
        if FromRoadTo  in self.dijkstraAnswer:
                answer = self.dijkstraAnswer[FromRoadTo]
                print("=== Dijkstra ===")
                print("{}---------->{}".format(carFrom, carTo))
                print('length = ', answer[0])
                print('The shortest path is ', answer[1])
                return answer[0],answer[1]

        roadMap = [[99999] * 65 for i in range(65)]
        for indexs in roadDataFrame.index:
            line = (roadDataFrame.loc[indexs].values[0:])
            fromInt = int(line[roadfrom])
            toInt = int(line[roadto])
            # 更改权重,需要更改所有的道路权重
            roadspeed = min(line[roadspeedIndex], carSpeed)
            weight = int(1.0 / (roadspeed* int(line[roadchannel])) * 1000)*((abs(line[roadspeedIndex]-carSpeed)/carSpeed)+1)
            roadMap[fromInt][toInt] = weight
            if line[roadisDuplex] == 1:
                roadMap[toInt][fromInt] = weight
        # 开始计
        edges = []
        for i in range(len(roadMap)):
            for j in range(len(roadMap[0])):
                if i != j and roadMap[i][j] != 99999:
                    edges.append((i, j, roadMap[i][j]))


        print("=== Dijkstra ===")
        print("{}---------->{}".format(carFrom, carTo))
        bestPathLength, Shortest_path = self.dijkstra(edges, carFrom, carTo)
        print('length = ', bestPathLength)
        print('The shortest path is ', Shortest_path)

        # 求出路径
        roadList = []
        length = len(Shortest_path)
        for index, pathID in enumerate(Shortest_path):
            if (index < length - 1):
                road = "{}:{}".format(pathID, Shortest_path[index + 1])
                roadList.append(roadDic[road])
        # print(roadList)
        #保留本次结果
        if FromRoadTo not in self.dijkstraAnswer:

            self.dijkstraAnswer[FromRoadTo]=[roadList,bestPathLength]

        return roadList, bestPathLength

