import tkinter as tk
from tkinter import filedialog
from Focus import Focus
from Analysis import Analysis

class Main:
    # Default values
    samplePath, videoPath, pathText, shapeText = "", "", "", ""
    root, openSampleButton, openVideoButton, focusButton, startButton, pathText = None, None, None, None, None, None
    focus, shapes, analysis = None, None, None

    # Constructor
    def __init__(self):
        # Initializing root window information
        self.root = tk.Tk()
        self.root.title("STAD94")
        self.root.geometry("500x350")

        # Creating buttons with respective function calls
        self.openSampleButton = tk.Button(self.root, text="Open Sample", command = lambda: self.setSamplePath())
        self.openVideoButton = tk.Button(self.root, text="Open Video", command = lambda: self.setVideoPath())
        self.focusButton = tk.Button(self.root, text="Focus", command = lambda: self.execFocus())
        self.startButton = tk.Button(self.root, text="Start Analysis", command = lambda: self.execAnalysis())
        
        # Disables buttons until they have information to work with
        self.focusButton.config(state=tk.DISABLED)
        self.startButton.config(state=tk.DISABLED)

        # Displaying buttons
        self.openSampleButton.pack()
        self.openVideoButton.pack()
        self.focusButton.pack()
        self.startButton.pack()

        # Default path text
        self.pathText = tk.Text(self.root)
        self.updateText()
        self.pathText.pack()

        # End
        self.root.mainloop()


    # Prompts file selection window and sets samplePath
    def setSamplePath(self):
        self.samplePath = filedialog.askopenfilename()
        self.enableFocus()
        self.enableAnaylsis()
        self.updateText()


    # Prompts file selection window and sets videoPath
    def setVideoPath(self):
        self.videoPath = filedialog.askopenfilename()
        self.enableAnaylsis()
        self.updateText()


    # Brings user to a modular selection page to map out dimensions of where to track during learning
    def execFocus(self):
        self.focus = Focus(self.samplePath)
        self.shapes = self.focus.getShapes()
        self.shapeText = self.focus.shapeString()
        self.updateText()


    # Updates the path text
    def updateText(self):
        self.pathText.delete("1.0", tk.END)
        self.pathText.insert(tk.CURRENT, "\nSample Path: " + self.samplePath + "\n\nVideo Path: " + self.videoPath + "\n\nShape Coordinates: " + self.shapeText)


    # Enables the focus button after a sample has been chosen
    def enableFocus(self):
        if self.samplePath != "":
            self.focusButton.config(state=tk.NORMAL)
        else:
            self.focusButton.config(state=tk.DISABLED)


    # Normalizes/disables button based on file selection status
    def enableAnaylsis(self):
        if self.samplePath != "" and self.videoPath != "":
            self.startButton.config(state=tk.NORMAL)
        else:
            self.startButton.config(state=tk.DISABLED)


    # Call machine learning module to start analysis
    def execAnalysis(self):
        self.analysis = Analysis(self.videoPath)
        self.analysis.bodyRecognition()


if __name__ == "__main__":
    main = Main()