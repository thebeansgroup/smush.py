#!/usr/local/bin/python2.7
import sys
import os
import os.path
import getopt
import time
from optimiser.formats.png import OptimisePNG
from optimiser.formats.jpg import OptimiseJPG
from optimiser.formats.gif import OptimiseGIF

__author__="al"
__date__ ="$Aug 11, 2010 12:21:32 PM$"

# there should be an option to keep or strip meta data (e.g. exif data) from jpegs

class Smush():
    def __init__(self, **kwargs):
        self.optimisers = {
            'PNG': OptimisePNG(**kwargs),
            'JPG': OptimiseJPG(**kwargs),
            'GIF': OptimiseGIF(**kwargs)
        }

        self.optimisers['JPEG'] = self.optimisers['JPG']

        self.__files_scanned = 0
        self.__start_time = time.time()

    def __smush(self, file):
        """
        Optimises a file
        """
        (basename, extension) = os.path.splitext(file)
        key = extension.lstrip('.').upper()

        if key in self.optimisers:
            print "optimising file ", file

            self.__files_scanned += 1

            self.optimisers[key].set_input(file)
            self.optimisers[key].optimise()


    def process(self, dir, recursive):
        """
        Iterates through the input directory optimising files
        """
        if recursive:
            self.__walk(dir, self.__smush)
        else:
            if os.path.isdir(dir):
                dir = os.path.abspath(dir)
                for file in os.listdir(dir):
                    self.__smush(os.path.join(dir, file))
            elif os.path.isfile(dir):
                self.__smush(dir)


    def __walk(self, dir, callback):
        """ Walks a directory, and executes a callback on each file """
        dir = os.path.abspath(dir)

        print "walking ", dir

        for file in os.listdir(dir):
            nfile = os.path.join(dir, file)
            callback(nfile)

            if os.path.isdir(nfile):
                self.__walk(nfile, callback)

    def stats(self):
        print "\n%d files scanned:" % (self.__files_scanned)

        for key, optimiser in self.optimisers.iteritems():
            # only show the jpg stats once
            if key == 'JPEG':
                continue

            # divide optimiser.files_optimised by 2 for each optimiser since each optimised file
            # gets counted twice
            print "    %d %ss optimised out of %d scanned. Saved %dkb" % (optimiser.files_optimised // 2,
                key, optimiser.files_scanned, optimiser.bytes_saved / 1024)

        print "Total time taken: %.2f seconds" % (time.time() - self.__start_time)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrqs", ["help", "recursive", "quiet", "strip-meta"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) == 0:
        usage()
        sys.exit()

    recursive = False
    quiet = False
    strip_jpg_meta = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-r", "--recursive"):
            recursive = True
        elif opt in ("-q", "--quiet"):
            quiet = True
        elif opt in ("-s", "--strip-meta"):
            strip_jpg_meta = True
        else:
            # unsupported option given
            usage()
            sys.exit(2)

    smush = Smush(strip_jpg_meta=strip_jpg_meta)

    for arg in args:
        try:
            smush.process(arg, recursive)
            print "\nSmushing Finished"
        except KeyboardInterrupt:
            print "\nSmushing aborted"

    if not quiet:
        smush.stats()


def usage():
    print """Losslessly optimises image files - this saves bandwidth when displaying them
on the web.

  Usage: """ + sys.argv[0] + """ [options] FILES...

    FILES can be a space-separated list of files or directories to optimise

  **WARNING**: Existing images files  will be OVERWRITTEN with optimised
               versions.

  Options are any of:
  -h, --help         Display this help message and exit
  -r, --recursive    Recurse through given directories optimising images
  -q, --quiet        Don't display optimisation statistics at the end
  -s, --strip-meta   Strip all meta-data from JPEGs
"""


if __name__ == "__main__":
    main()

#    optimiser = OptimisePNG()
#    optimiser.set_input('/path/to/image.png')
#    optimiser.optimise()