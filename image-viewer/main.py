# python 3.14.6
from tkinter import *
from PIL import Image, ImageTk
import glob

# root window
root = Tk()

# root window title & initial dimensions
root.title("SURE Image Viewer")
root.geometry('1920x1080')

# allow clicking to move focus
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())



# get all image names, sorted
images = glob.glob("Select Results/*")
images.sort()

# index of image currently accessed, default to 1st image
index = 0

# load initial image
image = Image.open(images[index])

# set width & height of enlargened crops
w = 244 * 5
h = 488 * 5

# crop initial image
# cropped: w=244, h=488
cropOrig = image.crop((9, 47, 252, 534)).resize((w, h))
cropOrig = ImageTk.PhotoImage(cropOrig)
cropCont = image.crop((9, 566, 252, 1053)).resize((w, h))
cropCont.putalpha(180)
cropCont = ImageTk.PhotoImage(cropCont)

# labels for image & image's filename
titleLabel = Label(root, text=images[index])
indexLabel = Label(root, text=index)

# canvas with layered crops
canvas = Canvas(root,
                width=750,
                height=750)
canvasOrig = canvas.create_image(0, 0, anchor=NW, image=cropOrig)
canvasCont = canvas.create_image(0, 0, anchor=NW, image=cropCont)

# case counts
correct = 0
adhesion = 0
missed = 0
miscap = 0

# case count labels
correctCount = Label(root, 
                     text="Correct = 0",
                     fg="#0A3A00")
adhesionCount = Label(root, 
                     text="Adhesion = 0",
                     fg="#5C3C00")
missedCount = Label(root, 
                     text="Missed = 0",
                     fg="#460000")
miscapCount = Label(root, 
                     text="Miscap = 0",
                     fg="#00025C")



# functions for changing displayed image

# reload the image so it displays the new one
# also reset all stats
def refreshImage():
    global image, cropOrig, cropCont, canvas, canvasOrig, canvasCont
    global w, h
    global indexLabel, titleLabel
    global correct, adhesion, missed, miscap
    global correctCount, adhesionCount, missedCount, miscapCount
    global contEnabled
    indexLabel.configure(text=index)
    titleLabel.configure(text=images[index])
    image = Image.open(images[index])
    cropOrig = image.crop((9, 47, 252, 534)).resize((w, h))
    cropOrig = ImageTk.PhotoImage(cropOrig)
    cropCont = image.crop((9, 566, 252, 1053)).resize((w, h))
    cropCont.putalpha(180)
    cropCont = ImageTk.PhotoImage(cropCont)
    canvas.delete('all')
    canvasOrig = canvas.create_image(0, 0, anchor=NW, image=cropOrig)
    canvasCont = canvas.create_image(0, 0, anchor=NW, image=cropCont)
    contEnabled = TRUE
    correct, adhesion, missed, miscap = 0, 0, 0, 0
    correctCount.configure(text="Correct = 0")
    adhesionCount.configure(text="Adhesion = 0")
    missedCount.configure(text="Missed = 0")
    miscapCount.configure(text="Miscap = 0")

# decrement image index
# only decrement if above min index (0)
def decrementImage(event=None):
    global index
    if index > 0:
        index -= 1
    refreshImage()

# increment image index
# only increment if below 99
def incrementImage(event=None):
    global index
    if index < 99:
        index += 1
    
    refreshImage()


# manual index entry

indexEntry = Entry(root, width=5)

def enterIndex():
    global index
    global indexEntry
    try:
        entry = int(indexEntry.get())
    except:
        print("Not a valid integer")
    else:
        if entry >= 0 and entry < 100:
            index = entry
    refreshImage()

entryBtn = Button(root, text="Enter",
                  command=enterIndex)


# placing points
# correct, adhesion, missed, miscaptured

def correctCase(event):
    global canvas, correct, correctCount
    color = "#31FF08"
    x, y = canvas.canvasx(event.x - 2), canvas.canvasy(event.y - 2)
    canvas.create_oval(x, y, x+4, y+4, fill=color)
    correct += 1
    correctCount.configure(text="Correct = "+str(correct))

def adhesionCase(event):
    global canvas, adhesion, adhesionCount
    color = "#FFA704"
    x, y = canvas.canvasx(event.x - 2), canvas.canvasy(event.y - 2)
    canvas.create_oval(x, y, x+4, y+4, fill=color)
    adhesion += 1
    adhesionCount.configure(text="Adhesion = "+str(adhesion))

def missedCase(event):
    global canvas, missed, missedCount
    color = "#FF0000"
    x, y = canvas.canvasx(event.x - 2), canvas.canvasy(event.y - 2)
    canvas.create_oval(x, y, x+4, y+4, fill=color)
    missed += 1
    missedCount.configure(text="Missed = "+str(missed))

def miscapCase(event):
    global canvas, miscap, miscapCount
    color = "#00EEFF"
    x, y = canvas.canvasx(event.x - 2), canvas.canvasy(event.y - 2)
    canvas.create_oval(x, y, x+4, y+4, fill=color)
    miscap += 1
    miscapCount.configure(text="Miscap = "+str(miscap))

canvas.bind("a", correctCase)
canvas.bind("s", adhesionCase)
canvas.bind("d", missedCase)
canvas.bind("f", miscapCase)


# move function

canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))


# key bindings
root.bind("q", decrementImage)
root.bind("e", incrementImage)

contEnabled = TRUE
def toggle(event=None):
    global contEnabled, canvas, canvasOrig, canvasCont
    if contEnabled:
        canvas.tag_lower(canvasCont)
        contEnabled = FALSE
    else:
        canvas.tag_lower(canvasOrig)
        contEnabled = TRUE

canvas.bind("<space>", toggle)



# visually display components
indexEntry.pack()
entryBtn.pack()
indexLabel.pack()
titleLabel.pack()
canvas.pack()
correctCount.pack()
adhesionCount.pack()
missedCount.pack()
miscapCount.pack()

root.mainloop()