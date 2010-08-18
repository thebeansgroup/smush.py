import os.path
import sys
from optimiser.optimiser import Optimiser

class OptimiseJPG(Optimiser):
    """
    Optimises jpegs
    """


    def __init__(self):
        # the command to execute this optimiser
        self.commands = ("jpegtran -outfile __OUTPUT__ -optimise -copy none __INPUT__",
            "jpegtran -outfile __OUTPUT__ -optimise -progressive __INPUT__")

        # file extensions this optimiser can work with
        self.extensions = (".jpg", ".jpeg")


    def _get_command(self):
        """
        Returns the next command to apply
        """
        # for the first iteration, return the first command
        if self.iterations == 0:
            self.iterations += 1
            return self.commands[0]
        elif self.iterations == 1:
            self.iterations += 1
                        
            # for the next one, only return the second command if file size > 10kb
            if os.path.getsize(self.input) > 10000:
                print "File is > 10kb - will be converted to progressive"
                return self.commands[1]

        return False