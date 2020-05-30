import pandas as pd

class Result:
    # Default values
    path, data = None, None


    # Constructor
    def __init__(self, path):
        self.path = path
        self.data = pd.read_csv(path)
        print(self.data)
    
    
