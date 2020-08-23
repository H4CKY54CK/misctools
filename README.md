![Python package](https://github.com/H4CKY54CK/misctools/workflows/Python%20package/badge.svg)

# misctools

Most Indefinitely Something Cool... tools.

# Installation

This package is not currently available through PyPi. However, you can still install this package with your preference of one of the two commands below.

`pip install https://github.com/H4CKY54CK/misctools/archive/master.zip`  
`pip install https://github.com/H4CKY54CK/misctools/archive/master.tar.gz`

Alternatively, you can download the repo as a `.zip` file, stand in the directory containing the `.zip` file, and issue the below command.

`pip install misctools-master.zip`

## What do I get?

This package provides several commands via the command line (listed below).

- spriteit  
- sliceit  
- archit  
- unarchit  
- wgetit  
- gifit

You also get a timing decorator, to time your functions, with the option to repeat the function multiple times, to acquire an average, best, and worst elapsed time.

## @timeit

The timing decorator can be used in several ways, illustrated below.

    # from misctools.timer import timeit
    # I forgot I changed this
    from misctools import timeit
    import time

    # Time how long a function takes.
    @timeit
    def main1():
        time.sleep(2)

    # Same thing, but in case you're used to using parentheses
    @timeit()
    def main2():
        time.sleep(.5)

    # Get an average elapsed time by running your function 5 times.
    @timeit(repeat=5)
    def main3():
        pass

    if __name__ == '__main__':
        for i in [main1, main2, main3]:
            i()


    # main1 elapsed: 2.00 s
    # main2 elapsed: 500.38 ms
    # main3 average elapsed: 616.67 ns | best (of 5): 300.00 ns | worst (of 5): 1.90 µs

The timing decorator also automatically converts the time returned into a sensible unit, for optimal viewing pleasure.

Just be careful that you don't repeat 50 times, and your code takes 50 seconds each run. That would take forever. Be smart.

Note: I'm considering moving this into a file that would house various other utility functions, in an attempt to stay organized.

## spriteit

I needed a specific tool for a subreddit I mod, so it's highly tailored to my specific needs. Here's how it works.

Call it from the command line like so:

`spriteit <source> [output] [options]`

For example, in a directory that contains the target folder, which contains a number of subfolders, each containing a number of same-size images, you could use it like so (let's assume the target/source directory is called "images"):

`spriteit images` To get a straight-up concatenation of the images per folder.

`spriteit images spritesheets` To send the output to a folder "spritesheets". (default is "sprites")  


`spriteit images -xy 40 40 --output=spritesheets` Two things happening here. `-xy` expects two integers to follow it. This is the desired dimensions of the INDIVIDUAL images inside the spritesheet. For example, a 10x10 sheet would end up being 400x400 px. Also, source and output are also flaggable, in that you can `--source=<input_dir>` and `--output=<output_dir>` instead of providing them positionally.  

`spriteit images -xy 40 40 -u -S=hacky` This would use the default output directory, "sprites", giving you spritesheets with the individual images's dimensions of 40x40 px, `-u` tells it to also get your stylesheet contents from your subreddit and prepend it to the outputted stylesheet, and `-S=hacky` tells it to use a already-defined site from a "praw.ini" file (which has a defined `subreddit` attribute) that can be accessed from where you are, and upload all outputted images to the subreddit's stylesheet, followed by updating the stylesheet itself. There is a small catch, however. You must define an attribute in your "praw.ini" file called `key`, and also put that at the end of your stylesheet, and all the flairs would come after that. It fetches the stylesheet, looks for the key (unique to the rest of the stylesheet), truncates it right then and there, replaces the key, followed by appending all the flairs (and the classes, since I needed multiple spritesheets). `--minify` can also be passed, if you wish to try and reduce your stylesheet's size.

There are also a few other commands. They're self explanatory, I think.

`spriteit images -xy 40 40 [-b | -nc | -ni | -m]`

`-b / --bot-files` I plan on changing this, but it esentially provides another file I need for the flairbot I use. Outputs to a CSV.  
`nc / --no-css` Skip the stylesheet, just give me the spritesheets!  
`-ni / --no-img` Skip the spritesheets, just give me the stylesheet!  
`-m / --minify` Minify the part of the stylesheet that we worked on, but leave the rest? Maybe I'll change it

## sliceit

This is a new addition to the family. It takes a spritesheet and slices it up into the images that make it up. Must be same size images that make up the spritesheet. It's not intelligent, so you'll need to be able to provide the height/width of the smaller images (one height, one width, since they should all be the same size), or the amount of rows/columns in the spritesheet.

`sliceit somespritesheet.png 60 60` Slices the images up into 60x60 chunks.  
`sliceit somespritesheet.png -x 60 -y 60` Same deal. `--width`/`--height` could be used in place of `-x`/`-y`.  
`sliceit somespritesheet.png -r 13 -c 1` Slices up the image based on 13 rows and 1 column(s). `--rows`/`--columns` could be used in place of `-r`/`-c`.  

## archit

`archit source` Guesses your native file format based on the output of sys. `.zip` for Windows, `.tar.gz` for linux.  
`archit source -f <formats>` Available formats are zip/tar/gztar/bztar/xztar. Multiple formats allowed, separated by a single space each.  
`archit source -i` Takes directory `source`, creates an archive file of it in the default and optionally specified formats, then attempts to install it via pip. Obviously this is only useful for, and will only work with, directories properly structured as a python package. Whether it succeeds or fails, it's final task is to clean up after itself (i.e. deleting the archived files that it created).

## unarchit

`unzipit source [options]` - Source must end in an acceptable extension, such as `.zip` or `.tar.gz`  

## wgetit

A simple, yet effective, Python/Windows implementation of the popular Linux command, `wget`, called `wgetit` (get it? _laughs nervously... and then maniacally..._).

`wgetit url` Works the same as wget. Without fancy options, though.

## gifit

`gifit foldername somefile.gif` Takes the contents of the directory `foldername`, and stitches them together (sorted by filename, so `file00.png`, `file01.png`, `file02.png`, etc), saving the final result as a GIF, `somefile.gif`.

## Other

Although, I really wish I'd chosen a different version number to start the project with. It originally started from v0.1, and really has incremented by 0.1 as I built it, but I've reuploaded the package several times, due to my still learning GitHub at the time. The third decimal place (minor minor version indicator?) is very recent, and will be the continued format onward.