# smush.py - Optimise images for the web

[Smush.it](http://www.smushit.com/) is a service from Yahoo that applies lossless optimisations to images 
for display on the web. Unfortunately they don't provide an API, and 
sometimes it's convenient to have a local command-line script.

smush.py uses the same tools as Smushit (read more at:
http://oreilly.com/server-administration/excerpts/9780596522315/optimizing-images.html), but can be run locally.

The following lossless optimisations are performed:

* GIFs - If they're animated GIFs, they are optimised with Gifsicle.
       If they aren't animated, they're converted to PNGs with ImageMagick, 
       then optimised as PNGs as below.
* PNGs - Quantised with pngnq, then crushed with pngcrush.
* JPGs - Optionally remove ALL metadata (it may not be legal to remove copyright 
       notices, so only use this on images you own the copyright to or that 
       don't have copyright notices).
       If they're larger than 10kb, they're converted to progressive JPGs.
       Compression is optimised with jpegtran.

*Note: If a GIF is converted to a PNG, it keeps the old `.gif` file extension in 
case the file name is in a database.*

## Installation

### Install all of the following required software:

  * Python 2.x >= 2.5
  * Gifsicle - http://www.lcdf.org/gifsicle/
  * ImageMagick - http://www.imagemagick.org
  * pngcrush - http://pmt.sourceforge.net/pngcrush/
  * jpegtran from libjpeg

### Compile, patch, and install pngnq (read on):

  * pngnq - http://pngnq.sourceforge.net/ (compilation requires libpng-dev)

In the `contrib` directory is a file `pngnq-x.x.diff`. This must be applied against
v1.0 and v1.1 of `pngnq.c` - the patch has been submitted back to the author, so it's
possible that later versions will include the patched functionality (check for
the existence of a `-o` option that allows an output file name to be specified).
In that case, then it's not necessary to apply the patch.

Apply the diff using `patch`, e.g.:

    wget http://sourceforge.net/projects/pngnq/files/pngnq/1.1/pngnq-1.1.tar.gz
    tar -xzvf pngnq-1.1.tar.gz
    cd pngnq-1.1/src
    patch < ~/smush.py/contrib/pngnq-1.1.diff

Then configure and make as usual.

## Usage

This script is intended to be run over a collection of existing images - GIFs 
(perhaps animated), PNGs and JPEGs. It will perform lossless optimisations and 
will OVERWRITE THE ORIGINAL file. It is intended to be able to be used to 
optimise images that have a reference stored in a database, hence the reason 
for not modifying input file names at all.

It can be run as follows:

    python smush.py /path/to/file/or/directory(ies)

where /path/to/file/or/directory(ies) is a file or directory path, or list of 
space-separated paths to files or directories that will be optimised.

Or type:

    python smush.py --help

for usage information.

It is safe to run this script multiple times on the same files since all 
operations are lossless. In fact, PNG images may be optimised further by 
repeatedly smushing them.

Unless the `-q` option is given, statistics will be displayed when
smushing has finished - these stats are approximate. GIFGIF refers to
animated GIFs.

*Note: This software has only been tested on Centos 5 Linux.*
