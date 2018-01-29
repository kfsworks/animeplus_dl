Animeplus.tv Download Script
========================

About
-----
This Animeplus.tv download Script downloads anime episodes and movies. In case of movies, multiple video files will be downloaded. All that is required is the link(from animeplus.tv) where the videos are hosted and played.

Dependencies
------------

  * Python3
  * BeautifulSoup (``pip install beautifulsoup4``)

Tested on Ubuntu Linux and Windows. It should work on any Linux, OS X, or Windows machine as long as the dependencies are installed.

Usage
-----

Mandatory argument:
  -l, --link  <link that hosts video links>

 Optional Arguments:
  -d, --directory <download directory>

To download an episode:

    ~ $ python animeplus_dl.py -l LINK -d DIRECTORY

Examples
--------
Download Kimi no na wa (2016) movie

    ~ $ python animeplus_dl.py -l http://www.animeplus.tv/kimi-no-na-wa.-2016-online -d ~/Videos

Download The Oregairu Zoku Ova Episode: 

    ~ $ python animeplus_dl.py -l http://www.animeplus.tv/oregairu-2-ova-online -d ~/Videos

Notes
-----
Please do not overuse and abuse this and destroy Animeplus.tv in the process. Please donate some money to animeplus.tv. I really would not like it if animeplus.tv were damaged due to greedy downloading. Please use this sparingly. 
