CHANGELOG
==========

1.9.0 (4-21-2020)
-----------------

**Added**

* New command line command, `substats`. Examine the last 1k comments made to a subreddit, group them according to the time of day they were made, and report back a total count per hour of the day. Good for getting a rough estimate of when the active time of a subreddit is.


**Changes**

* Corrected the formatting for `archit`.


1.8.5 ???
-----------------

**???**

* I forgot to log the changes.

1.8.4 (4-14-2020)
-----------------

**Patches**

* Implemented a workaround, so that we can have the latest Pillow again, as well as dropped the version requirement for Pillow.

1.8.3post1 (4-13-2020)
----------------------

**Corrections**

* Clarified/changed some wording in the README.

1.8.3 (4-13-2020)
-----------------

**Changes**

* Changed required version of Pillow to 7.0.0 due to 7.1.1 having a bug the prevented `gifit` from working.

1.8.2 (4-12-2020)
-----------------

**New**

* This changelog. Lol. I added it after I made the most recent changes, but I'll start keeping better track. Anything below this is a guess.
* Finally corrected the formatting of the README as well as updated it so it contains the most recent info as of now.
* Corrected and improved the output of the timer.
* Corrected a formatting issue when installing a package via `archit` for regular users. Trying to use the package to install itself (in an attempt to upgrade itself) is the only known way to reproduce the current formatting issue.
* Dropped `tqdm` as a required package, since there are currently no progress bars. However, one needs to be built for `archit` at the very least, for when users are trying to create large archive files, as well as unarchiving large archive files.