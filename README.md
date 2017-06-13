Animeplus.tv Download Script
========================

About
-----
Animeplus.tv Download Script downloads anime episodes and movies. In case of movies, multiple video files will be downloaded. All that is required is the link where the videos are hosted and played.

Dependencies
------------

  * Python 2.7 or better
  * BeautifulSoup (``pip install beautifulsoup4``)

Tested on Ubuntu Linux and Windows. It should work on any Linux, OS X, or Windows machine as long as the dependencies are installed.

Usage
-----

Mandatory argument:
  -l  <link that hosts video links>

 Optional Arguments:
   -d <download directory>

To download an entire series:

    ~ $ python mfdl.py -m MANGA_NAME

To download a specific chapter:

    ~ $ python mfdl.py -l EPISODE_LINK -d DOWNLOAD_DIRECTORY

Examples
--------
Download Kimi no na wa (2016) movie

    ~ $ python animeplus-dl.py -l http://www.animeplus.tv/kimi-no-na-wa.-2016-online -d ~/Videos

Download The Oregairu Zoku Ova Episode: 

    ~ $ python animeplus-dl.py -l http://www.animeplus.tv/oregairu-2-ova-online -d ~/Videos

Notes
-----
Please do not overuse and abuse this and destroy Animeplus.tv. Please donate some cash to animeplus.tv I really would not like people to destroy Animeplus because of greedy downloading. Use this wisely and don't be evil.
