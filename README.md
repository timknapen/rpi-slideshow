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




# New to Pi3D version (slideshow_pi3D.py)

See the full instructions at https://pi3d.github.io/html/ReadMe.html

    sudo pip3 install pi3d 
  
Set GPU memory to 128 in the raspberry config tool:
    
    sudo raspi-config
    
    
Run the slideshow:

    python slideshow_pi3D.py

Press ESC to exit the slideshow
