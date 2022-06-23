import time
from turtle import *
import colors 
class ImageRenderLang:
    def __init__(self, filepath, seperator = " ", colorname=False):
        self._seperator = seperator
        self._colorname = colorname
        file = open(filepath)
        self._encodedValuesDefault = file.readlines()
        self._encodedValuesDefault = [value for value in self._encodedValuesDefault if value!="\n"]
        #Remove the \n at the end
        for i in range(len(self._encodedValuesDefault)-1):
            self._encodedValuesDefault[i] = self._encodedValuesDefault[i][:-1]
    def parser(self):
        #Parse the seperators and add pixels into individual arrays
        pixels = []
        for row in self._encodedValuesDefault:
            currentrow = row.split(self._seperator)
            #Pop the 0s
            for item in range(len(currentrow)-1):
                if currentrow[item].startswith("0"):
                    currentrow.pop(item)
            pixels.append(currentrow)
        #pixels -> 2D Array, X-Axis = Row, Y-Axis = Item with color
        #Convert pixels into 3d array, with Y-Axis becoming items in a row and Z-Axis becoming the number/color of the pixel only do if colorname == True
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        if self._colorname == True:
            for row in range(len(pixels)):
                for itemindex in range(len(pixels[row])):
                    indexstart = 0
                    for index, charachter in enumerate(pixels[row][itemindex]):
                        if str(charachter).lower() in letters:
                            indexstart = index
                            break
                    pixels[row][itemindex] = [pixels[row][itemindex][:indexstart], pixels[row][itemindex][indexstart:]]
        return pixels

    def addtoobj(self):
        self.pixels = self.parser()
    def render(self, colormode = "WB", scale = 1, backgroundcolor = "white"):
        height = len(self.pixels)
        widths = []
        for row in self.pixels():
            currentwidth = 0
            for item in row:
                currentwidth+=int(item[0])
            widths.append(currentwidth)
        if all(ele == widths[0] for ele in widths):
            pass
        else:
            return f"Fatal render error: Width of image does not stay constant throughout image."
        

        

if __name__ == "__main__":
    obj = ImageRenderLang("D:\..txt", seperator = ",", colorname = True)
    obj.addtoobj()
    #obj.render(scale = 100, colormode="WB")
    print(obj.pixels)
