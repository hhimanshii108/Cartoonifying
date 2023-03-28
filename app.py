import os
import cv2
import sys
import easygui
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt

root= tk.Tk()
root.geometry('700x700')
root.title('Choose to convert')
root.configure(background='light blue')
label = Label(root,background="black", font=("arial",30,"bold"))
def u():
    Imagepath=easygui.fileopenbox()
    c(Imagepath)
    
def c(Imagepath):
    originalimage = cv2.imread(Imagepath)
    originalimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2RGB)
# check if the image is chosen
    if originalimage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    R_1 = cv2.resize(originalimage, (930, 510))
    grayscaleimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2GRAY)
    R_2 = cv2.resize(grayscaleimage, (930, 510))
    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayscaleimage, 5)
    R_3 = cv2.resize(smoothGrayScale, (930, 510))
    #retrieving the edges for cartoon effect
    getedge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
      cv2.ADAPTIVE_THRESH_MEAN_C, 
      cv2.THRESH_BINARY, 9, 9)
    R_4 = cv2.resize(getedge, (930, 510))
    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalimage, 9, 300, 300)
    R_5 = cv2.resize(colorImage, (930, 510))
    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getedge)
    R_6 = cv2.resize(cartoonImage, (930, 510))

    #Plotting the whole transition
    images=[R_1, R_2, R_3, R_4, R_5, R_6]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    save1 = Button(root, text="Save cartoon image", command=lambda:save(R_6,Imagepath))
    save1.configure(background="#E6FFE6",foreground="black",font=('arial',20,"bold"))
    save1.pack(side=TOP,pady=50)
    plt.show()
def save(R_6, Imagepath):
    #saving an image using imwrite()
    newname="cartoonified_Image"
    path1 = os.path.dirname(Imagepath)
    extension=os.path.splitext(Imagepath)[1]
    path = os.path.join(path1, newname+extension)
    cv2.imwrite(path, cv2.cvtColor(R_6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newname +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
a=Button(root,text="Cartoonify an image",command=u,padx=15,pady=10)
a.configure(background='light grey', foreground='black',font=('ariel',30,'bold'))
a.pack(side=TOP,pady=50)
root.mainloop()
