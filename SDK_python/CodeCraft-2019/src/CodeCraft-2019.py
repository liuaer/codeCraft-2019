#-*- coding: UTF-8 -*-
import logging
import sys
from CarGo import Answer



filePath = ''
import platform
sysstr = platform.system()
if(sysstr =="Windows"):
      filePath = '../../logs/CodeCraft-2019.log'
else:
      filePath ='../logs/CodeCraft-2019.log'
logging.basicConfig(level=logging.DEBUG,
                    filename=filePath,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

def main():

    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    # to read input file
    from datetime import datetime
    a=datetime.now()
    Answer(car_path,road_path,answer_path).getAnswer()
    b=datetime.now()
    # print("耗时{}".format((b-a).seconds ))
    # to write output file

if __name__ == "__main__":
    main()
