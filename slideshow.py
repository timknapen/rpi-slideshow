#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Based on the slideshow demo from PI3D https://pi3d.github.io
"""
import random, time, glob, threading
import sys
sys.path.insert(1, '/home/pi/pi3d')
import pi3d

from six_mod.moves import queue

print("press ESC to escape, S to go back, any key for next slide")

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(background=(0.0, 0.0, 0.0, 1.0), frames_per_second=60)
shader = pi3d.Shader("uv_flat")

CAMERA = pi3d.Camera(is_3d=False)

iFiles = glob.glob("images/*.jpg") # only jpg images
nFi = len(iFiles)
fileQ = queue.Queue() # queue for loading new texture files

alpha_step = 0.025
nSli = 8
drawFlag = False
autoPlay = True

def tex_load():
  
  while True:
    item = fileQ.get()

    fname = item[0]
    slide = item[1]

    #tex = pi3d.Texture(item[0], mipmap=False) #pixelly but faster 3.3MB in 3s
    tex = pi3d.Texture(item[0], blend=True, mipmap=True) #nicer but slower 3.3MB in 4.5s
    xrat = DISPLAY.width/tex.ix
    yrat = DISPLAY.height/tex.iy
    if yrat < xrat:
      xrat = yrat
    wi, hi = tex.ix * xrat, tex.iy * xrat
    slide.set_draw_details(shader,[tex])
    slide.scale(wi, hi, 1.0)
    slide.set_alpha(0)
    fileQ.task_done()


class Slide(pi3d.Sprite):
  def __init__(self):
    super(Slide, self).__init__(w=1.0, h=1.0)
    self.visible = False
    self.fadeup = False
    self.active = False


class Carousel:
  def __init__(self):
    self.slides = [None]*nSli
    half = 0
    for i in range(nSli):
      self.slides[i] = Slide()
    for i in range(nSli):
      # never mind this, hop is just to fill in the first series of images from
      # inside-out: 4 3 5 2 6 1 7 0.
      half += (i%2)
      step = (1,-1)[i%2]
      hop = 4 + step*half

      self.slides[hop].positionZ(0.8-(hop/10))
      item = [iFiles[hop%nFi], self.slides[hop]]
      fileQ.put(item)

    self.focus = 3 # holds the index of the focused image
    self.focus_fi = 0 # the file index of the focused image
    self.slides[self.focus].visible = True
    self.slides[self.focus].fadeup = True

  def next(self):
    self.slides[self.focus].fadeup = False
    self.focus = (self.focus+1)%nSli
    self.focus_fi = (self.focus_fi+1)%nFi
    # the focused slide is set to z = 0.1.
    # further away as i goes to the left (and wraps)
    # print ('Focus: ' , self.slides[self.focus])
    for i in range(nSli):
      self.slides[(self.focus-i)%nSli].positionZ(0.1*i + 0.1)
    self.slides[self.focus].fadeup = True
    self.slides[self.focus].visible = True

    fileName = iFiles[(self.focus_fi+4)%nFi]
    item = [fileName, self.slides[(self.focus-4)%nSli]]
    print('Loading: ', fileName)
    fileQ.put(item)

  def prev(self):
    self.slides[self.focus].fadeup = False
    self.focus = (self.focus-1)%nSli
    self.focus_fi = (self.focus_fi-1)%nFi
    for i in range(nSli):
      self.slides[(self.focus-i)%nSli].positionZ(0.1*i + 0.1)
    self.slides[self.focus].fadeup = True
    self.slides[self.focus].visible = True

    item = [iFiles[(self.focus_fi-3)%nFi], self.slides[(self.focus+5)%nSli]]
    fileQ.put(item)

  def update(self):
    # for each slide check the fade direction, bump the alpha and clip
    fadeDone = True
    for i in range(nSli):
      a = self.slides[i].alpha()
      if self.slides[i].fadeup == True and a < 1:
        a += alpha_step
        self.slides[i].set_alpha(a)
        self.slides[i].visible = True
        self.slides[i].active = True
        fadeDone = False # still fading
      elif self.slides[i].fadeup == False and a > 0:
        a -= alpha_step
        self.slides[i].set_alpha(a)
        self.slides[i].visible = True
        self.slides[i].active = True
        fadeDone = False # still fading
      else:
        if a <= 0:
          self.slides[i].visible = False
        self.slides[i].active = False
      
    if fadeDone and autoPlay:
      self.next()


  def draw(self):
    # slides have to be drawn back to front for transparency to work.
    # the 'focused' slide by definition at z=0.1, with deeper z
    # trailing to the left.  So start by drawing the one to the right
    # of 'focused', if it is set to visible.  It will be in the back.
    for i in range(nSli):
      ix = (self.focus+i+1)%nSli
      if self.slides[ix].visible == True:
        self.slides[ix].draw()


crsl = Carousel()

t = threading.Thread(target=tex_load)
t.daemon = True
t.start()

# block the world, for now, until all the initial textures are in.
# later on, if the UI overruns the thread, there will be no crashola since the
# old texture should still be there.
fileQ.join()

# Fetch key presses
mykeys = pi3d.Keyboard()
CAMERA = pi3d.Camera.instance()
CAMERA.was_moved = False #to save a tiny bit of work each loop


while DISPLAY.loop_running():
  crsl.update()
  crsl.draw()

  k = mykeys.read()
  #k = -1
  if k >-1:
    first = False
    d1, d2 = 2, 3
    if k==27: #ESC
      mykeys.close()
      DISPLAY.stop()
      break
    if k==115: #S go back a picture
      crsl.prev()
    #all other keys load next picture
    else:
      crsl.next()

DISPLAY.destroy()

