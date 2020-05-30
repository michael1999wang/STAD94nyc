class Shape:
    # Default values
    coordinates = []
    label = None

    # Constructor
    def __init__(self, coordinates, label):
        self.coordinates = coordinates
        self.label = label