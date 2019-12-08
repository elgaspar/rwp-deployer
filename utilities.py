import configparser
import sys


def read_config():
    config = configparser.ConfigParser()
    config.read('rwp-deployer.config')
    for option in config['settings']:
        value = config['settings'][option]
        if(not value):
            error('Config file is not set.')
    return config['settings']


def read_args():
    args = sys.argv[1:]
    if not args:
        print_usage_information()
        exit()
    return args


def print_usage_information():
    print("\nUsage:")
    print("   py rwp-deployer.py [repo_names]")


def error(msg):
    print("ERROR: " + msg)
    exit()
