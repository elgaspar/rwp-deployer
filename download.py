from github import Github
import urllib.request
import os
import shutil

import transform


class RepoDownloader:

    def __init__(self, github_token, output_dir):
        try:
            self.github = Github(github_token)
        except:
            print("ERROR on authenticating with GitHub")
            exit()
        self.output_dir = output_dir
        # TODO: check if output dir exists -> if not create it

    def download(self, repo_name):
        print('Downloading ' + repo_name + "...")
        zipfile = self.__download_file(repo_name)
        transform.tranform_zip_file(zipfile, self.__get_tmp_dir())
        return zipfile

    def __download_file(self, repo_name):
        url = self.__get_repo_url(repo_name)
        try:
            filename = self.output_dir + '/' + repo_name + '.zip'
            urllib.request.urlretrieve(url, filename)
        except Exception:
            print("ERROR on downloading")
            exit()
        return filename

    def __get_repo_url(self, repo_name):
        try:
            repo = self.github.get_user().get_repo(repo_name)
        except:
            print("Invalid repository name.")
            exit()

        repo_url = repo.get_archive_link('zipball', 'master')
        repo_url = repo_url.replace('/legacy.zip/', '/zip/')
        return repo_url

    def __get_tmp_dir(self):
        return self.output_dir + '/.tmp'
