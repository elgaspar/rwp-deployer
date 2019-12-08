from repo_url_getter import RepoUrlGetter
from download import RepoDownloader
import utilities

VERSION = "0.0.0"  # FIXME


print("RWP Deployer v" + VERSION)

settings = utilities.read_config()
repos_to_deploy = utilities.read_args()

print()
print('Repositories to deploy: ' + ', '.join(repos_to_deploy))

url_getter = RepoUrlGetter(settings['GithubToken'])
repo_urls = url_getter.get_urls(repos_to_deploy)

downloader = RepoDownloader(settings['TmpDir'])
downloader.download(repo_urls)

# TODO: deploy downloaded files
