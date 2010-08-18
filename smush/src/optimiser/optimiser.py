import os.path
import os
import shlex
import subprocess
import sys
import shutil

class Optimiser(object):
    """
    Super-class for optimisers
    """

    input_placeholder = "__INPUT__"
    output_placeholder = "__OUTPUT__"

    # string to place between the basename and extension of output images
    output_suffix = "-opt"


    def __init__(self):
        # the number of times the _get_command iterator has been run
        self.iterations = 0

    
    def set_input(self, input):
        self.iterations = 0
        self.input = input


    def _get_command(self):
        """
        Returns the next command to apply
        """
        command = False
        
        if self.iterations < len(self.commands):
            command = self.commands[self.iterations]
            self.iterations += 1

        return command


    def __get_output_file_name(self):
        """
        Returns the input file name with Optimiser.output_suffix inserted before the extension
        """
        (basename, extension) = os.path.splitext(self.input)
        return basename + Optimiser.output_suffix + extension


    def __replace_placeholders(self, command, input, output):
        """
        Replaces the input and output placeholders in a string with actual parameter values
        """
        return command.replace(Optimiser.input_placeholder, input).replace(Optimiser.output_placeholder, output)


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
            except IOError:
                print "Unable to copy %s to %s: %s" % (output, input, IOError)
                sys.exit(1)
        
        # delete the output file
        os.unlink(output)
        

    def is_acceptable_image(self, input):
        """
        Returns whether the input image can be used by a particular optimiser.

        All optimisers are expected to define a tuple called 'extensions' containing valid file
        extensions that can be used, converted to lowercase.
        """
        (basename, extension) = os.path.splitext(input.lower())

        return extension in self.extensions


    def optimise(self):
        """
        Calls the 'optimise_image' method on the object. Tests the 'optimised' file size. If the
        generated file is larger than the original file, discard it, otherwise discard the input file.
        """
        # make sure the input image is acceptable for this optimiser
        if not self.is_acceptable_image(self.input):
            print self.input, "is not a valid image for this optimiser"
            return

        while True:
            command = self._get_command()

            if not command:
                break

            output_file_name = self.__get_output_file_name()
            command = self.__replace_placeholders(command, self.input, output_file_name)

            print "Executing " + command
            
            args = shlex.split(command)
            
            try:
                subprocess.call(args)
            except OSError:
                print "Error executing command %s. Error was %s" % (command, OSError)
                sys.exit(1)

            # compare file sizes
            self._keep_smallest_file(self.input, output_file_name)

