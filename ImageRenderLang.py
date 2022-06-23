import time
from turtle import *
import colors 
class ImageRenderLang:
    def __init__(self, filepath): #seperator = " "
        self._seperator = ","
        file = open(filepath)
        self._encodedValuesDefault = file.readlines()
        self._encodedValuesDefault = [value for value in self._encodedValuesDefault if value!="\n"] #Only get values that are not newlines
        #Remove the \n at the end
        for i in range(len(self._encodedValuesDefault)-1):
            self._encodedValuesDefault[i] = self._encodedValuesDefault[i][:-1]
        #Access header then remove it
        self._encodedValuesDefault.pop(0)
        self._colormode = self._encodedValuesDefault[1]
        try:
            self._scale = int(self._encodedValuesDefault[2])
        except:
            self._scale = 1
        self._backgroundcolor = colors.get(self._encodedValuesDefault[3])

    def parser(self):
        #Parse the seperators and add pixels into individual arrays
        pixels = []
        for linenumber, row in enumerate(self._encodedValuesDefault):
            currentrow = row.split(self._seperator)
            #Pop the 0s
            for item in range(len(currentrow)-1):
                if currentrow[item].startswith("0"):
                    print(f"Removed item {currentrow[item]} from row {linenumber+1} due to 0 start value.")
                    currentrow.pop(item)
            pixels.append(currentrow)
        #pixels -> 2D Array, X-Axis = Row, Y-Axis = Item with color
        #Convert pixels into 3d array, with Y-Axis becoming items in a row and Z-Axis becoming the number/color of the pixel only do if colorname == True
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for row in range(len(pixels)):
            for itemindex in range(len(pixels[row])):
                indexstart = 0
                for index, charachter in enumerate(pixels[row][itemindex]):
                    if str(charachter).lower() in letters:
                        indexstart = index
                        break
                pixels[row][itemindex] = [pixels[row][itemindex][:indexstart], pixels[row][itemindex][indexstart:]]
        print("Extracted pixels from file.\n")
        return pixels

    def addtoobj(self):
        print("Added pixels to class to begin rendering.")
        self.pixels = self.parser()
    def render(self):
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

        width = width[0]

        

        

if __name__ == "__main__":
    obj = ImageRenderLang("D:\..txt")
    obj.addtoobj()
    #obj.render(scale = 100, colormode="WB")
    print(obj.pixels)
