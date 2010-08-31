from optimiser.optimiser import Optimiser

class OptimiseAnimatedGIF(Optimiser):
    """
    Optimises animated gifs with Gifsicle - http://www.lcdf.org/gifsicle/
    """

    def __init__(self, **kwargs):
        super(OptimiseAnimatedGIF, self).__init__(**kwargs)

        # the command to execute this optimiser
        self.commands = ('gifsicle -O2 "__INPUT__" --output "__OUTPUT__"',)

        # format as returned by 'identify'
        self.format = "GIFGIF"
