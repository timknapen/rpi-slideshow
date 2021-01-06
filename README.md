# rpi-slideshow
a slideshow for Glenn


# Requirements / current setup:

Raspberry Pi OS 32 bit (Kernel version: 5.4)
python 2.7 (should be installed with Raspberry OS)

install PIL and Tkinter:

    sudo apt-get install python-pil python-pil.imagetk

You need to run the script from X-server, so either boot into the GUI or from the CLI type
    
    startx

## Pi3D

See full instructions for pi3D at https://pi3d.github.io/html/ReadMe.html

    sudo pip3 install pi3d 
  
Set GPU memory to 128 in the raspberry config tool:
    
    sudo raspi-config
    

## This script

Download this repository to your pi

    wget https://github.com/timknapen/rpi-slideshow/archive/master.zip

And unzip it

    unzip master.zip

Put all images in the folder called `images` inside the repository
(The `images` folder needs to stay in the same folder as the script `slideshow.py`)

    
Run the slideshow:

    python slideshow.py


Press ESC to exit the slideshow.
