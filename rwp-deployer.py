import configparser
import sys

from repo_downloader import RepoDownloader

VERSION = "0.0.0"





def read_config():
    config = configparser.ConfigParser()
    config.read('rwp-deployer.config')
    for option in config['settings']:
        value = config['settings'][option]
        if(not value):
            print('Config file is not set.')
            exit()
    return config['settings']





print("RWP Deployer v" + VERSION)

settings = read_config()
repos_to_deploy = sys.argv[1:]
downloader = RepoDownloader(settings['GithubToken'], settings['TmpDir'])


print('Repositories to deploy: ' + ', '.join(repos_to_deploy))

for repo_name in repos_to_deploy:
    print()
    downloaded_filepath = downloader.download(repo_name)
    print('Download finished successfully.')
    # print(downloaded_filepath)
    
