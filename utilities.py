import configparser
import sys
import argparse


CONFIG_FILENAME = 'rwp-deployer.config'


def read_config(name):
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILENAME)
        for option in config[name]:
            value = config[name][option]
            if(not value):
                error('Config file is not set.')
        return config[name]
    except Exception:
        error('Config file is not set.')


def read_args():
    parser = argparse.ArgumentParser(
        description='Downloads latest code of a wordpress plugin from a GitHub repository, uploads it and install it in a WordPress server.')

    parser.add_argument('repositories', metavar='repo', nargs='+',
                        help='repository name')
    parser.add_argument('-d', dest='download_only', action='store_true',
                        help='download only and not deploy (default: false)')

    return parser.parse_args()


def print_usage_information():
    print("\nUsage:")
    print("   py rwp-deployer.py [repo_names]")


def error(msg):
    print("ERROR: " + msg)
    exit()
