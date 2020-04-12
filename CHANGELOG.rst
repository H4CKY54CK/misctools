CHANGELOG
==========

1.8.2 (4-12-2020)
-----------------

**Added**

* This changelog. Lol. I added it after I made the most recent changes, but I'll start keeping better track. Anything below this is a guess.
* Finally corrected the formatting of the README as well as updated it so it contains the most recent info as of now.
* Corrected and improved the output of the timer.
* Corrected a formatting issue when installing a package via `archit` for regular users. Trying to use the package to install itself (in an attempt to upgrade itself) is the only known way to reproduce the current formatting issue.
* Dropped `tqdm` as a required package, since there are currently no progress bars. However, one needs to be built for `archit` at the very least, for when users are trying to create large archive files, as well as unarchiving large archive files.