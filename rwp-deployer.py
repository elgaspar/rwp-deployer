import download
import utilities

VERSION = "0.0.0"  # FIXME


print("RWP Deployer v" + VERSION)

settings = utilities.read_config()
repos_to_deploy = utilities.read_args()
downloader = download.RepoDownloader(
    settings['GithubToken'],
    settings['TmpDir']
)

print('Repositories to deploy: ' + ', '.join(repos_to_deploy))

for repo_name in repos_to_deploy:
    print()
    downloader.download(repo_name)
    print('Download finished successfully.')
    # print(downloaded_filepath)
