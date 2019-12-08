from github import Github
import urllib.request
import os
import shutil

import transform
from utilities import error


class RepoDownloader:

    def __init__(self, github_token, output_dir):
        try:
            self.github = Github(github_token)
        except:
            error("Couldn't authenticate with GitHub.")
        self.output_dir = output_dir
        self.tmp_dir = self.output_dir + '/.tmp'

    def download(self, repo_name):
        print('Downloading ' + repo_name + "...")
        zipfile = self.__download_file(repo_name)
        transform.tranform_zip_file(zipfile, self.tmp_dir)
        return zipfile

    def __download_file(self, repo_name):
        url = self.__get_repo_url(repo_name)
        try:
            filename = self.output_dir + '/' + repo_name + '.zip'
            urllib.request.urlretrieve(url, filename)
        except Exception:
            error("Couldn't download file.")
        return filename

    def __get_repo_url(self, repo_name):
        try:
            repo = self.github.get_user().get_repo(repo_name)
        except:
            error("Invalid repository name.")

        repo_url = repo.get_archive_link('zipball', 'master')
        repo_url = repo_url.replace('/legacy.zip/', '/zip/')
        return repo_url
