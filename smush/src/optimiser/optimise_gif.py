from optimiser import Optimiser
from optimiser.optimise_animated_gif import OptimiseAnimatedGif

class OptimiseGif(Optimiser):
    """
    Optimises gifs. If they aren't animated, it converts them to pngs with ImageMagick
    """


    def __init__(self):
        # the command to execute this optimiser
        self.commands = ("convert __INPUT__ __OUTPUT__")

        # file extensions this optimiser can work with
        self.extensions = (".gif")

        # variable so we can easily determine whether a gif is animated or not
        self.animated_gif_optimiser = OptimiseAnimatedGif()


    def is_animated(self, input):
        """
        Tests an image to see whether it's an animated gif
        """

        return self.animated_gif_optimiser.is_acceptable_image(input)
        