#!/usr/bin/env python3
# -- coding: utf-8 --

from urllib.request import Request, urlopen
from urllib.error import HTTPError
import sys
import os
import logging
import re
import json
import itertools

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

request_headers = {
    # request headers while establishing connection with the url
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) "
    "Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
    "*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive"
}


def download(url, out_path):
    # Download a file
    # Requires url and output path
    u = urlopen(url)
    f = open(out_path, 'wb')

    meta = u.info()
    file_size = int(meta['Content-Length'])
    print("Downloading: %s Bytes: %s" % (out_path, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (
            file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print(status, end="\r")

    f.close()


def gethtml(url):
    # Get html source of url
    return urlopen(
        Request(url, headers=request_headers)
    ).read().decode('utf-8', 'ignore')


def get_video_links(link, loc):
    # Putting all functions together
    if 'animeplus.tv' not in link:
        sys.exit('Link does not belong to animeplus.tv')
    if not link.startswith('http://'):
        link = 'http://{0}'.format(link)

    if not os.path.exists(loc):
        os.mkdir(loc)

    logger.info('Searching: {0}'.format(link))

    def _search_playlist(link, playlist=1):
        # This stops the script if any error occurs
        # while establishing the connection
        try:
            htm = gethtml('{0}/{1}'.format(link, playlist))
        except (KeyboardInterrupt, SystemExit):
            logger.debug('Cancelled by user!')
            sys.exit()
        except HTTPError as err:
            if err.code == 404:
                logger.debug('Link not found!')
                sys.exit()
            else:
                logger.debug('Check connection!')
                sys.exit()
        # Acquires a list of downloadable video links
        return {
            'video_links': re.findall(r'iframe\s*src\s*=\s*"(.+?)"', htm),
            'playlist_length': len(re.findall(r'Playlist \d', htm))
        }
    playlist_length = _search_playlist(link)['playlist_length']
    video_links = _search_playlist(link)['video_links']

    for playlist in range(1, playlist_length+1):
        errs = None
        if playlist > 1:
            video_links = _search_playlist(link, playlist)['video_links']
        # Iterates through all video links found in the playlist
        for video_link in video_links:

            try:
                # acquires javascript object from the html link
                # which contains links
                video_sub_links_dict = json.loads(
                    re.search(
                        r'var\svideo_links\s*\=\s*({.*})\;',
                        gethtml(video_link)
                    ).group(1)
                )
                # iterates through sublinks
                # by going through the javascript object
                vid_sub_links = list(itertools.chain.from_iterable(
                    video_sub_links_dict['normal'].values()))

                for vid_sub_link in vid_sub_links:
                    try:
                        dwn_link = vid_sub_link['link']
                        file_name = vid_sub_link['filename']
                        logger.info(
                            'Found a downloadable link: \n{0}'.format(dwn_link)
                        )
                        download(
                            url=dwn_link,
                            out_path=os.path.join(loc, file_name)
                        )
                        logger.info('Downloaded {0} to {1}'.format(
                            file_name,
                            loc
                        ))
                        # try any one link and return to outer loop
                    except (KeyboardInterrupt, SystemExit):
                        logger.debug('Cancelled by user!')
                        sys.exit()
                    except Exception as e:
                        logger.debug(e)
                        logger.info('Moving on to the next sublink')
                        # if failure occurs move onto the next sublink
                        continue
                    else:
                        break

            # If any errors exist,
            # store the errors in a variable
            # then move on to the next link in the playlist
            except Exception as e:
                logger.debug('Problem downloading from link!')
                logger.info('Moving on to the next link in the playlist!')
                if errs is None:
                    errs = e
                continue

            # If the link points to an episode,
            # then stops the script when the download is a success
            # for any one file
            else:
                errs = None
                if any(s in link for s in [
                    'episode',
                    'special',
                    'ova',
                    'OVA']
                ):
                    break
                else:
                    continue

        # If any exceptions
        # while acquiring links from a playlist
        # move on to the next playlist
        if errs is not None:
            logger.debug('All downloadable links failed in playlist!')
            logger.info('Moving on to the next playlist!')
            continue
        else:
            break


def _Main():
    # Main function
    import argparse
    parser = argparse.ArgumentParser(
        description='Download anime from animeplus.tv')
    parser.add_argument('link', type=str,
                        help='Enter link which is hosting the video')
    parser.add_argument('--directory', '-d', type=str,
                        default='.', help='Give folder location')
    args = parser.parse_args()
    if args.link is None:
        parser.error('Arguments missing')
    get_video_links(link=args.link, loc=args.directory)


if __name__ == '__main__':
    _Main()
