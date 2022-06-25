import sys
from PIL import Image
import numpy as np
from turtle import *
import colors

class ImageRender:
    def __init__(self, filepath):
         #Open and read the file
        file = open(filepath)
        self._compressedValuesDefault = file.readlines()
        #Only get values that are not newlines
        self._compressedValuesDefault = [value for value in self._compressedValuesDefault if value!="\n"]
        
        #Remove the \n at the end of each row
        for i in range(len(self._compressedValuesDefault)-1):
            self._compressedValuesDefault[i] = self._compressedValuesDefault[i][:-1]
        
        #Turn output off
        if self._compressedValuesDefault[0] == "@OP OFF":
            self._printing = False
            #Make sure to pop the line
            self._compressedValuesDefault.pop(0)
        else:
            self._printing = True
        #Access header values then remove it

        #Pop the type
        self._compressedValuesDefault.pop(0)
        
        self._seperator = self._compressedValuesDefault[0]
        self._compressedValuesDefault.pop(0)
        #Find image render end
        for index, row in enumerate(self._compressedValuesDefault):
            if row == "ENDREN":
                if index!=len(self._compressedValuesDefault)-1:
                    self.existscommands = True
                    self._compressedValuesDefault = self._compressedValuesDefault[:index]
                    self._compressedValuesDefault.pop(-1)
                    self.commandIndexStartInclusive = index+1
                    self.commandListRows = self._compressedValuesDefault[index+1:]
                    break
                else:
                    self.existscommands = False #Are commands there
            elif index+1 == len(self._compressedValuesDefault) and row != "ENDREN":
                if self._printing != False:
                    print("EOS Error: No end on image render. Assuming end of file is the end of the image...")


    def parse(self):
        #Parse the seperators and add pixels into individual arrays
        compressedpixels = []
        for linenumber, row in enumerate(self._compressedValuesDefault):
            currentrow = row.split(self._seperator)
            #Pop the 0s
            for item in range(len(currentrow)-1):
                if currentrow[item].startswith("0"):
                    if self._printing != False:
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
                    if charachter == "#":
                        indexstart = index
                        break
                    elif str(charachter).lower() in letters:
                        indexstart = index
                        break
                compressedpixels[row][itemindex] = [compressedpixels[row][itemindex][:indexstart], compressedpixels[row][itemindex][indexstart:]]
        if self._printing != False:
            print("Extracted pixels from file.")
        compressedpixels.pop(-1)
        return compressedpixels

    def addtoobj(self):
        if self._printing != False:
            print("Added pixels to class to begin rendering.")
        self.compressedpixels = self.parse()
    
    def convertToIndividual(self):
        pixels = []
        #Why on earth is self._colormode == 1
        #if self._colormode == "WB":
        colorlist = {"W": "white", "B": "black", "A": "aqua", "BL": "blue", "BR": "brown", "C": "cyan", "GO": "gold", "G": "gray", "GR": "green", "I": "indigo", "M": "magenta", "O": "orange",
                     "P": "pink", "PU": "purple", "R": "red", "V": "violet", "Y": "yellow"}
        
        for row in self.compressedpixels:
            newrow = []
            for item in row:
                if item[1].startswith("#"):
                    h = item[1].lstrip('#') #Get the hex code
                    newitem = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                else:
                   newitem = colors.get(colorlist[item[1]]) #Seperate pixels into individual ones instead of multiplied, and convert color into tuple of RGB
                for _ in range(int(item[0])+1):
                    newrow.append(newitem)
            pixels.append(newrow)
        return pixels


    def render(self):
        pixels = self.convertToIndividual()
        # Convert the pixels into an array using numpy
        try:
            array = np.array(pixels, dtype=np.uint8)
        except:
            print("Length error: Length of rows is not constant. This could be due to a 0 starting value, or a missing pixel.")
            exit()
        # Use PIL to create an image from the new array of pixels
        print("Rendering Image. Depending on the size of your file and your computer, this could take time.") if self._printing == True else print()
        new_image = Image.fromarray(array)
        new_image.save('new.png')
        print("Render completed.")

class ImageCommands:

    def crop(self, crops):
        self._im.crop(crops)
    def rotate(self, theta):
        self._im.rotate(theta)
    def evalcomands(self):
        for index, i in enumerate(self.commands):
            commandlist = {"ROTATE": "self.rotate(commandparams)", "CROP": "self.crop(commandparams)"}
            for command in commandlist:
                if command in i:
                    commandparams = i[len(command)+1:]
                    try:
                        eval(commandlist[command])
                    except:
                        print(f"Fatal error: Line {index+self.commandindexstart} -> Invalid arguments.")
                else:
                    pass

    def __init__(self, imagePath, commands = None, file = None, commandindexstart = 0):
        if commands == None and file == None:
            print("Fatal Error: No base input provided for image altercation.")
            exit()
        elif any([commands, file] == ""):
            print("Fatal error: Filepath is empty.")
            exit()
        if commands == None:
            filer = file.open()
            self.commands = filer.readlines()
            filer.close()
            self.commands.pop(0) #COMMANDS
            for index, j in enumerate(self.commands):
                if j == "ENDCOMMANDS":
                    endindex = index
            if not any(self.commands == "ENDCOMMANDS"):
                print("EOS Error: No end on image commands. Assuming end of file is the end of the commands...")
            self.commands.pop(endindex) #ENDCOMMANDS
        elif file == None:
            self.commands = commands
        self._im = Image.open(imagePath)
        
        

if __name__ == "__main__":
    try: 
       file = r"{}".format(sys.argv[1])
    except IndexError:
        print("Fatal error: Missing input file.")
        exit()
    if file.endswith(".code"):
        opened = open(file, "r", encoding="utf-8")
    else:
        print("Fatal error: Invalid input file.")
        exit()

    readlines = opened.readlines()
    opened.close()
    if readlines[0] == "@OP OFF":
        type = readlines[1]
    else:
        type = readlines[0]
    print(type)
    if type == "IMREN\n":
        starter = ImageRender(file)
        print(starter.parse())
        starter.addtoobj()
        starter.render()
