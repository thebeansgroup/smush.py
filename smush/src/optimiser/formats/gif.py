from optimiser.optimiser import Optimiser
from animated_gif import OptimiseAnimatedGIF

class OptimiseGIF(Optimiser):
    """
    Optimises gifs. If they aren't animated, it converts them to pngs with ImageMagick
    """


    def __init__(self):
        # the command to execute this optimiser
        self.commands = ("convert __INPUT__ __OUTPUT__",)

        # file extensions this optimiser can work with
        self.extensions = (".gif")

        # variable so we can easily determine whether a gif is animated or not
        self.animated_gif_optimiser = OptimiseAnimatedGIF()


    def _is_animated(self, input):
        """
        Tests an image to see whether it's an animated gif
        """

        return self.animated_gif_optimiser.is_acceptable_image(input)


    def _get_command(self):
        """
        Returns the next command to apply
        """
        # for the first iteration, return the first command
        if self.iterations == 0:
            self.iterations += 1

            # if the GIF is animated, optimise it
            if self._is_animated(self.input):
                return self.animated_gif_optimiser.commands[0]
            else:             # otherwise convert it to PNG
                return self.commands[0]

        return False