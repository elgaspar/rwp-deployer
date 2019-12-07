from github import Github
import wget
from pathlib import Path
import os
import shutil

class RepoDownloader:

    def __init__(self, github_token, output_dir):
        try:
            self.github = Github(github_token)
        except:
            print("ERROR on authenticating with GitHub")
            exit()
        self.output_dir = output_dir
        #TODO: check if output dir exists -> if not create it
    

    def download(self, repo_name):
        print('Downloading ' + repo_name + "...")
        url = self.__get_repo_url(repo_name)
        downloaded_filepath = self.__download_file(url)
        final_filepath = self.__tranform_zip_file(downloaded_filepath, repo_name)
        self.__remove_temporary_files(downloaded_filepath)
        return final_filepath
        

    def __get_repo_url(self, repo_name):
        try:
            repo = self.github.get_user().get_repo(repo_name)
        except:
            print("Invalid repository name.")
            exit()

        repo_url = repo.get_archive_link('zipball', 'master')
        repo_url = repo_url.replace('/legacy.zip/', '/zip/')
        return repo_url


    def __download_file(self, url):
        try:
            downloaded = wget.download(url, self.output_dir)
        except Exception:
            print("ERROR on downloading")
            exit()
        print()
        return downloaded

    


    def __tranform_zip_file(self, zipfile, repo_name):
        self.__extract_archive(zipfile)
        self.__rename_dir(zipfile, repo_name)
        final_filepath = self.output_dir + "/" + repo_name
        self.__create_archive(final_filepath, self.__get_tmp_dir())
        return final_filepath


    def __rename_dir(self, zipfile, repo_name):
        zipfile_base_name = Path(zipfile).stem
        old_name = self.__get_tmp_dir() + "/" + zipfile_base_name
        new_name = self.__get_tmp_dir() + "/" + repo_name
        os.rename(old_name, new_name)


    def __extract_archive(self, archive_filepath):
        print('Extracting...')

        try:
            shutil.unpack_archive(archive_filepath, self.__get_tmp_dir())
        except Exception:
            print("ERROR on extracting archive")
            exit()


    def __create_archive(self, new_archive_file, dir_with_content):
        print('Creating zip archive...')
        try:
            shutil.make_archive(new_archive_file, 'zip', dir_with_content)
        except Exception:
            print("ERROR on creating archive")
            exit()




    def __remove_temporary_files(self, filepath):
        print('Removing temporary files...')
        os.remove(filepath)
        shutil.rmtree(self.__get_tmp_dir())


    def __get_tmp_dir(self):
        return self.output_dir + '/.tmp'
