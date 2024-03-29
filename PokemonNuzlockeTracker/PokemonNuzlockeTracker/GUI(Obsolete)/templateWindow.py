from tkinter import *
from PIL import Image, ImageTk
import os

class TemplateWindow():
    def __init__(self, x, y, parent = None):
        """create template for gui"""
        if parent == None:
            self._master = Tk()
        else:
            self._master = Toplevel(parent)
            self.parentXOffset = parent.winfo_x()
            self.parentYOffset = parent.winfo_y()
        self._debugMode = 0
        self._numberOfBadges = 0
        self._game = None
        self._font = "Helvetica 10 italic"
        self.currentpath = os.getcwd()
        self.imagePath = os.path.join(self.currentpath, "../images")

        self._previousX = x
        self._previousY = y
        self._masterX = x
        self._masterY = y
        self._updateTime = 500
        self._image = os.path.join(self.imagePath, "bg.jpg")
        self._icon = os.path.join(self.imagePath, "sprites/icons/nuzlocke.ico")

        self._master.geometry(f"{self._masterX}x{self._masterY}")
        if parent != None:
            #create window at lefthgand corner of parent window instead of a random location
            self._master.geometry(f"+{self.parentXOffset}+{self.parentYOffset}")

        self._master.attributes("-topmost", True)
        self._master.iconbitmap(self._icon)
        self._master.resizable(1,1)

        self._photo = ImageTk.PhotoImage(Image.open(self._image).resize([self._masterX, self._masterY]),Image.BOX)
        self._photoLabel = Label(self._master, image = self._photo)
        self._photoLabel.configure(image = self._photo)
        self._photoLabel.place(x=0, y=0)
        self._photoLabel.image = self._photo
        #make widgets resize with window
        self._master.rowconfigure(0, weight = 1)
        self._master.columnconfigure(0, weight = 1)
    

    def update(self):
        """update image relative to window size"""
        self._master.update()
        self._masterY = self._master.winfo_height()
        self._masterX = self._master.winfo_width()
        if (self._masterX != self._previousX) or (self._masterY != self._previousY):
            #update the bg to fully cover the adjusted area
            photo = ImageTk.PhotoImage(Image.open(self._image).resize([self._masterX, self._masterY]))
            self._photoLabel.configure(image = photo)
            #update values after resize
            self._previousX = self._masterX
            self._previousY = self._masterY
            #needed otherwise image is disposed due to garbage collection
            self._photoLabel.image = photo
        self._resizeImage = self._master.after(self._updateTime, self.update)
    
    def configureWindow(self, row, column):
        """function to update the rowconfigure and column configure"""
        for i in range(row):
            self._master.rowconfigure(i, weight = 1)
        for i in range(column):
            self._master.columnconfigure(i, weight = 1)
    
    def stop(self):
        """stop the update cycle else an error can occur"""
        self._master.after_cancel(self._resizeImage)

    def run(self):
        """function to actually run the window"""
        self._master.mainloop()
    
    def exit(self):
        """destroys window"""
        self._master.destroy()