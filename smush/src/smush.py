from optimiser.formats.png import OptimisePNG
from optimiser.formats.jpg import OptimiseJPG

__author__="al"
__date__ ="$Aug 11, 2010 12:21:32 PM$"

if __name__ == "__main__":
#    optimiser = OptimisePNG()
#    optimiser.set_input('/home/al/temp/temp-images/todo/logo.png')
#    optimiser.optimise()

    optimiser = OptimiseJPG()
    optimiser.set_input('/home/al/temp/temp-images/todo/riding.jpg')
    optimiser.optimise()
