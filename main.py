#!/usr/bin/env python3
from datetime import datetime
import configparser
import requests
import json
import sys
import argparse


def get_argument_parser():


    parser = argparse.ArgumentParser(description="Downloading terms from data cookbook")
    parser.add_argument('--configfile',
                        help='path to configuration file',
                        required=True,
                        default='config.ini')
    parser.add_argument('--env',
                        help='Target environment. Used to lookup section in config file',
                        required=True,
                        default='TEST')
    parser.add_argument('--outputfile',
                        help='path to the output json file which will be saved',
                        required=True,
                        default='terms.json')

    return parser


def get_config(filename="config.ini"):
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def get_cookie(filename, env):

    config = get_config(filename=filename)
    username = config[env]['username']
    password = config[env]['password']
    instance = config[env]['instance']

    url = f"https://{instance}.datacookbook.com/session/service_login"

    headers = {'content-type': 'application/json'}

    params = {
        "un": f"{username}",
        "pw": f"{password}",
        "requestType": "service_login",
        "outputFormat": "json"
    }

    response = requests.get(url=url, params=params, headers=headers)
    response_json = response.json()
    cookie_name  = response_json['CookieList'][0]['name']
    cookie_value = response_json['CookieList'][0]['value']

    cookies = {
        f'"{cookie_name}": "{cookie_value}"'
    }

    return cookies


def get_item_list(filename, env, json_file):



    config = get_config(filename=filename)
    instance = config[env]['instance']
    username = config[env]['username']
    password = config[env]['password']

    url = f"https://{instance}.datacookbook.com/institution/terms/list"

    print(f"Getting terms list from {url}")

    #cookies = get_cookie(filename=filename, env=env)

    params = {

        "un": f"{username}",
        "pw": f"{password}",
        "requestType": "list",
        "outputFormat": "json"
    }

    headers = {'content-type': 'application/json'}

    response = requests.get(url, params=params, headers=headers)
    response_json = response.json()

    term_list = response_json['TermList']
    size = len(term_list)

    print(f"Terms list response from API has {size} records")


    print(f"saving to {json_file}")

    with open(json_file, 'w') as file:
        json.dump(term_list, file, indent=4)





def main(argv):
    print(f"*** start - {datetime.now()} ***")

    parser = get_argument_parser()
    args = parser.parse_args()

    config_file = args.configfile
    env = args.env
    json_file = args.outputfile

    get_item_list(filename=config_file, env=env, json_file=json_file)
    print(f"=== end - {datetime.now()} ===")


if __name__ == "__main__":
    main(sys.argv)