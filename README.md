# Wiki Pages for the en website


This repo contains the `utils` directory that is for all utils script usefull to keep this repo updated and coerent.

* `./pages-and-subpages-from.py` downloads a page and all supages from a mediawiki setup.

  Example: `./pages-and-subpages-from.py --root-page Teacher`

* `./auto-update-dict.py` auto-update the `pages_id.yml` file (you have to edit the file by and to have a good looking keys set)

  Example: `./auto-update-dict.py`

This repo contains the `pages` directory.
This directory has to contain all content page (and subpages) of the en website that are listed in this README.md file.

The format is: `{pagetitle}.mw`

For example the page `About` has to be in the file `About.mw`

The list is:
* Manual
* About
* Hacker
* Student
* Teacher
* Project:Messages

### The pages_id.yml file

For translation needs you have to update also the dictionary that associate every page to an unique id.

For some pages is quite easy (`About` -> `about`), the file to update is the `pages_id.yml`

The format of this file is YAML
