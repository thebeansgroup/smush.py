import os.path
import os
import shlex
import subprocess

class Optimiser:
    """
    Super-class for optimisers
    """

    input_placeholder = "__INPUT__"
    output_placeholder = "__OUTPUT__"

    def set_input(self, input):
        self.input = input

    def get_command(self):
        """
        Iterator that returns the next command to apply
        """
        for command in self.commands:
            yield command

    def __replace_placeholders(self, command, input, output):
        """
        Replaces the input and output placeholders in a string with actual parameter values
        """
        return command.replace(Optimiser.input_placeholder, input).replace(Optimiser.output_placeholder, output)

    def __keep_smallest_file(self, input, output):
        """
        Compares the sizes of two files, and discards the larger one
        """
        input_size = os.path.getsize(input)
        output_size = os.path.getsize(output)

        os.unlink(input if (input_size > output_size) else output)

    def is_acceptable_image(self, input):
        """
        Returns whether the input image can be used by a particular optimiser.

        All optimisers are expected to define a tuple called 'extensions' containing valid file
        extensions that can be used, converted to lowercase.
        """
        (basename, extension) = os.path.splitext(input.lower())

        return extensions.contains(extension)


    def optimise(self, input, output):
        """
        Calls the 'optimise_image' method on the object. Tests the 'optimised' file size. If the
        generated file is larger than the original file, discard it, otherwise discard the input file.
        """

        # make sure the input image is acceptable for this optimiser
        if not self.is_acceptable_image(input):
            return

        for command in self.get_command():
            command = self.__replace_placeholders(command, input, output)

            args = shlex.split(command)
            try:
                output = subprocess.Popen(args)
            except OSError:
                print "Error executing command %s. Error was %s" % (command, OSError)
                sys.exit(1)

            # compare file sizes
            self.__keep_smallest_file(input, output)