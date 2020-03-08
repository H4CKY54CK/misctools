# misctools
Most Indefinitely Something Cool... tools.

# Installation

`pip install https://github.com/H4CKY54CK/misctools/archive/master.zip`  
`pip install https://github.com/H4CKY54CK/misctools/archive/master.tar.gz`

 This package provides several commands via the command line.
 
   - spriteit  
   - zipit/tarit  
   - unzipit/untarit  
   - wgetit  

## spriteit

  I needed a specific tool for a subreddit I mod, so it's highly tailored to my specific needs. Here's how it works.
  
  Call it from the command line like so:
  
  `spriteit <source> [output] [options]`
  
  For example, in a directory that contains the target folder, which contains a number of subfolders, each containing a number of same-size images, you could use it like so (let's assume the target/source directory is called "images"):

  `spriteit images` To get a straight-up concatenation of the images per folder.  
  `spriteit images spritesheets` To send the output to a folder "spritesheets". (default is "sprites")  
  `spriteit images -xy 40 40 --output=spritesheets` Two things happening here. `-xy` expects two integers to follow it. This is the desired dimensions of the INDIVIDUAL images inside the spritesheet. For example, a 10x10 sheet would end up being 400x400 px. Also, source and output are also flaggable, in that you can `--source=<input_dir>` and `--output=<output_dir>` instead of providing them positionally.  
  `spriteit images -xy 40 40 -u -S=hacky` This would use the default output directory, "sprites", giving you spritesheets with the individual images's dimensions of 40x40 px, `-u` tells it to also get your stylesheet contents from your subreddit and prepend it to the outputted stylesheet, and `-S=hacky` tells it to use a already-defined site from a "praw.ini" file (which has a defined `subreddit` attribute) that can be accessed from where you are, and upload all outputted images to the subreddit's stylesheet, followed by updating the stylesheet itself. There is a small catch, however. You must define an attribute in your "praw.ini" file called `key`, and also put that at the end of your stylesheet, and all the flairs would come after that. It fetches the stylesheet, looks for the key (unique to the rest of the stylesheet), truncates it right then and there, replaces the key, followed by appending all the flairs (and the classes, since I needed multiple spritesheets). `--minify` can also be passed, if you wish to try and reduce your stylesheet's size.

## the rest (to be continued)
