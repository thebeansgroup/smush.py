import os.path
import shutil
from optimiser.optimiser import Optimiser
from animated_gif import OptimiseAnimatedGIF

class OptimiseGIF(Optimiser):
    """
    Optimises gifs. If they aren't animated, it converts them to pngs with ImageMagick before
    optimising them as for pngs.

    Animated gifs get optimised according to the commands in OptimiseAnimatedGIF
    """


    def __init__(self, **kwargs):
        super(OptimiseGIF, self).__init__(**kwargs)

        # the command to execute this optimiser
        self.commands = ('convert "__INPUT__" png:"__OUTPUT__"',
            'pngnq -n 256 -e -opt.smush "__INPUT__"',
            'pngcrush -rem alla -brute -reduce "__INPUT__" "__OUTPUT__"')

        # variable so we can easily determine whether a gif is animated or not
        self.animated_gif_optimiser = OptimiseAnimatedGIF()

        self.converted_to_png = False
        self.is_animated = False

        # format as returned by 'identify'
        self.format = "GIF"


    def set_input(self, input):
        super(OptimiseGIF, self).set_input(input)
        self.converted_to_png = False
        self.is_animated = False


    def _is_animated(self, input):
        """
        Tests an image to see whether it's an animated gif
        """
        return self.animated_gif_optimiser._is_acceptable_image(input)


    def _keep_smallest_file(self, input, output):
        """
        Compares the sizes of two files, and discards the larger one
        """
        input_size = os.path.getsize(input)
        output_size = os.path.getsize(output)
        
        # if the image was optimised (output is smaller than input), overwrite the input file with the output
        # file.
        if (output_size < input_size):
            try:
                shutil.copyfile(output, input)
                self.files_optimised += 1
                self.bytes_saved += (input_size - output_size)
            except IOError:
                print "Unable to copy %s to %s: %s" % (output, input, IOError)
                sys.exit(1)

            if self.iterations == 1 and not self.is_animated:
                self.converted_to_png = True
            
        # delete the output file
        os.unlink(output)


    def _get_command(self):
        """
        Returns the next command to apply
        """

        command = False

        # for the first iteration, return the first command
        if self.iterations == 0:
            # if the GIF is animated, optimise it
            if self._is_animated(self.input):
                command = self.animated_gif_optimiser.commands[0]
                self.is_animated = True
            else:             # otherwise convert it to PNG
                command = self.commands[0]

        # execute the png optimisations if the gif was converted to a png
        elif self.converted_to_png and self.iterations < len(self.commands):
            command = self.commands[self.iterations]

        self.iterations += 1

        return command