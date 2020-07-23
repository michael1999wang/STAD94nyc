from Shape import Shape
import numpy as np
import pandas as pd
import ast
import json
import os.path
    
# Writes JSON file locally under the data folder to save shapes for future use
def writeJSON(shapeList):
    # Forming the map
    result = {}
    content = []
    for shape in shapeList:
        # Converting string to dict
        content.append(ast.literal_eval(shape.exportJSON()))
    result["content"] = content
    result = str(result).replace("'", '"')

    # Writing the string casted map to the JSON file
    jsonFile = open("data/SavedShapes.json", "w")
    jsonFile.write(str(result))
    jsonFile.close()    

# Loads the shapes saved in the JSON file into memory
def loadJSON():
    if os.path.exists("data/SavedShapes.json"):
        # Opening the file
        jsonFile = open("data/SavedShapes.json", "r")
        jsonString = jsonFile.readline()

        # Loading the dictionary and extracting contents
        shapeDict = json.loads(jsonString)
        contents = shapeDict["content"]

        # Loading all the shapes into memory
        shapes = []
        for content in contents:
            shapes.append(Shape(content["label"], content["coordinates"]))

        # Closing the file and returning the loaded shapes
        jsonFile.close()
        return shapes


# Main executable (testing purposes)
if __name__ == "__main__":
    shapes = []
    shapes.append(Shape("test1", [[1, 2], [3, 4]]))
    shapes.append(Shape("test2", [[1, 2], [3, 4]]))
    shapes.append(Shape("test3", [[1, 2], [3, 4]]))
    shapes.append(Shape("test4", [[1, 2], [3, 4]]))
    shapes.append(Shape("test5", [[1, 2], [3, 4]]))
    writeJSON(shapes)
    loadJSON()
