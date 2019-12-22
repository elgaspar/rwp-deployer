import urllib.request
import os
import shutil

import transform
from utilities import error


class RepoDownloader:

    def __init__(self, output_dir, excluded_filenames=[]):
        self.output_dir = output_dir
        self.tmp_dir = self.output_dir + '/.tmp'
        self.excluded_filenames = excluded_filenames

    def download(self, urls):
        # print()
        print('Downloading...')
        downloaded = {}
        for repo_name, url in urls.items():
            # print('Downloading ' + repo_name + "...")
            downloaded[repo_name] = self.__download_repo(repo_name, url)
        # print('All repositories were downloaded successfully.')
        return downloaded

    def __download_repo(self, repo_name, url):
        save_as = self.output_dir + '\\' + repo_name + '.zip'
        zipfile = self.__download_file(url, save_as)
        transform.tranform_zip_file(
            zipfile, self.tmp_dir, self.excluded_filenames)
        # print()
        return zipfile

    def __download_file(self, url, save_as):
        try:
            urllib.request.urlretrieve(url, save_as)
        except Exception:
            error("Couldn't download file.")
        return save_as
