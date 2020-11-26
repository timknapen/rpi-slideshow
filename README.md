# rpi-slideshow
a slideshow for Glenn


# Requirements / current setup:

Raspberry Pi OS 32 bit (Kernel version: 5.4)
python 2.7 (should be installed with Raspberry OS)

install PIL and Tkinter:

    sudo apt-get install python-pil python-pil.imagetk

You need to run the script from X-server, so either boot into the GUI or from the CLI type
    
    startx

Put all images in a folder called "images"

Run the slideshow:

    python slideshow.py

Press ESC to exit the slideshow