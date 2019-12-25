from github import Github

from utilities import error


class RepoUrlGetter:

    def __init__(self, github_token):
        try:
            self.github = Github(github_token)
        except:
            error("Couldn't authenticate with GitHub.")

    def get_urls(self, repo_names):
        print("Retrieving URLs...")
        urls = {}
        contains_invalid_name = False
        for repo_name in repo_names:
            url = self.__get_repo_url(repo_name)
            if(url):
                urls[repo_name] = url
            else:
                print("Invalid repository name: " + repo_name)
                contains_invalid_name = True
        if(contains_invalid_name):
            exit()
        return urls

    def __get_repo_url(self, repo_name):
        try:
            repo = self.github.get_user().get_repo(repo_name)
        except:
            return False

        repo_url = repo.get_archive_link('zipball', 'master')
        repo_url = repo_url.replace('/legacy.zip/', '/zip/')
        return repo_url
