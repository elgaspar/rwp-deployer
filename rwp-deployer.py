import argparse
from repo_url_getter import RepoUrlGetter
from download import RepoDownloader
from deploy import PluginDeployer
import utilities
import json


VERSION = "0.0.0"  # FIXME

args = utilities.read_args()

print()
print("RWP Deployer v" + VERSION)

settings = utilities.read_config('settings')
remote_connect_details = utilities.read_config('remote')


print()
print('Repositories:\n\t' + '\n\t'.join(args.repositories))
print()

url_getter = RepoUrlGetter(settings['github_token'])
repo_urls = url_getter.get_urls(args.repositories)

excluded_filenames = json.loads(settings['excluded_filenames'])
downloader = RepoDownloader(settings['tmp_dir'], excluded_filenames)
downloaded = downloader.download(repo_urls)

if not args.download_only:
    deployer = PluginDeployer(remote_connect_details)
    deployer.deploy(downloaded)

    if not args.keep_files:
        print('Cleaning temporary files...')
        utilities.remove_files(downloaded.values())

print('Success')
