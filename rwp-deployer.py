import configparser
from github import Github
import wget

import os
import shutil
from pathlib import Path



def read_config():
    config = configparser.ConfigParser()
    config.read('rwp-deployer.config')
    for option in config['settings']:
        value = config['settings'][option]
        if(not value):
            print('Config file is not set.')
            exit()
    return config['settings']



def download(url, path):
    print('Downloading...')
    try:
        downloaded = wget.download(url, path)
        print()
        return downloaded
    except Exception:
        print("ERROR on downloading")
        exit()


def extract_archive(archive_filepath, output_dir):
    print('Extracting...')
    try:
        shutil.unpack_archive(archive_filepath, output_dir)
    except Exception:
        print("ERROR on extracting archive")
        exit()

def create_archive(new_archive_file, dir):
    print('Creating zip archive...')
    try:
        shutil.make_archive(new_archive_file, 'zip', dir)
    except Exception:
        print("ERROR on creating archive")
        exit()



print("--- gh2wp beta version ---")





repo_name = 'e-activities-core'


settings = read_config()




g = Github(settings['GithubToken'])



repo = g.get_user().get_repo(repo_name)



print('Repository name: ' + repo_name)

archive_url = repo.get_archive_link('zipball')



tmp_dir = settings['TmpDir']


downloaded_filepath = download(archive_url, tmp_dir)


downloaded_file_base_name = Path(downloaded_filepath).stem


extracted_dir = tmp_dir + '/.tmp' #TODO
extract_archive(downloaded_filepath, extracted_dir)


os.rename(extracted_dir + "/" + downloaded_file_base_name, extracted_dir + "/" + repo_name)
create_archive(tmp_dir + "/" + repo_name, extracted_dir)

print('Removing temporary files...')
os.remove(downloaded_filepath)
shutil.rmtree(extracted_dir)



