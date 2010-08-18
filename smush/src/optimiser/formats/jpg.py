from optimiser.optimiser import Optimiser

class OptimiseJPG(Optimiser):
    """
    Optimises jpegs
    """


    def __init__(self):
        # the command to execute this optimiser
        self.commands = ("jpegtran -outfile __OUTPUT__ -optimise __INPUT__",)

        # file extensions this optimiser can work with
        self.extensions = (".jpg", ".jpeg")


        