import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class Focus:
    # Default values
    master, image, canvas = None, None, None

    # Constructor
    def __init__(self, samplePath):
        # Initialize window
        self.master = tk.Tk()

        # Find image dimensions
        width, height = Image.open(samplePath).size

        # Create canvas of that size
        self.canvas = Canvas(self.master, width=width, height=height, cursor="cross", highlightthickness=0)
        self.canvas.pack()
        self.image = ImageTk.PhotoImage(Image.open(samplePath))
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        # End
        self.master.mainloop()

    

if __name__ == "__main__":
    focus = Focus("/Users/michaelwang/Documents/GitHub/STAD94nyc/media/tokyo_snapshot.png")