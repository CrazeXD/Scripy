import time
from PIL import Image, ImageDraw
import colors 
class RLEConversion:
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

    def render(self, colormode = "WB", scale = 1, backgroundcolor = "white"):
        #Check size
        self.pixels = self.parser()
        height = len(self.pixels)
        #Check width to make sure it's constant
        widths = []
        for i in self.pixels:
            for j in i:
                widths.append(len(j))
        for i in range(len(widths)):
            if widths[i-1]!=widths[i]:
                return "Error, width of image must be constant. Number of values in the rows of the file is not constant.\n"
        width = widths[0]
        image = Image.new(mode="RGB", size = (width, height), color = colors.get(backgroundcolor))
        draw = ImageDraw.Draw(image)
        startingcoords = [0, 0]
        for row in self.pixels:
            for item in row:
                for i in range(int(item[0])+1):
                    draw.rectangle([tuple(startingcoords), (startingcoords[0]+1, startingcoords[1]+1)], fill = {"W": "white", "B":"black"}[item[1]])
                    startingcoords[0]+=1
                startingcoords[1]+=1
        image.show()
        return

        

if __name__ == "__main__":
    obj = RLEConversion("D:\..txt", seperator = ",", colorname = True)
    obj.render(scale = 100, backgroundcolor = "blue2", colormode="WB")
    print(obj.pixels)