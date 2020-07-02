import tkinter as tk
from tkinter import filedialog

import SaveAndLoad
from Focus import Focus
from Analysis import Analysis
from Result import Result


class Main:
    # Default values
    snapshotPath, videoPath, pathText, shapeText = "", "", "", ""
    root, openSampleButton, openVideoButton, focusButton, saveButton, loadButton, analysisButton, pathText = None, None, None, None, None, None, None, None
    shapes, analysis = None, None


    # Constructor
    def __init__(self):
        # Initializing root window information
        self.root = tk.Tk()
        self.root.title("STAD94")
        self.root.geometry("500x350")

        # Creating buttons with respective function calls
        self.openSampleButton = tk.Button(self.root, text="Open Snapshot", command = lambda: self.setSnapshotPath())
        self.openVideoButton = tk.Button(self.root, text="Open Video", command = lambda: self.setVideoPath())
        self.focusButton = tk.Button(self.root, text="Focus", command = lambda: self.execFocus())
        self.saveButton = tk.Button(self.root, text="Save Shapes", command = lambda: self.saveShapes())
        self.loadButton = tk.Button(self.root, text="Load Shapes", command = lambda: self.loadShapes())
        self.analysisButton = tk.Button(self.root, text="Start Analysis", command = lambda: self.execAnalysis())
        
        # Disables buttons until they have information to work with
        self.focusButton.config(state=tk.DISABLED)
        self.analysisButton.config(state=tk.DISABLED)
        self.saveButton.config(state=tk.DISABLED)

        # Displaying buttons
        self.openSampleButton.pack()
        self.openVideoButton.pack()
        self.saveButton.pack()
        self.loadButton.pack()
        self.focusButton.pack()
        self.analysisButton.pack()

        # Default path text
        self.pathText = tk.Text(self.root)
        self.updateText()
        self.pathText.pack()

        # End
        self.root.mainloop()


    # Prompts file selection window and sets snapshotPath
    def setSnapshotPath(self):
        self.snapshotPath = filedialog.askopenfilename()
        self.enableFocus()
        self.enableAnaylsis()
        self.updateText()


    # Prompts file selection window and sets videoPath
    def setVideoPath(self):
        self.videoPath = filedialog.askopenfilename()
        self.enableAnaylsis()
        self.updateText()


    # Updates the path text
    def updateText(self):
        self.pathText.delete("1.0", tk.END)
        self.pathText.insert(tk.CURRENT, "\nSample Path: " + self.snapshotPath + "\n\nVideo Path: " + self.videoPath + "\n\nEntry Coordinates: " + self.shapeText)


    # Enables the focus button after a sample has been chosen
    def enableFocus(self):
        if self.snapshotPath != "":
            self.focusButton.config(state=tk.NORMAL)
        else:
            self.focusButton.config(state=tk.DISABLED)


    # Brings user to a modular selection page to map out dimensions of where to track during learning
    def execFocus(self):
        self.focus = Focus(self.snapshotPath)
        self.shapes = self.focus.getShapes()
        self.shapeText = self.focus.shapeString()
        self.updateText()

        # Enable save if there were shapes returned
        if self.shapes is not None:
            self.saveButton.config(state=tk.NORMAL)

    
    # Saving currently focused shapes into a local file (data/SavedShapes.json)
    def saveShapes(self):
        SaveAndLoad.writeJSON(self.shapes)


    # Loading previously focused shapes into memory
    def loadShapes(self):
        self.shapes = SaveAndLoad.loadJSON()
        print(self.shapes)

        # Switch on the save button if shapes were loaded
        if self.shapes is not None:
            self.saveButton.config(state=tk.NORMAL)
            
            # Updating the textfield
            self.shapeText = "\n"
            for shape in self.shapes:
                for coordinates in shape.coordinates:
                    self.shapeText += "(" + str(coordinates[0]) + "," + str(coordinates[1]) + ") "
                self.shapeText += "\n"
            
            self.updateText()


    # Normalizes/disables button based on file selection status
    def enableAnaylsis(self):
        if self.snapshotPath != "" and self.videoPath != "":
            self.analysisButton.config(state=tk.NORMAL)
        else:
            self.analysisButton.config(state=tk.DISABLED)


    # Call machine learning module to start analysis
    def execAnalysis(self):
        self.analysis = Analysis(self.videoPath, self.shapes)
        self.analysis.execBodyRecognition()
        # result = Result("testdata.csv")


# Main executable
if __name__ == "__main__":
    main = Main()