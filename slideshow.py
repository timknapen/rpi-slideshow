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
        #hackish way, essentially makes root window
        #as small as possible but still "focused"
        #enabling us to use the binding on <esc>
        self.wm_geometry("0x0+0+0")

        self.window = MySlideShow(self)
        self.window.startSlideShow()


class MySlideShow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
      
        #remove window decorations 
        self.overrideredirect(True)

        #save reference to photo so that garbage collection
        #does not clear image variable in show_image()
        self.persistent_image = None
        self.imageList = []
        self.pixNum = 0

        #used to display as background image
        self.label = tk.Label(self)
        self.label.pack(side="top", fill="both", expand=True)
        self.label.configure(background='black')
        self.label.configure(cursor='none')

        scr_w, scr_h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.wm_geometry("{}x{}+{}+{}".format(scr_w,scr_h,0,0))
        self.getImages()
        
        

    def getImages(self):
        '''
        Get image directory from command line or use current directory
        '''
        print("Getting images...")
    
        curr_dir = './images'
        imageCounter = 0
        for root, dirs, files in os.walk(curr_dir):
            for f in files:
                if f.endswith(".png") or f.endswith(".jpg"):
                    img_path = os.path.join(root, f)
                    imageCounter += 1
                    print imageCounter, " ", img_path
                    self.imageList.append(img_path)

        print("")


    def startSlideShow(self, maxDelay=5): #delay in seconds
        myimage = random.choice(self.imageList) 
        # self.imageList[self.pixNum]
        # self.pixNum = (self.pixNum + 1) % len(self.imageList)
        self.showImage(myimage)
        #its like a callback function after n seconds (cycle through pics)
        thisDelay = random.randrange(0, maxDelay, 1) #choose a random delay between 0 and maxDelay in seconds
        print "  Waiting ", thisDelay, " seconds"
        print ""
        self.after(thisDelay*1000, self.startSlideShow)


    def showImage(self, filename):
        print "Showing image: " , filename
        image = Image.open(filename)  

        img_w, img_h = image.size
        scr_w, scr_h = self.winfo_screenwidth(), self.winfo_screenheight()

        imgScale = min(float(scr_w)/float(img_w), float(scr_h)/float(img_h))

        width, height = min(scr_w, img_w), min(scr_h, img_h)
        if imgScale < 1: #only scale down!
            width, height = img_w * imgScale, img_h * imgScale
        else:
            print "  Not scaling "
        
        print "  Screen size: " , scr_w , " x " , scr_h
        print "  Image size: " , img_w , " x " , img_h
        print "  Scale factor: " , imgScale
        print "  Scaled: " , width , " x ", height

        image.thumbnail((width, height), Image.ANTIALIAS) #resizes image, makes everything faster

        # create new image 
        self.persistent_image = ImageTk.PhotoImage(image)
        self.label.configure(image=self.persistent_image)


if os.environ.get('DISPLAY','') == '':
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