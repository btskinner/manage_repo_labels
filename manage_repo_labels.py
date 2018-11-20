#!/usr/bin/env python3
################################################################################
#
# <PROJ> Create repo labels
# <FILE> make_repo_labels.py
# <AUTH> Benjamin Skinner (btskinner@virginia.edu)
# <INIT> 19 November 2018
#
################################################################################

# modules
import argparse
import json
import requests

# --------------------------------------
# FUNCTIONS
# --------------------------------------

# command line parser
def set_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id',
                        help='GitHub ID',
                        metavar="ID",
                        required=True)
    parser.add_argument('-t', '--token',
                        help='GitHub authorization token in file',
                        metavar='TOKEN',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('-r', '--repo',
                        help='Repository name',
                        metavar='REPO',
                        required=True)
    parser.add_argument('-o', '--org',
                        help='Organization name',
                        metavar='ORG')
    parser.add_argument('-l', '--labels',
                        help='Labels in JSON file',
                        metavar='LABELS',
                        type=argparse.FileType('r'))
    parser.add_argument('-c', '--check_existing',
                        help='Flag to check existing labels',
                        action='store_true')
    parser.add_argument('-d', '--drop_existing',
                        help='Flag to drop existing labels',
                        action='store_true')
    return parser.parse_args()

# pretty print
def pretty_print(dict_list, header, key_list):
    long_name = max(key_list, key=len)
    print('-'*len(header))
    print(header.upper())
    print('-'*len(header), end='\n\n')
    for item in dict_list:
        for key in key_list:
            space = len(long_name) - len(key) + 1
            print('  {}:{} {}'.format(key.upper(), ' '*space, item[key]))
        print('')

# read json labels
def read_json(args):
    return json.loads(args.labels.read())

# set url
def set_url(args):
    url = 'https://api.github.com/repos/'
    owner = args.org if args.org else args.id
    url += owner + '/' + args.repo + '/labels'
    return url

# create authorization tuple
def set_auth(args):
    return (args.id, args.token.read().strip())

# check label list
def check_label_list(label_list):
    if not label_list:
        print('')
        print('No current labels!', end='\n\n')
        exit()

# retrieve and print current labels
def get_current(url, auth):
    r = requests.get(url, auth=auth)
    return json.loads(r.text)

# drop current labels
def drop_current(url, auth):
    label_list = get_current(url, auth)
    check_label_list(label_list)
    pretty_print(label_list, 'current labels to be dropped', ['name'])
    proceed = input('Are you sure you want to drop these labels? [Y/N]: ')
    proceed = (proceed.lower() in ['y','yes'])
    if proceed:
        print('Dropping:')
        for item in label_list:
            lab_url = url + '/' + item['name']
            r = requests.delete(lab_url, auth=auth)
            print('  - {}'.format(item['name']))

# add from file
def add_labels(args, url, auth):
    new_labels = read_json(args)
    pretty_print(new_labels, 'new labels to be added', ['name','color'])
    proceed = input('Are you sure you want to add these labels? [Y/N]: ')
    proceed = (proceed.lower() in ['y','yes'])
    if proceed:
        print('Adding:')
        for item in new_labels:
            r = requests.post(url, auth=auth, json=item)
            print('  - {}'.format(item['name']))

# --------------------------------------
# RUN
# --------------------------------------

if __name__ == "__main__":
    args = set_cli()
    url = set_url(args)
    auth = set_auth(args)
    if args.check_existing:
        label_list = get_current(url, auth)
        check_label_list(label_list)
        pretty_print(label_list, 'current labels', ['name','color','default'])
        exit()
    if args.drop_existing:
        drop_current(url, auth)
    if args.labels:
        add_labels(args, url, auth)
        
