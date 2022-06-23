from PIL import Image
import numpy as np
from turtle import *
import colors 
class ImageRenderLang:
    def __init__(self, filepath): #seperator = " "
        self._seperator = ","
        file = open(filepath)
        self._compressedValuesDefault = file.readlines()
        self._compressedValuesDefault = [value for value in self._compressedValuesDefault if value!="\n"] #Only get values that are not newlines
        
        #Remove the \n at the end
        for i in range(len(self._compressedValuesDefault)-1):
            self._compressedValuesDefault[i] = self._compressedValuesDefault[i][:-1]
        
        #Access header values then remove it
        self._compressedValuesDefault.pop(0)
        if self._compressedValuesDefault[0] == "WB" or self._compressedValuesDefault[0] == "RGB":
            self._colormode = self._compressedValuesDefault[1]
        else:
            print("Error, no color mode specified for a image render. Terminating process.")
            exit()
        self._compressedValuesDefault.pop(0)
        try:
            self._scale = int(self._compressedValuesDefault[0])
            self._compressedValuesDefault.pop(0)
        except:
            self._scale = 1
        self._backgroundcolor = colors.get(self._compressedValuesDefault[0])
        self._compressedValuesDefault.pop(0)

    def parser(self):
        #Parse the seperators and add pixels into individual arrays
        compressedpixels = []
        for linenumber, row in enumerate(self._compressedValuesDefault):
            currentrow = row.split(self._seperator)
            #Pop the 0s
            for item in range(len(currentrow)-1):
                if currentrow[item].startswith("0"):
                    print(f"Removed item {currentrow[item]} from row {linenumber+1} due to 0 start value.")
                    currentrow.pop(item)
            compressedpixels.append(currentrow)
        #compressedpixels -> 2D Array, X-Axis = Row, Y-Axis = Item with color
        #Convert compressedpixels into 3d array, with Y-Axis becoming items in a row and Z-Axis becoming the number/color of the pixel only do if colorname == True
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for row in range(len(compressedpixels)):
            for itemindex in range(len(compressedpixels[row])):
                indexstart = 0
                for index, charachter in enumerate(compressedpixels[row][itemindex]):
                    if str(charachter).lower() in letters:
                        indexstart = index
                        break
                compressedpixels[row][itemindex] = [compressedpixels[row][itemindex][:indexstart], compressedpixels[row][itemindex][indexstart:]]
        print("Extracted pixels from file.\n")
        return compressedpixels

    def addtoobj(self):
        print("Added pixels to class to begin rendering.")
        self.compressedpixels = self.parser()

    def convertToIndividual(self):
        pixels = []
        #Why on earth is self._colormode == 1
        #if self._colormode == "WB":
        colorlist = {"W": "white", "B": "black"}
        for row in self.compressedpixels:
            newrow = []
            for item in row:
                newitem = colors.get(colorlist[item[1]]) #Seperate pixels into individual ones instead of multiplied, and convert color into tuple of RGB
                for _ in range(int(item[0])+1):
                    newrow.append(newitem)
            pixels.append(newrow)
        return pixels

    def render(self):
        pixels = self.convertToIndividual()
        print(pixels)
        # Convert the pixels into an array using numpy
        array = np.array(pixels, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array)
        new_image.save('new.png')

        

        

if __name__ == "__main__":
    obj = ImageRenderLang("D:\..txt")
    obj.addtoobj()
    obj.convertToIndividual()
    obj.render()
