import pandas as pd
import matplotlib.pyplot as plt


class Result:
    # Default values
    path, data = None, None


    # Constructor
    def __init__(self, path):
        self.path = path
        self.data = pd.read_csv(path)
    

    
    
    # Displays data in an more readable way in the console
    def printData(self):
        for i, row in self.data.iterrows():
            print("Label: " + str(row[0]) + "\tPoints: " + str(row[1]))


# Main executable
if __name__ == "__main__":
    result = Result("data/testdata.csv")
    result.printData()