from PIL import Image
import numpy as np
from turtle import *
import colors
import sys

def ImageRender(filepath):
    #Open and read the file
    file = open(filepath)
    compressedValuesDefault = file.readlines()
    #Only get values that are not newlines
    compressedValuesDefault = [value for value in compressedValuesDefault if value!="\n"]
    
    #Remove the \n at the end of each row
    for i in range(len(compressedValuesDefault)-1):
        compressedValuesDefault[i] = compressedValuesDefault[i][:-1]
    
    #Turn output off
    if compressedValuesDefault[0] == "@OP OFF":
        printing = False
        #Make sure to pop the line
        compressedValuesDefault.pop(0)
    else:
        printing = True
    #Access header values then remove it

    #Pop the type
    compressedValuesDefault.pop(0)
    
    seperator = compressedValuesDefault[0]
    compressedValuesDefault.pop(0)
    #Find image render end
    for index, row in enumerate(compressedValuesDefault):
        if row == "ENDREN":
            if index!=len(compressedValuesDefault)-1:
                compressedValuesDefault = compressedValuesDefault[:index]
                compressedValuesDefault.pop(-1)
                break
        elif index+1 == len(compressedValuesDefault) and row != "ENDREN":
            if printing != False:
                print("EOS Error: No end on image render. Assuming end of file is the end of the image...")
    #Parse the seperators and add pixels into individual arrays
    compressedpixels = []
    for linenumber, row in enumerate(compressedValuesDefault):
        currentrow = row.split(seperator)
        #Pop the 0s
        for item in range(len(currentrow)-1):
            if currentrow[item].startswith("0"):
                if printing != False:
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
    if printing != False:
        print("Extracted pixels from file.")
    compressedpixels.pop(-1)
    pixels = []
    colorlist = {"W": "white", "B": "black", "A": "aqua", "BL": "blue", "BR": "brown", "C": "cyan", "GO": "gold", "G": "gray", "GR": "green", "I": "indigo", "M": "magenta", "O": "orange",
                    "P": "pink", "PU": "purple", "R": "red", "V": "violet", "Y": "yellow"}
    
    for row in compressedpixels:
        newrow = []
        for item in row:
            if item[1].startswith("#"):
                h = item[1].lstrip('#') #Get the hex code
                newitem = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            else:
                newitem = colors.get(colorlist[item[1]]) #Seperate pixels into individual ones instead of multiplied, and convert color into tuple of RGB
            for _ in range(int(item[0])):
                newrow.append(newitem)
        pixels.append(newrow)
    # Convert the pixels into an array using numpy
    try:
        array = np.array(pixels, dtype=np.uint8)
    except:
        print("Length error: Length of rows is not constant. This could be due to a 0 starting value, or a missing pixel.")
        exit()
    # Use PIL to create an image from the new array of pixels
    print("Rendering Image. Depending on the size of your file and your computer, this could take time.") if printing == True else print()
    new_image = Image.fromarray(array)
    new_image.save('new.png')
    print("Render completed.")



if __name__ == '__main__':
    try: 
       filepath = r"{}".format(sys.argv[1])
    except IndexError:
        print("Fatal error: Missing input file.")
        exit()
    if filepath.endswith(".code"):
        opened = open(filepath, "r", encoding="utf-8")
    else:
        print("Fatal error: Invalid input file.")
        exit()

    readlines = opened.readlines()
    opened.close()
    if readlines[0] == "@OP OFF":
        type = readlines[1]
    else:
        type = readlines[0]
    if type == "IMREN\n":
        ImageRender(filepath)