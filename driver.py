import tkinter as tk
from tkinter import filedialog

class Main:
    # Default values so other methods don't throw errors
    samplePath, videoPath, pathText = "", "", ""
    root, openSampleButton, openVideoButton, startButton, pathText = None, None, None, None, None


    def __init__(self):
        # Initializing root window information
        self.root = tk.Tk()
        self.root.title("STAD94")
        self.root.geometry("250x250")

        # Creating buttons with respective function calls
        self.openSampleButton = tk.Button(self.root, text="Open Sample", command = lambda: self.setSamplePath())
        self.openVideoButton = tk.Button(self.root, text="Open Video", command = lambda: self.setVideoPath())
        self.startButton = tk.Button(self.root, text="Start Analysis", command = lambda: self.analysis())
        self.startButton.config(state=tk.DISABLED)

        # Displaying buttons
        self.openSampleButton.pack()
        self.openVideoButton.pack()
        self.startButton.pack()

        # Default path text
        self.pathText = tk.Text(self.root)
        self.updatePathText()
        self.pathText.pack()

        # End
        self.root.mainloop()


    # Prompts file selection window and sets samplePath
    def setSamplePath(self):
        self.samplePath = filedialog.askopenfilename()
        self.enableAnaylsis()
        self.updatePathText()


    # Prompts file selection window and sets videoPath
    def setVideoPath(self):
        self.videoPath = filedialog.askopenfilename()
        self.enableAnaylsis()
        self.updatePathText()


    # Updates the path text
    def updatePathText(self):
        self.pathText.delete("1.0", tk.END)
        self.pathText.insert(tk.CURRENT, "\nSample Path: " + self.samplePath + "\n\nVideo Path: " + self.videoPath)


    # Disables/normalizes button based on file selection status
    def enableAnaylsis(self):
        if self.samplePath is not None and self.videoPath is not None:
            self.startButton.config(state=tk.NORMAL)
        else:
            self.startButton.config(state=tk.DISABLED)


    # Call machine learning object to start analysis
    def analysis(self):
        pass


if __name__ == "__main__":
    main = Main()