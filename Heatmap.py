import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

# Normalize the list of points
def normalizeList(lst):
    result = []
    
    # Unstring each element in the list and append to the result
    for element in lst:
        result.append(ast.literal_eval(element))

    # Return the result
    return result

# Find midpoint of a quadrilateral
def findMidpoint(points):
    # Keep track of both kinds of coordinates
    x, y = [], []

    # Loop through and append to each list
    for point in points:
        x.append(point[0])
        y.append(point[1])
    
    # Get min amd max values for each
    minX, minY, maxX, maxY = min(x), min(y), max(x), max(y)

    # Returning the averages
    return [int((minX + maxX)/2), int((minY + maxY)/2)]

# Main executable
if __name__ == "__main__":
    # Get all data from csv
    df = pd.read_csv("data/totals.csv")
    df_points = list(df["Points"])
    df_hits = list(df["Hits"])

    # Get the image data
    img = plt.imread("data/view.png")

    # Get the normalized list
    normalized = normalizeList(df_points)

    # Loop through the shapes
    midPoints = []
    for shape in normalized:
        # Append the points to the midpoint
        midPoints.append(findMidpoint(shape))
    
    # Convert arrays into numpy arrays
    np_midPoints = np.asarray(midPoints)
    np_hits = np.asarray(df_hits)

    # Flatten the array
    x, y = np_midPoints[..., 0].ravel(), np_midPoints[..., 1].ravel()
    color = np_hits.ravel()

    # Plot the map
    plt.title("Heatmap")
    plt.imshow(img)
    plt.scatter(x, y, c = color, s = 200)
    plt.colorbar()
    plt.show()