'''
Python 2.7 slideshow for Glenn
modified from https://gist.github.com/terencewu/034e09f0e318c621516b

All images must be dropped in a folder called ./images

Usage: python slideShow.py
'''

import Tkinter as tk
from PIL import Image, ImageTk
import time
import sys
import os
import random


class HiddenRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # hackish way, essentially makes root window
        # as small as possible but still "focused"
        # enabling us to use the binding on <esc>
        self.wm_geometry("0x0+0+0")

        self.window = MySlideShow(self)
        self.window.startSlideShow()



class MySlideShow(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        # remove window decorations
        self.overrideredirect(True)

        # save reference to photo so that garbage collection
        # does not clear image variable in show_image()
        self.persistent_image = None
        self.imageList = []
        self.pixNum = 0

        print " creating my images "
        scr_w, scr_h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.prevImage = Image.new("RGB", (scr_w, scr_h), "black")
        self.mixImage = Image.new("RGB", (scr_w, scr_h), "black")

        # used to display as background image
        #self.label = tk.Label(self)
        #self.label.pack(side="top", fill="both", expand=True)
        
        # v2
        self.label = tk.Label(self, image=self.persistent_image)
        self.label.pack(side="top", fill="both", expand=True)

        self.label.configure(background='black')
        self.label.configure(cursor='none')

        print "Loading images... "

        self.getImages()

    def getImages(self):
        '''
        Get image directory from command line or use current directory
        '''
        print("getting images...")

        curr_dir = './images'

        for root, dirs, files in os.walk(curr_dir):
            for f in files:
                if f.endswith(".png") or f.endswith(".jpg"):
                    img_path = os.path.join(root, f)
                    print(img_path)
                    self.imageList.append(img_path)

    def startSlideShow(self, delay=1):  # delay in seconds
        filename = random.choice(self.imageList)
        # self.imageList[self.pixNum]
        # self.pixNum = (self.pixNum + 1) % len(self.imageList)
        self.showImage(filename)
        # its like a callback function after n seconds (cycle through pics)
        self.after(delay*1000, self.startSlideShow)

    def showImage(self, filename):
        print " "
        print "Showing image: ", filename

        loadImg = Image.open(filename)

        img_w, img_h = loadImg.size
        scr_w, scr_h = self.winfo_screenwidth(), self.winfo_screenheight()

        imgScale = min(float(scr_w )/float(img_w), float(scr_h)/float(img_h))
        print "  image scale: ", imgScale

        width, height = min(scr_w , img_w), min(scr_h, img_h)
        if imgScale < 1:
            width, height = int(img_w * imgScale), int(img_h * imgScale)
        else:
            print " WARNING imgscale ", imgScale

        print "  image size: ", img_w, " x ", img_h
        print "  screen size: ", scr_w, " x ", scr_h
        print "  scaled: ", width, " x ", height

        # resizes image, makes everything faster
        loadImg.thumbnail((width, height), Image.ANTIALIAS)
        # print " created the thumbnail, now resize to screen version"
        curImage = Image.new("RGB", (scr_w, scr_h), "black")
        curImage.paste(loadImg, (int((scr_w - width )/2), int((scr_h - height)/2)))

        if not self.prevImage:
            self.prevImage = curImage
            print "There was no image loaded yet"
            return


        alpha = 0
        while 1.0 > alpha:
            # print " alpha: " , alpha
            self.mixImage = Image.blend(self.prevImage, curImage, alpha)
            alpha = alpha + 0.01
            self.persistent_image = ImageTk.PhotoImage(self.mixImage)
            self.label.configure(image=self.persistent_image)
            self.label.update()
            time.sleep(0.001)



        self.prevImage = curImage


if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

'''
#create main window
master = tk.Tk()
master.title("tester")
master.geometry("300x100")
'''


slideShow = HiddenRoot()
slideShow.bind("<Escape>", lambda e: slideShow.destroy())  # exit on esc
slideShow.mainloop()
