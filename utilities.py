import configparser
import sys


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
