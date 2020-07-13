import pandas as pd
import matplotlib.pyplot as plt
from csv import DictReader
from collections import OrderedDict


class Result:
    # Default values
    path, shapes = None, None
    data = []


    # Constructor
    def __init__(self, path, shapes):
        self.path = path
        self.shapes = shapes
        self.randomScatter()

        # Reading csv data as a map
        with open(path, 'r') as labelMap:
            csv_dict = DictReader(labelMap)
            for row in csv_dict:
                self.data.append(dict(row))
        
        print(self.data)

        self.randomScatter()


    # Creates heatmap data from csv
    def randomScatter(self):
        x, y = [], []

        # Getting the respective types of points on the axes
        for shape in self.shapes:
            for coordinate in shape.coordinates:
                print(coordinate[0], coordinate[1])
                x.append(int(coordinate[0]))
                y.append(int(coordinate[1]))
        
        # Getting metrics for the coordinate lists
        maxX, maxY = max(x), max(y)
        minX, minY = min(x), min(y)

        print(maxX, maxY)
    
    
    # Displays data in an more readable way in the console
    def printData(self):
        for i, row in self.data.iterrows():
            print("Label: " + str(row[0]) + "\tPoints: " + str(row[1]))


# Main executable
# if __name__ == "__main__":
#     result = Result("data/testdata.csv")
#     result.printData()