from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Tk, colorchooser, filedialog, Button, Entry, StringVar, Label, PhotoImage, Canvas, Toplevel, Spinbox, Scale, StringVar, HORIZONTAL, VERTICAL, CENTER

root = Tk()
root.geometry('1024x768')

global img
global file
global s
global x1, y1
global x2, y2
global crop
global draw
global color

color = ['', 'red']
print(color)

crop = False
draw = False


def save():
    filename = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[
                                            ('PNG Image', '*.png *.PNG'), ('JPG Image', '*.jpg *.JPG')])
    print(filename)
    convert(filename)


def up(event):
    global x2, y2
    global s
    global crop
    global draw
    x2, y2 = event.x, event.y
    print('{}, {}'.format(x2, y2))
    if(crop == True and draw != True):
        canvas.delete(s)
        imgCrop(x1, x2, y1, y2)
    elif(crop == False and draw != True):
        canvas.delete(s)
        imgResize(x1, x2, y1, y2)


def motion(event):
    global x1, y1
    global imgC
    global draw
    global color

    if(draw == True):
        x1, y1 = event.x, event.y
        print('{}, {}'.format(x1, y1))
        paint = canvas.create_rectangle(
            x1, y1, x1 + size.get(), y1 + size.get(), fill=color[1], outline='')
    else:
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))
        canvas.coords(s, x1, y1, x, y)


def place(event):
    global s
    global x1, y1
    global draw
    global color

    if(draw == True):
        x1, y1 = event.x, event.y
        print('{}, {}'.format(x1, y1))
        paint = canvas.create_oval(
            x1, y1, x1 + size.get(), y1 + size.get(), fill=color[1], outline='')
    else:
        x1, y1 = event.x, event.y
        print('{}, {}'.format(x1, y1))
        s = canvas.create_rectangle(x1, y1, x1, y1, fill='')


def convert(filename):
    global img
    img._PhotoImage__photo.write(filename)
    img = Image.open(filename).convert("RGB")
    img.save(filename)


def upload():
    global file
    global img
    file = filedialog.askopenfilename()
    print(file)

    img = Image.open(file)
    img.resize((1920, 1080), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(file=file)
    imag(img)


def imgCrop(x1, x2, y1, y2):
    left = (x2 - x1) / 4
    top = (y2 - y1) / 4
    right = 3 * (x2 - x1) / 4
    bottom = 3 * (y2 - y1) / 4
    global file
    global img
    img = Image.open(file)
    img = img.crop((x1, y1, x2, y2))
    img = ImageTk.PhotoImage(img)
    imag(img)


def cropTrue():
    global crop
    global draw
    draw = False
    crop = True
    print(crop)


def cropFalse():
    global crop
    global draw
    draw = False
    crop = False
    print(crop)


def drawTrue():
    global draw
    global crop
    crop = False
    draw = True


def imgResize(x1, x2, y1, y2):
    global file
    global img
    img = Image.open(file)
    img = img.resize((x2 - x1, y2 - y1))
    img = ImageTk.PhotoImage(img)
    imag(img)


def colorSelect():
    global color
    color = colorchooser.askcolor()


def imag(img):
    global canvas
    print(img)
    canvas.postscript(file='canvas.png', colormode='color')
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    uploaded = canvas.create_image(
        width / 2, height / 2, image=img, anchor='center')
    uploaded.place(relx=.5, rely=.5)


uploadBtn = Button(root, text='Upload', command=upload)
uploadBtn.place(relx=.45, rely=.025, relwidth=.125, relheight=.05)

size = Scale(root, from_=1, to=50, orient=HORIZONTAL)
size.place(relx=.015, rely=.4, relwidth=.075, relheight=.05)

colorBtn = Button(root, text='Choose Color', command=colorSelect)
colorBtn.place(relx=.015, rely=.45, relwidth=.075, relheight=.05)

canvas = Canvas(bg='light gray')
canvas.place(relx=.1, rely=.1, relwidth=.8, relheight=.8)

save = Button(root, text='Save', command=save)
save.place(relx=.45, rely=.925, relwidth=.125, relheight=.05)

cropBtn = Button(root, text='Crop', command=cropTrue)
cropBtn.place(relx=.015, rely=.1, relwidth=.075, relheight=.1)

resizeBtn = Button(root, text='Resize', command=cropFalse)
resizeBtn.place(relx=.015, rely=.2, relwidth=.075, relheight=.1)

drawBtn = Button(root, text='Draw', command=drawTrue)
drawBtn.place(relx=.015, rely=.3, relwidth=.075, relheight=.1)

cropP = Label(canvas, bg='gray50')

# ResizeBtn1 = Button(canvas, text='', bg='gray')
# ResizeBtn1.place(relx=.975, rely=.0, relwidth=.025, relheight=.04)

canvas.bind('<Button-1>', place)
canvas.bind('<B1-Motion>', motion)
canvas.bind('<ButtonRelease-1>', up)

root.mainloop()
