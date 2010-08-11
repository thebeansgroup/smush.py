from optimiser.optimise_png import OptimisePng

__author__="al"
__date__ ="$Aug 11, 2010 12:21:32 PM$"

if __name__ == "__main__":
    optimiser = OptimisePng()
    optimiser.set_input('/home/al/temp/temp-images/todo/logo.png')
    optimiser.optimise()
