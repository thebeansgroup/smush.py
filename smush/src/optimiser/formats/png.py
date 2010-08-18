from optimiser.optimiser import Optimiser

class OptimisePNG(Optimiser):
    """
    Optimises pngs. Uses pngnq (http://pngnq.sourceforge.net/) to quantise them, then uses pngcrush
    (http://pmt.sourceforge.net/pngcrush/) to crush them.
    """


    def __init__(self):
        # the command to execute this optimiser
        self.commands = ("pngnq -n 256 -e -opt.png __INPUT__",
            "pngcrush -rem alla -brute -reduce __INPUT__ __OUTPUT__")

        # file extensions this optimiser can work with
        self.extensions = (".png")
        