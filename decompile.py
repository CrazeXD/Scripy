import os
from PIL import Image
import sys

def inverse(imagepath):
    im = Image.open(imagepath)
    rgb_im = im.convert('RGB')
    width = im.size[0]
    height = im.size[1]
    pixels = []
    for row in range(height):
        currentrow = []
        for col in range(width):
            currentrow.append(rgb_im.getpixel((col, row)))
        pixels.append(currentrow)
    for indexrow, row in enumerate(pixels):
        for index, item in enumerate(row):
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
                cr.append(str(count)+current)
                current = item
                count = 1
        cr.append(str(count)+current)
        code.append(cr)
    file = open(os.path.splitext(imagepath)[0]+".code", "w", encoding="utf-8")
    file.write("IMREN\n, \n")
    for row in code:
        for item in row:
            file.write(item)
            file.write(", ")
        file.write("\n")
    file.write("ENDREN")
    file.close()
    
inverse(sys.argv[1])