#!/usr/bin/env python3
import requests
import urllib.parse as urlparse
import os
import os.path
import sys
import argparse

# this is the default output directory, from the utils/ path is ../pages/
default_output_dir = "{}/".format(os.path.abspath("{}/../pages/".format(os.path.dirname(os.path.realpath(__file__)))))

parser = argparse.ArgumentParser(description='This script helps to download a page and all supages from a mediawiki instance')

parser.add_argument('--api-url', action="store", default="http://en.wikitolearn.org/api.php")
parser.add_argument('--root-page', action="store",required=True)
parser.add_argument('--output-dir', action="store",default=default_output_dir)

argument_parsed = parser.parse_args()
api_url = argument_parsed.api_url
output_dir = argument_parsed.output_dir
root_page = argument_parsed.root_page

def list_page_and_subpages(api_url, root_page, apfrom=None):
    pages_titles = []
    args = {
        "action": "query",
        "list": "allpages",
        "apprefix": root_page,
        "aplimit": 15,
        "format": "json"
    }
    if apfrom != None:
        args['apfrom'] = apfrom

    response = requests.get(api_url + "?" + urlparse.urlencode(args))
    response_json = response.json()
    if 'error' in response_json:
        raise ValueError(response_json['error'])
    for pag in response_json['query']['allpages']:
        if pag['title'] == root_page or pag['title'].startswith(root_page+"/"):
            pages_titles.append(pag['title'])
    if 'continue' in response_json:
        if 'apcontinue' in response_json['continue']:
            for pag_title in list_page_and_subpages(api_url, root_page, response_json['continue']['apcontinue']):
                pages_titles.append(pag_title)
    return pages_titles

def download_wikipage(api_url, page_title, out_basedir):
    args = {
        "action": "query",
        "titles": page_title,
        "prop": "revisions",
        "format": "json",
        "rvprop": "content"
    }

    response = requests.get(api_url + "?" + urlparse.urlencode(args))
    response_json = response.json()
    if 'error' in response_json:
        raise ValueError(response_json['error'])
    pages = response_json['query']['pages']
    for page_id in pages:
        page_split = page_title.split('/')
        output_filename = out_basedir
        if len(page_split) > 1:
            for dir_segment_index in range(0, len(page_split) - 1):
                output_filename = output_filename + \
                    page_split[dir_segment_index] + "/"
                if not os.path.exists(output_filename):
                    os.makedirs(output_filename)
        output_filename = output_filename + \
            page_split[len(page_split) - 1] + ".mw"
        page_content = pages[page_id]['revisions'][0]['*']

        text_file = open(output_filename, "wb")
        text_file.write(page_content.encode('utf8'))
        text_file.close()

for page_title in list_page_and_subpages(api_url,root_page):
    print("Download for: {}".format(page_title))
    download_wikipage(api_url,page_title,output_dir)
