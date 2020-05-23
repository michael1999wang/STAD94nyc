import tkinter as tk
from tkinter import filedialog

class Main:

    samplePath, videoPath, pathText = "", "", ""
    root, openSampleButton, openVideoButton, startButton, pathText = None, None, None, None, None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("STAD94")
        self.root.geometry("250x250")
        self.openSampleButton = tk.Button(self.root, text="Open Sample", command = lambda: self.setSamplePath())
        self.openVideoButton = tk.Button(self.root, text="Open Video", command = lambda: self.setVideoPath())
        self.startButton = tk.Button(self.root, text="Start Analysis", command = lambda: self.analysis())
        self.startButton.config(state=tk.DISABLED)

        self.openSampleButton.pack()
        self.openVideoButton.pack()
        self.startButton.pack()

        self.pathText = tk.Text(self.root)
        self.updatePathText()
        self.pathText.pack()

        self.root.mainloop()


    def setSamplePath(self):
        self.samplePath = filedialog.askopenfilename()
        self.enableAnaylsis()
        self.updatePathText()

    def setVideoPath(self):
        self.videoPath = filedialog.askopenfilename()
        self.enableAnaylsis()
        self.updatePathText()

    def updatePathText(self):
        self.pathText.delete("1.0", tk.END)
        self.pathText.insert(tk.CURRENT, "\nSample Path: " + self.samplePath + "\n\nVideo Path: " + self.videoPath)

    def enableAnaylsis(self):
        if self.samplePath is not None and self.videoPath is not None:
            self.startButton.config(state=tk.NORMAL)
        else:
            self.startButton.config(state=tk.DISABLED)

    def analysis(self):
        pass


if __name__ == "__main__":
    main = Main()