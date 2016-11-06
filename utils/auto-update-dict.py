#!/usr/bin/env python3
import yaml
import os
import argparse
from re import sub

# this is the default output directory, from the utils/ path is ../pages/
default_output_dir = "{}/".format(os.path.abspath("{}/../pages/".format(os.path.dirname(os.path.realpath(__file__)))))
default_pages_id_file = os.path.abspath("{}/../pages_id.yml".format(os.path.dirname(os.path.realpath(__file__))))

parser = argparse.ArgumentParser(description='This script helps to fix the pages_id.yml file')

parser.add_argument('--output-dir', action="store",default=default_output_dir)
parser.add_argument('--pages-id-file', action="store",default=default_pages_id_file)

argument_parsed = parser.parse_args()
output_dir = argument_parsed.output_dir
pages_id_file = argument_parsed.pages_id_file

mw_pages_files = []
for root, directories, filenames in os.walk(output_dir):
    for filename in filenames:
        mw_pages_files.append(os.path.join(root, filename))

placeholder_dict = {}

if os.path.isfile(pages_id_file):
    with open(pages_id_file) as data_file:
        reverse_placeholder_dict = yaml.load(data_file)
        for k in reverse_placeholder_dict:
            placeholder_dict[reverse_placeholder_dict[k]] = k
        data_file.close()

def get_placeholder(link):
    if link not in placeholder_dict:
        placeholder = None
        retry_counter = 0
        while placeholder == None or placeholder in placeholder_dict.values():
            placeholder = "FILE_{}".format(
                len(placeholder_dict) + retry_counter)
            retry_counter = retry_counter + 1

        placeholder_dict[link] = placeholder

    return placeholder_dict[link]

def evaluate(match):
    link_to = str(match.group(1))
    link_label = None
    placeholder = None

    if match.group(3) != None:
        link_label = str(match.group(3))

    placeholder = get_placeholder(link_to)

    return_val = "[[" + placeholder
    if link_label != None:
        return_val = return_val + "|" + link_label
    return_val = return_val + "]]"
    return return_val

for mw_page_file in mw_pages_files:
    get_placeholder(mw_page_file[len(output_dir):-3])

for mw_page_file in mw_pages_files:
    with open(mw_page_file, 'r') as content_file:
        content = content_file.read()
        # this regex uses
        # https://www.mediawiki.org/wiki/Manual:$wgLegalTitleChars
        sub(r'\[{2}(.[^\[\]\{\}\|\#\<\>\%\+\?]+)(\|(.[^\[\]\{\}\|\#\<\>\%\+\?]+)){0,1}\]{2}', evaluate, content)

with open(pages_id_file, 'w') as outfile:
    reverse_placeholder_dict = {}
    for k in placeholder_dict:
        reverse_placeholder_dict[placeholder_dict[k]] = k
    yaml.dump(reverse_placeholder_dict, outfile, default_flow_style=False)
    outfile.close()
