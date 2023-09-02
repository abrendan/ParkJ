import numpy as np
import cv2
import pickle
import sys

from tkinter import *
#from tkinter.filedialog import askopenfilenames 
from tkinter import filedialog
from zipfile import ZipFile 
from tkinter import ttk
from tkinter.messagebox import showinfo

#Width of the output in terminal characters
width = 80
height = 1 


#Our characters, and their approximate brightness values
charSet = " ,(S#g@@g#S(, "

# Generates a character sequence to set the foreground and background colors
def setColor (bg, fg):
  return "\u001b[48;5;%s;38;5;%sm" % (bg, fg)

black = setColor(16, 16)

# Load in color lookup table data
lerped =  pickle.load( open( "colors.pkl", "rb" ) )
LUT = np.load("LUT.npy")


root = Tk() 
root.geometry('400x300')
root.title("ParkJ")
root.configure(bg='black')


def select_file():
  global file_names
  file_names = filedialog.askopenfilename(initialdir = "/",title = "Select File",
            defaultextension=".*",
            filetypes=[("All Files", "*.*")])
  img = cv2.imread(file_names)
  src_height, src_width, _ = img.shape
  aspect_ratio = src_width / src_height
  height = int(width / (2 * aspect_ratio))
  img = cv2.resize(img, (width, height))
  print(convertImg(img))
  showinfo(
        title='Success',
        message="Successfully converted! Look in the terminal window."
    )




def convertImg(img):
  line = ""
  
  for row in img:
    for color in row:
      color = np.round(color).astype(int)

      b, g, r = color[0], color[1], color[2]

      # Lookup the color index in the RGB lookup table
      idx = LUT[b, g, r]
  
      # Get the ANSI color codes and lerp character
      bg, fg, lerp, rgb = lerped[idx]

      char = charSet[lerp]
  
      line += "%s%c" % (setColor(bg, fg), char)
    # End each line with a black background to avoid color fringe
    line += "%s\n" % black
  
  # Move the cursor back to the top of the frame to prevent rolling
  line += "\u001b[%iD\u001b[%iA" % (width, height + 1)
  return line





Label(root, bg='black', fg='purple', text="ParkJ", font="garamond 40 bold").pack(pady=10)
Label(root, bg='black', fg='purple', text="convert images to text", font="futura 12 bold").pack(pady=2)




Button(root, bg='#292929', fg='purple',text="Select image",command=select_file,font=14).pack(pady=10)

frame = Frame()
frame.pack(pady=20)



root.mainloop()

