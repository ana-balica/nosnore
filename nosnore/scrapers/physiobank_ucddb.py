import os
import sys
import urllib
from urlparse import urljoin
from lxml import etree


def download(url):
    """ Download contents of a page

    :param url: target URL where from to download contents
    :return: string page contents
    """
    browser = urllib.urlopen(url)
    response = browser.getcode()
    if response == 200:
        contents = browser.read()
    else:
        print 'Bad header response. Exiting...'
        sys.exit()
    return contents


def scrape_ucddb():
    """ Scrape recorded data from UCD database and save all the files to the 
    filesystem
    """
    BASE_URL = "http://physionet.org/physiobank/database/ucddb/"
    contents = download(BASE_URL)
    tree = etree.HTML(contents)
    urls = tree.xpath("//pre/a/@href")
    urls = filter_urls(urls)
    absolute_urls = [urljoin(BASE_URL, url) for url in urls]

    for url in absolute_urls:
        save_contents(url)


def filter_urls(urls):
    """ Filter the extracted URLs by choosing only *.txt and *.rec files

    :param urls: a list of url strings
    :return: a list of filtered url strings
    """
    filtered_urls = []
    for url in urls:
        if url.endswith("txt") or url.endswith("rec"):
            filtered_urls.extend([url])
    return filtered_urls


def save_contents(url):
    """ Save the contents of a page to a file

    :param url: string URL 
    """
    contents = download(url)
    SAVE_PATH = "../samples/ucddb/"
    try:
        filename = url.rsplit('/', 1)[1]
    except IndexError:
        print "Splitting of URLS went wrong. No contents saved. Returning..."
        return

    with open(os.path.join(SAVE_PATH, filename), "wb") as f:
        f.write(contents)
    print "File '{0}' saved".format(filename)


if __name__ == '__main__':
    scrape_ucddb()
