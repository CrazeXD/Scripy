import os
from PIL import Image
import numpy as np
from turtle import *
import colors
import sys
colorlist = {"W": "white", "B": "black", "A": "aqua", "BL": "blue", "BR": "brown", "C": "cyan", "GO": "gold", "G": "gray", "GR": "green", "I": "indigo", "M": "magenta", "O": "orange",
                    "P": "pink", "PU": "purple", "R": "red", "V": "violet", "Y": "yellow"}
def ImageRender(filepath, savepath):  # sourcery skip: low-code-quality
    file = open(filepath)
    compressedValuesDefault = file.readlines()
    compressedValuesDefault = [value for value in compressedValuesDefault if value != "\n"]

    for i in range(len(compressedValuesDefault) - 1):
        compressedValuesDefault[i] = compressedValuesDefault[i][:-1]
    if compressedValuesDefault[0] == "@OP OFF":
        printing = False
        compressedValuesDefault.pop(0)
    else:
        printing = True
    compressedValuesDefault.pop(0)
    seperator = compressedValuesDefault[0]
    compressedValuesDefault.pop(0)
    for index, row in enumerate(compressedValuesDefault):
        if row == "ENDREN":
            if index != len(compressedValuesDefault) - 1:
                compressedValuesDefault = compressedValuesDefault[:index]
                compressedValuesDefault.pop(-1)
                break
        elif index + 1 == len(compressedValuesDefault):
            if printing:
                print("EOS Error: No end on image render. Assuming end of file is the end of the image...")

    for linenumber, row in enumerate(compressedValuesDefault):
        if row.startswith("//"):
            compressedValuesDefault.pop(linenumber)
    compressedpixels = []
    for linenumber, row in enumerate(compressedValuesDefault):
        currentrow = row.split(seperator)
        for item in range(len(currentrow) - 1):
            if currentrow[item].startswith("0"):
                if printing:
                    print(f"Removed item {currentrow[item]} from row {linenumber + 1} due to 0 start value.")

                currentrow.pop(item)
        compressedpixels.append(currentrow)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for compressedpixel in compressedpixels:
        for itemindex in range(len(compressedpixel)):
            indexstart = 0
            for index, charachter in enumerate(compressedpixel[itemindex]):
                if charachter == "#":
                    indexstart = index
                    break
                elif str(charachter).lower() in letters:
                    indexstart = index
                    break
            compressedpixel[itemindex] = [compressedpixel[itemindex][:indexstart], compressedpixel[itemindex][indexstart:]]

    if printing:
        print("Extracted pixels from file.")
    compressedpixels.pop(-1)
    pixels = []
    for row in compressedpixels:
        newrow = []
        for item in row:
            if item[1].startswith("#"):
                h = item[1].lstrip('#')
                newitem = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            else:
                newitem = colors.get(colorlist[item[1]])
            try:
                newrow.extend(newitem for _ in range(int(item[0])))
            except ValueError:
                print("Fatal error: Missing numeric value before pixel color.")
                sys.exit()
        pixels.append(newrow)
    try:
        array = np.array(pixels, dtype=np.uint8)
    except Exception:
        print("Length error: Length of rows is not constant. This could be due to a 0 starting value, or a missing pixel.")

        sys.exit()
    print("Rendering Image. Depending on the size of your file and your computer, this could take time.") if printing else print()

    new_image = Image.fromarray(array)
    try:
        new_image.save(savepath)
    except SystemError:
        print("Syntax Error: You are missing the seperator. Please add a seperator to your file.")

        sys.exit()
    except ValueError:
        print("Argument Error: You have an invalid save path.")
        sys.exit()
    print("Render completed.")
    return None

def inverse(imagepath, savepath):  # sourcery skip: low-code-quality
    if not os.path.isfile(imagepath):
        print("File not found.")
        sys.exit()
    im = Image.open(imagepath)
    rgb_im = im.convert('RGB')
    width = im.size[0]
    height = im.size[1]
    pixels = []
    for row in range(height):
        currentrow = [rgb_im.getpixel((col, row)) for col in range(width)]
        pixels.append(currentrow)
    for indexrow, row in enumerate(pixels):
        for index, item in enumerate(row):
            if item in list(colors.colors().values()):
                keys = list(colors.colors().keys())
                for k in keys:
                    if colors.colors()[k] == item:
                        colorlistvalues = list(colorlist.values())
                        colorlistkeys = list(colorlist.keys())
                        colorindex = colorlistvalues.index(k)
                        coloritem = colorlistkeys[colorindex]
                        pixels[indexrow][index] = coloritem
            else:
                pixels[indexrow][index] = '#%02x%02x%02x' % item
    code = []
    '''Make a run length encoding algorithm for the pixels'''
    count = 1
    for row in pixels:
        current = row[0]
        cr = []
        for index, item in enumerate(row):
            if index == 0:
                pass
            elif item == current:
                count += 1
            else:
                cr.append(str(count) + current)
                current = item
                count = 1
        cr.append(str(count) + current)
        code.append(cr)
    with open(savepath + os.path.splitext(imagepath)[0].rsplit("\\")[1] + ".code", "w", encoding="utf-8") as file:
        file.write("IMREN\n, \n")
        for indexrow, row in enumerate(code):
            for index, item in enumerate(row):
                file.write(item)
                if indexrow != len(code) - 1 or index != len(row) - 1:
                    file.write(", ")
            file.write("\n")
        file.write("ENDREN")
    print("Decompile completed.")
# sourcery skip: avoid-builtin-shadow
if __name__ == '__main__':
    try: 
        filepath = f"{sys.argv[1]}"
        savepath = f"{sys.argv[2]}"
    except IndexError:
        print("Argument error: Missing input file(s).")
        sys.exit()
    if not os.path.isfile(filepath):
        print("Argument Error: File not found.")
        sys.exit()
    if filepath.endswith(".code"):
        opened = open(filepath, "r", encoding="utf-8")
    elif filepath.endswith(("png", "jpg", "jpeg", "bmp")):
        inverse(filepath, savepath)
        sys.exit()
    else:
        print("Fatal error: Invalid input file.")
        sys.exit()

    readlines = opened.readlines()
    opened.close()
    type = readlines[1] if readlines[0] == "@OP OFF" else readlines[0]
    if type == "IMREN\n":
        ImageRender(filepath, savepath)
