from optimiser.formats.png import OptimisePNG
from optimiser.formats.jpg import OptimiseJPG
from optimiser.formats.gif import OptimiseGIF

__author__="al"
__date__ ="$Aug 11, 2010 12:21:32 PM$"

# there should be an option to keep or strip meta data (e.g. exif data) from jpegs

if __name__ == "__main__":
#    optimiser = OptimisePNG()
#    optimiser.set_input('/home/al/temp/temp-images/todo/logo.png')
#    optimiser.optimise()

#    optimiser = OptimiseJPG()
#    optimiser.set_input('/home/al/temp/temp-images/todo/riding.jpg')
#    optimiser.optimise()

    optimiser = OptimiseGIF()
    optimiser.set_input('/home/al/temp/temp-images/todo/the-dog-wins-1.gif')
    optimiser.optimise()

#    optimiser = OptimiseGIF()
#    optimiser.set_input('/home/al/temp/temp-images/todo/fish.gif')
#    optimiser.optimise()