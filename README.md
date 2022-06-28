# Scripy

## Am Image Rendering Language

### Made by Craze

**Scripy** is an image rendering language that allows you to write out the pixels of an image

## Documentation
For example, the following code will create alternating white and black lines 4 pixels long.
    
    @OP OFF
    IMREN
    ,
    4W,
    4B,
    4W,
    4B
    ENDREN

### How to write:
In the first line of the code, you can disable status updates by writing @OP OFF. It must be on the first line. This is not required.

On the next line, write the word IMREN in capitols. This tells the code to start compiling at that point.

Next, write the seperator in between values. If you have a space after the seperators in your code, you must put one on the line here as well.

Then, start writing your code. To write the code, write a number, then either a hex code or charachters. These charachters represent common colors.

Here is a list of them that are in the program, written as a dictionary:
{"W": "white", "B": "black", "A": "aqua", "BL": "blue", "BR": "brown", "C": "cyan", "GO": "gold", "G": "gray", "GR": "green", "I": "indigo", "M": "magenta", "O": "orange", "P": "pink", "PU": "purple", "R": "red", "V": "violet", "Y": "yellow"}

Note: RGB Values for these colors can be found in colors.py.

In the last line, write ENDREN. This will tell the program to stop reading the lines at that point. This can be useful if you are testing out what images will look like if you remove certain rows from the end.

For any row, you may comment it out using // in the beginning of the row.

To run, navigate to where you have the scripy.exe file.

Launch it with 2 arguments, the first being the path to your code file. If the code file is in the same directory as the .exe, you may simply type the name of the file (must have the extension). 

The 2nd argument should be the path(with filename and extension) where you want to save the image. For example, D:\main.png could be passed in.

### Turn Images Into Code

To turn an image into code, run the scripy exe with 2 arguments. 

The first should be the path to the image with a file extension of either "png", "jpg", "jpeg", or "bmp".

The second should be the path to the code you want, without a filename or extension. The filename will be the same as that of the image file.

Please note, if the path for the second argument on any commands doesn't exist, the code will break.