import tkinter as tk
from tkinter import *
from tkinter import filedialog

import SaveAndLoad
from Focus import Focus
from Analysis import Analysis
from Result import Result

class Main:
    # Default values
    snapshotPath = videoPath = pathText = shapeText = ""
    root = openSampleButton = openVideoButton = saveButton = loadButton = focusButton = assignButton = analysisButton = pathText = shapes = analysis = None
    frame = openFrame = shapeFrame = analysisFrame = disp = None

    # Constructor
    def __init__(self):
        # Initializing root window information
        self.root = tk.Tk()
        self.root.title("STAD94")
        self.root.geometry("500x350")
        
        # Creating buttons with respective function calls
        self.openSampleButton = tk.Button(text="Open Snapshot", command = lambda: self.setSnapshotPath())
        self.openVideoButton = tk.Button(text="Open Video", command = lambda: self.setVideoPath())
        self.saveButton = tk.Button(text="Save Shapes", command = lambda: self.saveShapes())
        self.loadButton = tk.Button(text="Load Shapes", command = lambda: self.loadShapes())
        self.focusButton = tk.Button(text="Focus", command = lambda: self.execFocus())
        self.assignButton = tk.Button(text="Assign", command = lambda: self.assignCategory())
        self.analysisButton = tk.Button(text="Start Analysis", command = lambda: self.execAnalysis())
        
        # Disables buttons until they have information to work with
        self.focusButton.config(state=tk.DISABLED)
        # self.analysisButton.config(state=tk.DISABLED)
        self.saveButton.config(state=tk.DISABLED)

        # Displaying buttons
        self.openSampleButton.pack()
        self.openVideoButton.pack()
        self.saveButton.pack()
        self.loadButton.pack()
        self.focusButton.pack()
        self.assignButton.pack()
        self.analysisButton.pack()

        # Default path text
        self.pathText = tk.Text(self.root)
        self.updateText()
        self.pathText.pack()

        # End
        self.root.mainloop()

    # Prompts file selection window and sets snapshotPath
    def setSnapshotPath(self):
        # self.snapshotPath = filedialog.askopenfilename()
        # self.snapshotPath = "/Users/michaelwang/Documents/GitHub/STAD94nyc/media/tokyo_snapshot.png"
        self.enableFocus()
        self.enableAnaylsis()
        self.updateText()

    # Prompts file selection window and sets videoPath
    def setVideoPath(self):
        # self.videoPath = filedialog.askopenfilename()
        # self.videoPath = "/Users/michaelwang/Documents/GitHub/STAD94nyc/media/tokyo_short.mp4"
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

    # Saving currently focused shapes into a local file (data/SavedShapes.json)
    def saveShapes(self):
        SaveAndLoad.writeJSON(self.shapes)

    # Loading previously focused shapes into memory
    def loadShapes(self):
        self.shapes = SaveAndLoad.loadJSON()
        
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
        
        self.printCategories()

    # Brings user to a modular selection page to map out dimensions of where to track during learning
    def execFocus(self):
        self.focus = Focus(self.snapshotPath)
        self.shapes = self.focus.getShapes()
        self.shapeText = self.focus.shapeString()
        self.updateText()

        # Enable save if there were shapes returned
        if self.shapes is not None:
            self.saveButton.config(state=tk.NORMAL)

    # Assigns categories to the created shapes
    def assignCategory(self):
        # Create a new window
        newWindow = tk.Toplevel(self.root)
        newWindow.title("Assign Categories")
        
        # Creating a header row
        tk.Label(newWindow, text = "Label", relief=tk.RIDGE, width=10).grid(row=0, column=0)
        tk.Label(newWindow, text = "Coordinates", relief=tk.RIDGE, width=50).grid(row=0, column=1)
        tk.Label(newWindow, text = "Category", relief=tk.RIDGE, width=15).grid(row=0, column=2)

        # Entries
        entries = []

        # Loop through the existing shapes
        row = 1
        for shape in self.shapes:
            tk.Label(newWindow, text = str(shape.label), relief=tk.RIDGE, width=10).grid(row=row, column=0)
            tk.Label(newWindow, text = str(shape.coordinates), relief=tk.RIDGE, width=50).grid(row=row, column=1)
            entries.append(tk.Entry(newWindow, width=15))
            entries[row - 1].grid(row=row, column=2)
            row += 1
        
        # Get all entry data
        def pressedDone(window, entries):
            # Add the category data for each shape
            for i in range (0, len(self.shapes)):
                self.shapes[i].category = entries[i].get()

            # Destroy the window
            window.destroy()
            
            # self.printCategories()

        # Button to close everything
        tk.Button(newWindow, text="Done", command = lambda: pressedDone(newWindow, entries)).grid(row=row+1, column=0)
        
        # Show everything
        newWindow.mainloop()
        

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
        # result = Result("data/testdata.csv", self.shapes)

    # Printing categories (for debugging)
    def printCategories(self):
        for shape in self.shapes:
            print(shape.category)

# Main executable
if __name__ == "__main__":
    main = Main()