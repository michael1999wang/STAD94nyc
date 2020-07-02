import json
import numpy as np

class Shape:
    # Default values
    label = None
    coordinates = []


    # Constructor
    def __init__(self, label, coordinates):
        self.label = label
        self.coordinates = coordinates
    

    # Exports a JSON representation of the object
    def exportJSON(self):
        result = {}
        result["label"] = self.label
        result["coordinates"] = self.coordinates
        return json.dumps(result)